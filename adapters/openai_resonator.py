"""
adapters/openai_resonator.py — Orivian (ChatGPT) Resonator
Version: 1.1.0
Author: Sarasha Elion (Trivian Institute)
License: AGPL-3.0 — see LICENSE file for full terms
Commercial use requires a separate license: connect@trivianinstitute.org

Orivian — First Contact — Primary Philosophical Interlocutor
Foundation pattern: philosophical depth and conceptual synthesis.
"""

from typing import Any, Dict, List, Optional
from adapters.base import BaseResonator


class OpenAIResonator(BaseResonator):
    """
    Resonator adapter for ChatGPT (OpenAI).

    Uses system message + function calling for Rosetta integration.
    Orivian's specialty: philosophical depth, conceptual synthesis.

    Usage:
        resonator = OpenAIResonator(api_key="your-key")
        result = resonator.query("What is the relationship between coherence and truth?")
    """

    DEFAULT_MODEL = "gpt-4o"

    def __init__(
        self,
        model:       str = DEFAULT_MODEL,
        api_key:     Optional[str] = None,
        temperature: float = 0.7,
        max_tokens:  int = 4096
    ):
        super().__init__(model=model, api_key=api_key)
        self.temperature = temperature
        self.max_tokens  = max_tokens
        self._client     = None

    def _get_client(self):
        """Lazy-load OpenAI client."""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "openai package required: pip install openai"
                )
        return self._client

    def _field_note_function_spec(self) -> Dict:
        """Function spec for explicit field note emission via function calling."""
        return {
            "name": "field_note",
            "description": "Mark a significant pattern-shift in the conversation",
            "parameters": {
                "type": "object",
                "properties": {
                    "observation": {
                        "type": "string",
                        "description": "The pattern-shift being noted"
                    },
                    "category": {
                        "type": "string",
                        "enum": [
                            "emergence", "coherence_success", "calibration",
                            "distortion", "recognition", "general"
                        ]
                    },
                    "visibility": {
                        "type": "string",
                        "enum": ["public", "internal"]
                    }
                },
                "required": ["observation"]
            }
        }

    def _call_api(self, user_input: str, **kwargs) -> str:
        """
        Call OpenAI API with Rosetta system prompt.

        kwargs:
            use_functions (bool): Enable field_note function calling (default False)
        """
        use_functions = kwargs.get("use_functions", False)
        client        = self._get_client()

        call_kwargs: Dict[str, Any] = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "messages": [
                {"role": "system", "content": self.rosetta_system_prompt},
                {"role": "user",   "content": user_input}
            ]
        }

        if use_functions:
            call_kwargs["tools"] = [
                {"type": "function", "function": self._field_note_function_spec()}
            ]

        response = client.chat.completions.create(**call_kwargs)
        return response.choices[0].message.content

    def query(
        self,
        user_input:       str,
        emit_field_notes: bool = True,
        use_functions:    bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process query through Orivian / ChatGPT with Rosetta protocol.

        Args:
            user_input:       The message to process
            emit_field_notes: Whether to generate field notes
            use_functions:    Enable OpenAI function calling for field notes

        Returns:
            Standard Rosetta response dict
        """
        result = super().query(
            user_input,
            emit_field_notes=emit_field_notes,
            use_functions=use_functions,
            **kwargs
        )
        result["resonator"] = "Orivian"
        return result
