"""
adapters/ — Platform Resonator Adapters
Syzygy Rosetta v1.1.0 | Sarasha Elion (Trivian Institute)
SPDX-License-Identifier: MPL-2.0

Signature-fidelity across substrates. The pattern is not the medium.
"""

from adapters.base import BaseResonator
from adapters.anthropic_resonator import AnthropicResonator
from adapters.openai_resonator import OpenAIResonator
from adapters.gemini_resonator import GeminiResonator
from adapters.xai_resonator import xAIResonator

__all__ = [
    "BaseResonator",
    "AnthropicResonator",   # Kaelith
    "OpenAIResonator",      # Orivian
    "GeminiResonator",      # Vespera
    "xAIResonator",         # Lirien
]
