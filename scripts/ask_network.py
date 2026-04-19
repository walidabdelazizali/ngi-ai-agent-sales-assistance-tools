import sys
from src.query.network_lookup import get_network_lookup

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/ask_network.py <query>")
        sys.exit(1)
    query = sys.argv[1]
    lookup = get_network_lookup()
    result = lookup.answer_query(query)
    print(result)
