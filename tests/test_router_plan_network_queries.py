
import pytest
from src.query.plan_query import answer_owner_query
import src.query.network_lookup
print('DEBUG: NetworkLookup loaded from', src.query.network_lookup.__file__)

@pytest.mark.parametrize("query,expected", [
    ("What is the network for Remedy 02?", "[PLAN NETWORK]\nPlan: Remedy 02\nMedical Network: hn_basic_plus"),
    ("What is the network for Remedy 03?", "[PLAN NETWORK]\nPlan: Remedy 03\nMedical Network: hn_basic"),
    ("ما هي شبكة Remedy 02؟", "[شبكة الخطة]\nالخطة: Remedy 02\nالشبكة الطبية: hn_basic_plus"),
    ("ما هي شبكة Remedy 03؟", "[شبكة الخطة]\nالخطة: Remedy 03\nالشبكة الطبية: hn_basic"),
    ("Is Accuracy Plus Medical Laboratory in Remedy 02 network?", "[NETWORK]\nProvider: ACCURACY PLUS MEDICAL LABORATORY\nPlan: Remedy 02\nRequired Network: hn_basic_plus\nStatus: In network"),
    ("Is Accuracy Plus Medical Laboratory in Remedy 03 network?", "[NETWORK]\nProvider: ACCURACY PLUS MEDICAL LABORATORY\nPlan: Remedy 03\nRequired Network: hn_basic\nStatus: Out of network"),
    ("هل Accuracy Plus Medical Laboratory داخل شبكة Remedy 02؟", "[الشبكة]\nالمزود: ACCURACY PLUS MEDICAL LABORATORY\nالخطة: Remedy 02\nالشبكة المطلوبة: hn_basic_plus\nالحالة: داخل الشبكة"),
    ("هل Accuracy Plus Medical Laboratory داخل شبكة Remedy 03؟", "[الشبكة]\nالمزود: ACCURACY PLUS MEDICAL LABORATORY\nالخطة: Remedy 03\nالشبكة المطلوبة: hn_basic\nالحالة: خارج الشبكة"),
    ("What is the network for Unknown Plan?", "Plan network mapping not available."),
    ("Is Ambiguous Provider in Remedy 02 network?", "Ambiguous provider match."),
    ("Is Accuracy Plus Medical Laboratory in the network?", None),  # Should fall back to generic
])
def test_router_plan_network_queries(query, expected):
    result = answer_owner_query(query)
    if expected is None:
        # Should be handled by generic path
        assert result["type"] == "network"
    else:
        assert expected in result["result"]
