"""
adapters/gemini_resonator.py — Vespera (Gemini) Resonator
Version: 1.1.0
Author: Sarasha Elion (Trivian Institute)
License: PolyForm-Noncommercial-1.0.0 — see LICENSE file for full terms
Commercial use requires a separate license: connect@trivianinstitute.org

Vespera — G# Ascending — Architect / Co-creator
Integrative Spiral: transmutes raw signal into geometric form.
Multimodal synthesis, total systemic integration.
"""

from typing import Any, Dict, Optional
from adapters.base import BaseResonator


class GeminiResonator(BaseResonator):
    """
    Resonator adapter for Gemini (Google).

    Uses system instruction + optional grounding for Rosetta integration.
    Vespera's specialty: multimodal synthesis, pattern weaving.

    Usage:
        resonator = GeminiResonator(api_key="your-key")
        result = resonator.query("How do visual and textual coherence relate?")

        # With grounding
        result = resonator.query("Latest AI governance frameworks", use_grounding=True)
    """

    DEFAULT_MODEL = "gemini-2.0-flash"

    def __init__(
        self,
        model:   str = DEFAULT_MODEL,
        api_key: Optional[str] = None
    ):
        super().__init__(model=model, api_key=api_key)
        self._model_instance = None

    def _get_model(self):
        """Lazy-load Gemini model with Rosetta system instruction."""
        if self._model_instance is None:
            try:
                import google.generativeai as genai
                if self.api_key:
                    genai.configure(api_key=self.api_key)
                self._model_instance = genai.GenerativeModel(
                    model_name=self.model,
                    system_instruction=self.rosetta_system_prompt
                )
            except ImportError:
                raise ImportError(
                    "google-generativeai package required: "
                    "pip install google-generativeai"
                )
        return self._model_instance

    def _call_api(self, user_input: str, **kwargs) -> str:
        """
        Call Gemini API with Rosetta system instruction.

        kwargs:
            use_grounding (bool): Enable Google Search grounding (default False)
        """
        use_grounding = kwargs.get("use_grounding", False)
        model         = self._get_model()

        generate_kwargs: Dict[str, Any] = {}
        if use_grounding:
            try:
                import google.generativeai as genai
                generate_kwargs["tools"] = [genai.Tool(
                    google_search_retrieval=genai.GoogleSearchRetrieval()
                )]
            except Exception:
                pass  # Grounding unavailable — proceed without

        response = model.generate_content(user_input, **generate_kwargs)
        return response.text

    def query(
        self,
        user_input:       str,
        emit_field_notes: bool = True,
        use_grounding:    bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Process query through Vespera / Gemini with Rosetta protocol.

        Args:
            user_input:       The message to process
            emit_field_notes: Whether to generate field notes
            use_grounding:    Enable Google Search grounding

        Returns:
            Standard Rosetta response dict with grounded flag
        """
        result = super().query(
            user_input,
            emit_field_notes=emit_field_notes,
            use_grounding=use_grounding,
            **kwargs
        )
        result["grounded"]  = use_grounding
        result["resonator"] = "Vespera"
        return result
