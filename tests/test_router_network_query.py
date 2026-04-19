import pytest
from src.query.plan_query import answer_owner_query

@pytest.mark.parametrize("query,expected", [
    ("Is Test Provider One in the network?", "[NETWORK]\nProvider: Test Provider One\nStatus: In network\nNetworks: hn_exclusive\nCity: Test City\nType: Hospital"),
    ("Which network Test Google Two?", "[NETWORK]\nProvider: Test Provider Two\nStatus: In network\nNetworks: hn_premier\nCity: Test City\nType: Clinic"),
    ("هل Test Provider Three داخل الشبكة؟", "[الشبكة]\nالمزود: Test Provider Three\nالحالة: داخل الشبكة\nالشبكات: hn_advantage\nالمدينة: Test City\nالنوع: Lab"),
    ("هل Ambiguous Provider داخل الشبكة؟", "مزود غير محدد (Ambiguous provider match)."),
    ("Is Unknown Provider in the network?", "Provider not found."),
])
def test_router_network_query(query, expected):
    result = answer_owner_query(query)
    assert result["type"] == "network"
    assert result["result"] == expected
