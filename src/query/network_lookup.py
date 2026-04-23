
# Centralized alias mapping for network columns
NETWORK_ALIASES = {
    "hn_basic_plus": [
        "basic plus",
        "hn basic plus",
        "basic plus network",
        "بيسك بلس",
        "شبكة بيسك بلس"
    ]
}


# Only one class definition should exist. All methods must be inside this class.
import pandas as pd
from pathlib import Path
import re
import unicodedata

NETWORK_CSV = Path("runtime_data/networks/network_list_normalized.csv")

class NetworkLookup:
    @staticmethod
    def extract_provider_from_query(query):
        # English: Is [PROVIDER] in the network?
        m = re.match(r"is\s+(.+?)\s+in the network", query.strip().lower())
        if m:
            return m.group(1).strip().title()
        # Arabic: هل [PROVIDER] داخل الشبكة؟
        m = re.match(r"هل\s+(.+?)\s+داخل الشبكة", query.strip().lower())
        if m:
            return m.group(1).strip().title()
        # Fallback: return whole query
        return query.strip()
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
        s = re.sub(r" +", " ", s)  # collapse multiple spaces
        return s

    @staticmethod
    def extract_provider_and_network_from_query(query):
        # Normalize query
        q = query.strip().lower()
        # Try to find network alias in query
        for col, aliases in NETWORK_ALIASES.items():
            for alias in aliases:
                # English: 'in [alias]' | Arabic: 'في [alias]'
                if f"in {alias}" in q:
                    parts = q.split(f"in {alias}", 1)
                    provider = parts[0].replace("is", "").strip(" ؟?.,:!\-\n\t")
                    return provider, col
                if f"في {alias}" in q:
                    parts = q.split(f"في {alias}", 1)
                    provider = parts[0].replace("هل", "").strip(" ؟?.,:!\-\n\t")
                    return provider, col
        # Fallback: no alias found, try generic patterns
        # English: Is [PROVIDER] in the network?
        m = re.match(r"is\s+(.+?)\s+in the network", q)
        if m:
            return m.group(1).strip(), None
        # Arabic: هل [PROVIDER] داخل الشبكة؟
        m = re.match(r"هل\s+(.+?)\s+داخل الشبكة", q)
        if m:
            return m.group(1).strip(), None
        # Fallback: return whole query as provider
        return query.strip(), None

    def find_provider(self, name):
        norm = self._normalize(name)
        print(f"[DEBUG] find_provider: input='{name}', normalized='{norm}'")
        # 1. exact provider_name
        if norm in self.provider_name_idx:
            print(f"[DEBUG] provider_name_idx match for '{norm}'")
            idxs = self.provider_name_idx[norm]
            if len(idxs) == 1:
                return self.df.iloc[idxs[0]]
            return 'ambiguous' if len(idxs) > 1 else None
        # 2. exact google_name
        if norm in self.google_name_idx:
            print(f"[DEBUG] google_name_idx match for '{norm}'")
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
        print(f"[DEBUG] contains matches for '{norm}': {matches}")
        if len(matches) == 1:
            return self.df.iloc[matches[0]]
        if len(matches) > 1:
            return 'ambiguous'
        return None

    def is_in_network(self, name):
        details = self.provider_details(name)
        return details.get("found", False) and bool(details.get("available_network_tiers", []))

    def which_networks(self, name):
        details = self.provider_details(name)
        return details["available_network_tiers"] if details.get("found", False) else []

    def answer_query(self, query):
        provider, network_col = self.extract_provider_and_network_from_query(query)
        norm_provider = self._normalize(provider)
        # Alias-based query (output hardening for Basic Plus only)
        if network_col:
            details = self.provider_in_network(provider, network_col)
            # Only harden output for Basic Plus
            if network_col == "hn_basic_plus":
                display_network = "HN Basic Plus network"
                prov_name = details.get("provider_name") or norm_provider
                prov_type = details.get("type", "")
                prov_city = details.get("city", "")
                if details.get("found"):
                    if details.get("in_network"):
                        extra = []
                        if prov_type:
                            extra.append(f"Type: {prov_type}.")
                        if prov_city:
                            extra.append(f"City: {prov_city}.")
                        extra_str = (" "+" ".join(extra)) if extra else ""
                        return f"[NETWORK] {prov_name} is in {display_network}.{extra_str}"
                    else:
                        return f"[NETWORK] {prov_name} is not in {display_network}."
                return "Provider not found."
            # All other alias-based queries (preserve old behavior, but do not leak internal label)
            if details.get("found"):
                display_network = network_col.replace("hn_", "HN ").replace("_", " ").title().strip()
                prov_name = details.get("provider_name") or norm_provider
                if details.get("in_network"):
                    return f"[NETWORK] {prov_name} is in {display_network}."
                else:
                    return f"[NETWORK] {prov_name} is not in {display_network}."
            return "Provider not found."
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
        # Find the provider row (allow ambiguous for test fixture)
        row = self.find_provider(provider_name)
        if row is None:
            return {"found": False}
        if isinstance(row, str) and row == 'ambiguous':
            return {"found": False, "ambiguous": True}
        # network_code must match a column
        col = network_code.lower()
        if col not in self.df.columns:
            return {"found": False}
        val = str(row[col]).strip() if col in row else ""
        val = unicodedata.normalize('NFKC', val)
        unavailable_values = ("", "-", "0", "x", "X", "✖", "✕", "✗", "no", "n", "false")
        available_values = ("✔", "✓", "yes", "y", "true", "1")
        in_network = val in available_values
        # available_network_tiers for this provider
        tiers = [c for c in self.network_tier_cols if str(row.get(c, "")).strip() in available_values]
        return {
            "found": True,
            "ambiguous": False,
            "provider_name": row.get("provider_name", ""),
            "google_name": row.get("google_name", ""),
            "city": row.get("city", ""),
            "type": row.get("type", ""),
            "network_code": network_code,
            "in_network": in_network,
            "available_network_tiers": tiers,
        }


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


def get_network_lookup():
    return NetworkLookup()
