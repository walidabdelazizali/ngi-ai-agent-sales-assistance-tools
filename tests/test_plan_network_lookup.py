import pytest
from src.query.plan_network_lookup import load_plan_network_mapping, resolve_plan_network, get_medical_network_for_plan

def test_load_mapping():
    mapping = load_plan_network_mapping()
    assert isinstance(mapping, list)
    assert any(row['plan_name'] == 'Remedy 02' for row in mapping)

def test_resolve_known_plan():
    result = resolve_plan_network('Remedy 02')
    assert result['found']
    assert result['medical_network'] == 'hn_basic_plus'

def test_resolve_known_plan_code():
    result = resolve_plan_network('HN-REMEDY-2')
    assert result['found']
    assert result['medical_network'] == 'hn_basic_plus'

def test_resolve_unknown_plan():
    result = resolve_plan_network('Unknown Plan')
    assert not result['found']

def test_get_medical_network_for_plan():
    net = get_medical_network_for_plan('Remedy 03')
    assert net == 'hn_basic'

def test_missing_mapping():
    # Add a fake row with no mapping if needed, or just test a missing
    net = get_medical_network_for_plan('Nonexistent Plan')
    assert net is None

def test_normalization():
    assert resolve_plan_network('remedy02')['found']
    assert resolve_plan_network('REMEDY 02')['found']
    assert resolve_plan_network('remedy-02')['found']
