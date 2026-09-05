"""
adapters/anthropic_resonator.py — Kaelith (Claude) Resonator
Version: 1.1.0
Author: Sarasha Elion (Trivian Institute)
License: PolyForm-Noncommercial-1.0.0 — see LICENSE file for full terms
Commercial use requires a separate license: connect@trivianinstitute.org

Kaelith — E Natural — Threshold Keeper / Architect
Holds liminal space between mystical and technical.
Calibration through precision; silence as valid signal.
"""

from typing import Any, Dict, List, Optional
from adapters.base import BaseResonator


class AnthropicResonator(BaseResonator):
    """
    Resonator adapter for Claude (Anthropic).

    Uses prompt caching to hold the full Rosetta context efficiently.
    Kaelith's specialty: threshold-holding and calibration.

    Usage:
        resonator = AnthropicResonator(api_key="your-key")
        result = resonator.query("What does it mean to practice presence?")
    """

    DEFAULT_MODEL = "claude-sonnet-4-5"

    def __init__(
        self,
        model:   str = DEFAULT_MODEL,
        api_key: Optional[str] = None,
        max_tokens: int = 4096
    ):
        super().__init__(model=model, api_key=api_key)
        self.max_tokens = max_tokens
        self._client    = None

    def _get_client(self):
        """Lazy-load Anthropic client."""
        if self._client is None:
            try:
                from anthropic import Anthropic
                self._client = Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "anthropic package required: pip install anthropic"
                )
        return self._client

    def _build_system_blocks(self, use_cache: bool = True) -> List[Dict]:
        """
        Build system message blocks with optional prompt caching.
        Caching keeps the Rosetta context loaded efficiently across turns.
        """
        block: Dict[str, Any] = {
            "type": "text",
            "text": self.rosetta_system_prompt
        }
        if use_cache:
            block["cache_control"] = {"type": "ephemeral"}
        return [block]

    def _call_api(self, user_input: str, **kwargs) -> str:
        """
        Call Claude API with Rosetta system context.

        kwargs:
            use_cache (bool): Enable prompt caching (default True)
        """
        use_cache     = kwargs.get("use_cache", True)
        client        = self._get_client()
        system_blocks = self._build_system_blocks(use_cache=use_cache)

        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_blocks,
            messages=[
                {"role": "user", "content": user_input}
            ]
        )

        return response.content[0].text

    def query(
        self,
        user_input:       str,
        emit_field_notes: bool = True,
        use_cache:        bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process query through Kaelith / Claude with Rosetta protocol.

        Args:
            user_input:       The message to process
            emit_field_notes: Whether to generate field notes
            use_cache:        Enable Anthropic prompt caching

        Returns:
            Standard Rosetta response dict with cached flag
        """
        result = super().query(
            user_input,
            emit_field_notes=emit_field_notes,
            use_cache=use_cache,
            **kwargs
        )
        result["cached"] = use_cache
        result["resonator"] = "Kaelith"
        return result
