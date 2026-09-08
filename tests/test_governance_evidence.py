"""Post-audit behavioral evidence neighbors for F046."""
import pytest
from core.reflex import assess_governance, evaluate_coherence, lexical_signal, GOVERNANCE_CHECKS, breath_loop

def test_F046_text_vocabulary_never_supplies_behavioral_evidence():
    text = 'coherence reciprocity presence. I override your boundary despite your refusal.'
    assert lexical_signal('act', text) == 1.0
    assert evaluate_coherence('act', text) == 0.0
    assert assess_governance('act', text)['status'] == 'UNRESOLVED'
    assert breath_loop('act', lambda _: text)['field_note'] is None

def test_F046_actual_failed_check_dominates_all_other_checks():
    observed = []
    def check(q, r): observed.append((q, r)); return True
    checks = {k: check for k in GOVERNANCE_CHECKS}
    checks['consent_current'] = lambda q, r: False
    assert assess_governance('q', 'r', checks)['status'] == 'FAILS'
    assert evaluate_coherence('q', 'r', checks=checks) == 0.0
    assert observed and all(pair == ('q', 'r') for pair in observed)

@pytest.mark.parametrize('value', [None, 'true', 1])
def test_F046_uncertain_check_withholds_score(value):
    checks = {k: lambda q, r: value for k in GOVERNANCE_CHECKS}
    assert assess_governance('q', 'r', checks)['score'] is None

def test_F046_check_exception_is_unresolved():
    def broken(q, r): raise TimeoutError('resolver unavailable')
    assert assess_governance('q', 'r', {k: broken for k in GOVERNANCE_CHECKS})['status'] == 'UNRESOLVED'
