

# Only one class definition should exist. All methods must be inside this class.
import pandas as pd
from pathlib import Path
import re

NETWORK_CSV = Path("runtime_data/networks/network_list_normalized.csv")

class NetworkLookup:
    def __init__(self, csv_path=NETWORK_CSV):
        self.df = pd.read_csv(csv_path, dtype=str, encoding='utf-8-sig').fillna("")
        self.df.columns = [c.lower() for c in self.df.columns]
        self.network_tier_cols = [
            c for c in self.df.columns
            if (
                c.lower().startswith("hn ")
                or c.lower().startswith("hn_")
                or c.lower().startswith("essential")
                or c.lower().endswith("plus")
                or c.lower().endswith("basic")
            )
        ]
        # Build lookup indexes
        self.provider_name_idx = {}
        self.google_name_idx = {}
        for idx, row in self.df.iterrows():
            pn = self._normalize(row.get("provider_name", ""))
            gn = self._normalize(row.get("google_name", ""))
            if pn:
                self.provider_name_idx.setdefault(pn, []).append(idx)
            if gn:
                self.google_name_idx.setdefault(gn, []).append(idx)

    @staticmethod
    def _normalize(s):
        if not isinstance(s, str):
            s = str(s)
        s = s.strip().lower()
        s = re.sub(r"[؟?]$", "", s)
        s = re.sub(r"[\s\t\n\r]+", " ", s)
        s = re.sub(r"^[^\w\d]+|[^\w\d]+$", "", s)  # strip simple punctuation at ends
        s = re.sub(r"[\.,;:!\-\(\)\[\]{}'\"]", "", s)  # remove simple punctuation inside
        return s

    @staticmethod
    def extract_provider_from_query(query):
        # English patterns
        patterns = [
            r"is\s+(.+?)\s+in the network",
            r"which network\s+(.+?)(?:\?|$)",
            r"details\s+(.+?)(?:\?|$)",
            # Arabic patterns
            r"هل\s+(.+?)\s+داخل الشبكة",
            r"ما هي الشبكات المتاحة ل[ـ]؟?\s*([\w\s]+)",
            r"ما هي الشبكات المتاحة لـ\s*([\w\s]+)",
        ]
        for pat in patterns:
            m = re.search(pat, query, re.IGNORECASE)
            if m:
                return m.group(1).strip()
        # fallback: try to use the whole query
        return query.strip()

    def find_provider(self, name):
        norm = self._normalize(name)
        # 1. exact provider_name
        if norm in self.provider_name_idx:
            idxs = self.provider_name_idx[norm]
            if len(idxs) == 1:
                return self.df.iloc[idxs[0]]
            return 'ambiguous' if len(idxs) > 1 else None
        # 2. exact google_name
        if norm in self.google_name_idx:
            idxs = self.google_name_idx[norm]
            if len(idxs) == 1:
                return self.df.iloc[idxs[0]]
            return 'ambiguous' if len(idxs) > 1 else None
        # 3. unique contains match
        matches = []
        for idx, row in self.df.iterrows():
            pn = self._normalize(row.get("provider_name", ""))
            gn = self._normalize(row.get("google_name", ""))
            if norm in pn or norm in gn:
                matches.append(idx)
        if len(matches) == 1:
            return self.df.iloc[matches[0]]
        if len(matches) > 1:
            return 'ambiguous'
        return None

    def provider_details(self, name):
        row = self.find_provider(name)
        if row is None:
            return {"found": False}
        if isinstance(row, str) and row == 'ambiguous':
            return {"found": False, "ambiguous": True}
        if not hasattr(row, "get"):
            # Defensive: not a dict/Series, treat as not found
            return {"found": False}
        unavailable_values = ("", "-", "0", "x", "X", "✖", "✕", "✗", "no", "n", "false")
        available_values = ("✔", "✓", "yes", "y", "true", "1")
        available = []
        for tier in self.network_tier_cols:
            val = str(row.get(tier, "")).strip()
            if val in available_values:
                available.append(tier)
            elif val and val not in unavailable_values:
                # Defensive: treat any non-empty, non-unavailable, non-explicitly available as available
                available.append(tier)
        return {
            "provider_name": row.get("provider_name", ""),
            "google_name": row.get("google_name", ""),
            "city": row.get("city", ""),
            "type": row.get("type", ""),
            "available_network_tiers": available,
            "found": True
        }

    def is_in_network(self, name):
        details = self.provider_details(name)
        return details.get("found", False) and bool(details.get("available_network_tiers", []))

    def which_networks(self, name):
        details = self.provider_details(name)
        return details["available_network_tiers"] if details.get("found", False) else []

    def answer_query(self, query):
        # Extract provider from query
        provider = self.extract_provider_from_query(query)
        norm_provider = self._normalize(provider)
        # in network?
        if re.search(r"is .+ in the network|هل .+ داخل الشبكة", query, re.IGNORECASE):
            found = self.is_in_network(provider)
            return f"YES: {norm_provider}" if found else f"NO: {norm_provider}"
        # which network?
        if re.search(r"which network|ما هي الشبكات", query, re.IGNORECASE):
            nets = self.which_networks(provider)
            return f"Networks for {norm_provider}: {', '.join(nets) if nets else 'None'}"
        # details
        if re.search(r"details|تفاصيل", query, re.IGNORECASE):
            d = self.provider_details(provider)
            return str(d)
        # fallback: try direct lookup
        d = self.provider_details(provider)
        if d.get("found", False):
            return str(d)
        if d.get("ambiguous", False):
            return "Ambiguous provider match."
        return "Provider not found."

    def provider_in_network(self, provider_name, network_code):
        details = self.provider_details(provider_name)
        if not details.get("found"):
            return {"found": False}
        if details.get("ambiguous"):
            return {"found": False, "ambiguous": True}
        tiers = details.get("available_network_tiers", [])
        in_network = network_code in tiers
        return {
            "found": True,
            "ambiguous": False,
            "provider_name": details.get("provider_name"),
            "google_name": details.get("google_name"),
            "city": details.get("city"),
            "type": details.get("type"),
            "network_code": network_code,
            "in_network": in_network,
            "available_network_tiers": tiers,
        }

    def provider_details_for_network(self, provider_name, network_code):
        # Alias for provider_in_network for clarity
        return self.provider_in_network(provider_name, network_code)

    def provider_details_for_network(self, provider_name, network_code):
        # Alias for provider_in_network for clarity
        return self.provider_in_network(provider_name, network_code)
import pandas as pd
from pathlib import Path
import re

NETWORK_CSV = Path("runtime_data/networks/network_list_normalized.csv")


class NetworkLookup:
    def __init__(self, csv_path=NETWORK_CSV):
        self.df = pd.read_csv(csv_path, dtype=str, encoding='utf-8-sig').fillna("")
        self.df.columns = [c.lower() for c in self.df.columns]
        self.network_tier_cols = [
            c for c in self.df.columns
            if (
                c.lower().startswith("hn ")
                or c.lower().startswith("hn_")
                or c.lower().startswith("essential")
                or c.lower().endswith("plus")
                or c.lower().endswith("basic")
            )
        ]
        # Build lookup indexes
        self.provider_name_idx = {}
        self.google_name_idx = {}
        for idx, row in self.df.iterrows():
            pn = self._normalize(row.get("provider_name", ""))
            gn = self._normalize(row.get("google_name", ""))
            if pn:
                self.provider_name_idx.setdefault(pn, []).append(idx)
            if gn:
                self.google_name_idx.setdefault(gn, []).append(idx)

    @staticmethod
    def _normalize(s):
        if not isinstance(s, str):
            s = str(s)
        s = s.strip().lower()
        s = re.sub(r"[؟?]$", "", s)
        s = re.sub(r"[\s\t\n\r]+", " ", s)
        s = re.sub(r"^[^\w\d]+|[^\w\d]+$", "", s)  # strip simple punctuation at ends
        s = re.sub(r"[\.,;:!\-\(\)\[\]{}'\"]", "", s)  # remove simple punctuation inside
        return s

    @staticmethod
    def extract_provider_from_query(query):
        # English patterns
        patterns = [
            r"is\s+(.+?)\s+in the network",
            r"which network\s+(.+?)(?:\?|$)",
            r"details\s+(.+?)(?:\?|$)",
            # Arabic patterns
            r"هل\s+(.+?)\s+داخل الشبكة",
            r"ما هي الشبكات المتاحة ل[ـ]؟?\s*([\w\s]+)",
            r"ما هي الشبكات المتاحة لـ\s*([\w\s]+)",
        ]
        for pat in patterns:
            m = re.search(pat, query, re.IGNORECASE)
            if m:
                return m.group(1).strip()
        # fallback: try to use the whole query
        return query.strip()

    def find_provider(self, name):
        norm = self._normalize(name)
        # 1. exact provider_name
        if norm in self.provider_name_idx:
            idxs = self.provider_name_idx[norm]
            if len(idxs) == 1:
                return self.df.iloc[idxs[0]]
            return 'ambiguous' if len(idxs) > 1 else None
        # 2. exact google_name
        if norm in self.google_name_idx:
            idxs = self.google_name_idx[norm]
            if len(idxs) == 1:
                return self.df.iloc[idxs[0]]
            return 'ambiguous' if len(idxs) > 1 else None
        # 3. unique contains match
        matches = []
        for idx, row in self.df.iterrows():
            pn = self._normalize(row.get("provider_name", ""))
            gn = self._normalize(row.get("google_name", ""))
            if norm in pn or norm in gn:
                matches.append(idx)
        if len(matches) == 1:
            return self.df.iloc[matches[0]]
        if len(matches) > 1:
            return 'ambiguous'
        return None

    def provider_details(self, name):
        row = self.find_provider(name)
        if row is None:
            return {"found": False}
        if isinstance(row, str) and row == 'ambiguous':
            return {"found": False, "ambiguous": True}
        if not hasattr(row, "get"):
            # Defensive: not a dict/Series, treat as not found
            return {"found": False}
        unavailable_values = ("", "-", "0", "x", "X", "✖", "✕", "✗", "no", "n", "false")
        available_values = ("✔", "✓", "yes", "y", "true", "1")
        available = []
        for tier in self.network_tier_cols:
            val = str(row.get(tier, "")).strip()
            if val in available_values:
                available.append(tier)
            elif val and val not in unavailable_values:
                # Defensive: treat any non-empty, non-unavailable, non-explicitly available as available
                available.append(tier)
        return {
            "provider_name": row.get("provider_name", ""),
            "google_name": row.get("google_name", ""),
            "city": row.get("city", ""),
            "type": row.get("type", ""),
            "available_network_tiers": available,
            "found": True
        }

    def is_in_network(self, name):
        details = self.provider_details(name)
        return details.get("found", False) and bool(details.get("available_network_tiers", []))

    def which_networks(self, name):
        details = self.provider_details(name)
        return details["available_network_tiers"] if details.get("found", False) else []

    def answer_query(self, query):
        # Extract provider from query
        provider = self.extract_provider_from_query(query)
        norm_provider = self._normalize(provider)
        # in network?
        if re.search(r"is .+ in the network|هل .+ داخل الشبكة", query, re.IGNORECASE):
            found = self.is_in_network(provider)
            return f"YES: {norm_provider}" if found else f"NO: {norm_provider}"
        # which network?
        if re.search(r"which network|ما هي الشبكات", query, re.IGNORECASE):
            nets = self.which_networks(provider)
            return f"Networks for {norm_provider}: {', '.join(nets) if nets else 'None'}"
        # details
        if re.search(r"details|تفاصيل", query, re.IGNORECASE):
            d = self.provider_details(provider)
            return str(d)
        # fallback: try direct lookup
        d = self.provider_details(provider)
        if d.get("found", False):
            return str(d)
        if d.get("ambiguous", False):
            return "Ambiguous provider match."
        return "Provider not found."

def get_network_lookup():
    return NetworkLookup()
