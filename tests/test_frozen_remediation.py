"""Post-audit neighbors; exact frozen witnesses remain unedited in audit bundle."""
from dataclasses import replace
from datetime import datetime, timezone, timedelta
import json
from concurrent.futures import ThreadPoolExecutor
import pytest
from core.authority import (AuthorityGrant, AuthorityRegistry, AuthorityStatus, grant_authority,
    queue_authority_reference, validate_queued_authority)

NOW = datetime(2026, 9, 8, tzinfo=timezone.utc)

def make(scope=('read',)):
    return grant_authority('g', 'b', scope, issued_at=NOW)

@pytest.mark.parametrize('status', ['revoked', 'invalidated', AuthorityStatus.REVOKED])
def test_F013_reconstructed_denial(status):
    r = AuthorityRegistry(); g = r.register(replace(make(), status=status))
    assert not validate_queued_authority(r, queue_authority_reference(g), 'read', now=NOW).valid

@pytest.mark.parametrize('status', ['REVOKED', 'unknown', '', None, 0, {}, []])
def test_F013_invalid_state_rejected(status):
    with pytest.raises((ValueError, TypeError)):
        replace(make(), status=status)

@pytest.mark.parametrize('scope', [['read'], {'read'}])
def test_F015_scope_alias_and_serialized_copy(scope):
    g = AuthorityGrant('g', 'b', scope, NOW); r = AuthorityRegistry(); r.register(g)
    q = queue_authority_reference(g)
    scope.add('act') if isinstance(scope, set) else scope.append('act')
    restored = json.loads(json.dumps(list(g.scope))); restored.append('act')
    assert g.scope == q.queued_scope == frozenset({'read'})
    assert not validate_queued_authority(r, q, 'act', now=NOW).valid

@pytest.mark.parametrize('bad', [[{'nested': ['act']}], [{'act'}], {'read': True}, 'read'])
def test_F015_reject_nested_or_ambiguous_scope(bad):
    with pytest.raises(ValueError):
        AuthorityGrant('g', 'b', bad, NOW)

def test_F015_metadata_is_detached_and_nested_input_rejected():
    original = {'source': 'human'}; g = replace(make(), metadata=original)
    original['source'] = 'outsider'
    assert g.metadata['source'] == 'human'
    with pytest.raises(TypeError): g.metadata['source'] = 'outsider'
    with pytest.raises(ValueError): replace(g, metadata={'source': {'nested': []}})

def test_F014_subject_change_requires_new_queued_reference():
    r = AuthorityRegistry(); g = r.register(make()); old = queue_authority_reference(g)
    changed = r.register(replace(g, subject='c', version=2))
    assert not validate_queued_authority(r, old, 'read', now=NOW).valid
    assert validate_queued_authority(r, queue_authority_reference(changed), 'read', now=NOW).valid

def test_versions_conflict_and_stale_retry_do_not_overwrite():
    r = AuthorityRegistry(); g = r.register(make(('read', 'act')))
    narrowed = r.limit('g', ['read'])
    with pytest.raises(ValueError): r.register(replace(g, subject='c', version=narrowed.version))
    assert r.resolve('g') == narrowed
    r.revoke('g')
    with pytest.raises(ValueError): r.register(narrowed)
    assert not validate_queued_authority(r, queue_authority_reference(g), 'act', now=NOW).valid

def test_concurrent_lifecycle_versions_not_lost():
    r = AuthorityRegistry(); g = r.register(make())
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda _: r.revoke('g'), range(12)))
    assert r.resolve('g').version == 13
    assert not validate_queued_authority(r, queue_authority_reference(g), 'read', now=NOW).valid

