
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
    def _cleanup_provider_query(query):
        """
        Remove common question phrases from provider queries for more robust matching.
        Only applies to 'Is ... in the network' and Arabic equivalents, not 'Which network ...'.
        """
        q = query.strip().lower()
        # Only strip for 'Is ... in the network' and Arabic equivalents
        # English: Is [PROVIDER] in the network?
        m = re.match(r"is\s+(.+?)\s+in the network", q)
        if m:
            return m.group(1).strip().title()
        # Arabic: هل [PROVIDER] داخل الشبكة؟
        m = re.match(r"هل\s+(.+?)\s+داخل الشبكة", q)
        if m:
            return m.group(1).strip().title()
        # Arabic: هل [PROVIDER] في الشبكة؟
        m = re.match(r"هل\s+(.+?)\s+في الشبكة", q)
        if m:
            return m.group(1).strip().title()
        # Otherwise, return original
        return query.strip()
    def list_basic_plus_providers(self, city=None, provider_type=None, lang="en", label_override=None):
        """
        List all providers in HN Basic Plus, optionally filtered by city and type.
        Applies normalization and mapping for city/type variants.
        lang: 'en' or 'ar' for output language.
        label_override: (city, type) for output heading, if provided.
        """
        available_values = ("✔", "✓", "yes", "y", "true", "1")
        df = self.df[self.df["hn_basic_plus"].apply(lambda v: str(v).strip() in available_values)]
        # --- City normalization ---
        if city:
            city_norm = city.strip().lower()
            # Accept variants: e.g., 'sharjah', 'al sharjah', etc.
            def city_match(val):
                v = str(val).strip().lower()
                return city_norm in v or v in city_norm
            df = df[df["city"].apply(city_match)]
        # --- Type normalization and mapping ---
        if provider_type:
            type_norm = provider_type.strip().lower()
            # Map type to possible variants in data
            type_map = {
                "clinic": ["clinic", "medical center"],
                "clinics": ["clinic", "medical center"],
                "medical center": ["medical center", "clinic"],
                "hospital": ["hospital"],
                "hospitals": ["hospital"],
                "lab": ["diagnostic center", "laboratory"],
                "labs": ["diagnostic center", "laboratory"],
                "diagnostic center": ["diagnostic center", "laboratory"],
                "diagnostic centers": ["diagnostic center", "laboratory"],
                "pharmacy": ["pharmacy"],
                "pharmacies": ["pharmacy"],
            }
            mapped_types = type_map.get(type_norm, [type_norm])
            def type_match(val):
                v = str(val).strip().lower()
                return any(mt in v or v in mt for mt in mapped_types)
            df = df[df["type"].apply(type_match)]
        if df.empty:
            if lang == "ar":
                return "[NETWORK]\nلا يوجد مزودون مطابقون للمعايير المحددة في شبكة HN Basic Plus."
            else:
                return "[NETWORK]\nNo matching providers found in HN Basic Plus network."
        # Format output: return all matching providers (no truncation)
        lines = []
        for _, row in df.iterrows():
            name = row.get("provider_name", "")
            lines.append(f"- {name}")
        # Heading
        if label_override:
            city_disp, type_disp = label_override
        else:
            city_disp = city or ""
            type_disp = provider_type or ""
        if lang == "ar":
            heading = f"[NETWORK]\n{type_disp}{city_disp and ' ' + city_disp} (HN Basic Plus):"
        else:
            heading = f"[NETWORK]\n{city_disp} {type_disp}(s) (HN Basic Plus):".replace("  ", " ").replace("(s)s", "s")
        return heading + "\n" + "\n".join(lines)
    @staticmethod
    def extract_provider_from_query(query):
        q = query.strip()
        # 1. Which network tiers is X available in?
        m = re.match(r"^which network tiers is (.+) available in\??$", q, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        # 2. Which network is X available in?
        m = re.match(r"^which network is (.+) available in\??$", q, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        # 3. What city is X located in?
        m = re.match(r"^what city is (.+) located in\??$", q, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        # 4. What type of provider is X?
        m = re.match(r"^what type of provider is (.+)\??$", q, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        # 5. Which network X?
        m = re.match(r"^which network (.+)\??$", q, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        # Otherwise, use cleanup helper
        return NetworkLookup._cleanup_provider_query(query)
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
        # Arabic: هل [PROVIDER] في الشبكة؟
        m = re.match(r"هل\s+(.+?)\s+في الشبكة", q)
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

        # 2.5: Try stripping trailing city if present and retry
        city_list = set(self.df["city"].dropna().str.lower().unique())
        norm_parts = norm.split()
        if len(norm_parts) > 2:
            # Try removing last word if it matches a city
            if norm_parts[-1] in city_list:
                norm_city_stripped = " ".join(norm_parts[:-1])
                if norm_city_stripped in self.provider_name_idx:
                    idxs = self.provider_name_idx[norm_city_stripped]
                    if len(idxs) == 1:
                        return self.df.iloc[idxs[0]]
                    return 'ambiguous' if len(idxs) > 1 else None

        # --- Multi-word entity safe matching ---
        # Known generic words to exclude as sole match
        known_types = {"hospital", "pharmacy", "clinic", "medical", "center", "centre"}
        known_cities = set(self.df["city"].dropna().str.lower().unique())
        norm_tokens = norm.split()
        # Build all n-grams (phrases) from the query, longest to shortest
        ngrams = []
        for n in range(len(norm_tokens), 0, -1):
            for i in range(len(norm_tokens) - n + 1):
                phrase = " ".join(norm_tokens[i:i+n])
                ngrams.append(phrase)
        matches = []
        for idx, row in self.df.iterrows():
            pn = self._normalize(row.get("provider_name", ""))
            gn = self._normalize(row.get("google_name", ""))
            row_type = str(row.get("type", "")).lower()
            row_city = str(row.get("city", "")).lower()
            # Only match if overlap is not a generic type word
            for phrase in ngrams:
                if phrase in known_types or phrase in known_cities:
                    continue
                # Accept if provider_name is a word-bound substring of query, or vice versa
                if (f" {pn} " in f" {norm} " or f" {norm} " in f" {pn} ") or (f" {gn} " in f" {norm} " or f" {norm} " in f" {gn} "):
                    matches.append(idx)
                    break
        # If no matches, fallback to unique_contains_fallback logic (for test coverage)
        if not matches:
            for idx, row in self.df.iterrows():
                pn = self._normalize(row.get("provider_name", ""))
                if norm in pn:
                    matches.append(idx)
        # If still no matches, not found
        if not matches:
            return None
        # If type is in query, filter by type
        type_token = None
        for t in norm_tokens:
            if t in known_types:
                type_token = t
                break
        if type_token:
            matches = [i for i in matches if type_token in str(self.df.iloc[i].get("type", "")).lower()]
            if not matches:
                return None
        # If city is in query, filter by city
        city_token = None
        for t in norm_tokens:
            if t in known_cities:
                city_token = t
                break
        if city_token:
            matches = [i for i in matches if city_token in str(self.df.iloc[i].get("city", "")).lower()]
            if not matches:
                return None
        # Final decision
        if len(matches) == 1:
            return self.df.iloc[matches[0]]
        if len(matches) > 1:
            return 'ambiguous'
        return None
        # 4. substring/contains match in google_name only
        google_matches = []
        for idx, row in self.df.iterrows():
            gn = self._normalize(row.get("google_name", ""))
            if norm in gn:
                google_matches.append(idx)
        if len(google_matches) == 1:
            return self.df.iloc[google_matches[0]]
        if len(google_matches) > 1:
            return 'ambiguous'
        return None

    def is_in_network(self, name):
        details = self.provider_details(name)
        return details.get("found", False) and bool(details.get("available_network_tiers", []))

    def which_networks(self, name):
        details = self.provider_details(name)
        return details["available_network_tiers"] if details.get("found", False) else []

    def answer_query(self, query):
        q = query.strip().lower()
        # General English city+type queries (HN Basic Plus only)
        en_city_map = {"abu dhabi": "Abu Dhabi", "dubai": "Dubai", "sharjah": "Sharjah", "ajman": "Ajman"}
        en_type_map = {
            "hospitals": "Hospital", "hospital": "Hospital",
            "clinics": "Clinic", "clinic": "Clinic",
            "labs": "Diagnostic Center", "lab": "Diagnostic Center",
            "diagnostic centers": "Diagnostic Center", "diagnostic center": "Diagnostic Center"
        }
        for city_key, city_val in en_city_map.items():
            for type_key, type_val in en_type_map.items():
                # e.g. "show hospitals in sharjah", "clinics in dubai", "labs in ajman"
                if re.fullmatch(rf"(show )?{type_key} in {city_key}", q):
                    return self.list_basic_plus_providers(city=city_val, provider_type=type_val, lang="en", label_override=(city_val, type_val+"s"))
        # General Arabic city+type queries (HN Basic Plus only)
        ar_city_map = {"ابوظبي": "Abu Dhabi", "أبوظبي": "Abu Dhabi", "دبي": "Dubai", "الشارقة": "Sharjah", "عجمان": "Ajman"}
        ar_type_map = {
            "مستشفيات": ("Hospital", "مستشفيات"),
            "عيادات": ("Clinic", "عيادات"),
            "مراكز": ("Medical Center", "مراكز"),
            "تحاليل": ("Diagnostic Center", "تحاليل"),
            "مراكز أشعة": ("Diagnostic Center", "مراكز أشعة")
        }
        for city_key, city_val in ar_city_map.items():
            for type_key, (type_val, type_disp) in ar_type_map.items():
                # e.g. "هاتلي مستشفيات في الشارقة", "عيادات في دبي", "تحاليل في عجمان", "مراكز أشعة في أبوظبي"
                if re.fullmatch(rf"(هاتلي )?{type_key} في {city_key}", q):
                    return self.list_basic_plus_providers(city=city_val, provider_type=type_val, lang="ar", label_override=(city_key, type_disp))
        # City+type listing for HN Basic Plus (English, legacy pattern)
        m = re.match(r"list (hospitals|clinics|labs|pharmacies|medical centers?) in ([a-zA-Z\s]+) (?:in )?basic plus", query.strip(), re.IGNORECASE)
        if m:
            ptype = m.group(1).rstrip('s').title()
            city = m.group(2).strip().title()
            return self.list_basic_plus_providers(city=city, provider_type=ptype, lang="en", label_override=(city, ptype+"s"))
        # City+type listing for HN Basic Plus (Arabic, legacy pattern)
        m = re.match(r"اعرض (مستشفيات|عيادات|مختبرات|صيدليات|مراكز طبية) في ([^\s]+) (?:في )?بيسك بلس", query.strip())
        if m:
            ar_type = m.group(1)
            city = m.group(2)
            type_map = {"مستشفيات": "Hospital", "عيادات": "Clinic", "مختبرات": "Diagnostic Center", "صيدليات": "Pharmacy", "مراكز طبية": "Medical Center"}
            ptype = type_map.get(ar_type, "")
            return self.list_basic_plus_providers(city=city, provider_type=ptype, lang="ar", label_override=(city, ar_type))
        # ...existing code...
        provider, network_col = self.extract_provider_and_network_from_query(query)
        norm_provider = self._normalize(provider)
        # Alias-based query (output hardening for Basic Plus only)
        if network_col:
            details = self.provider_in_network(provider, network_col)
            # Only harden output for Basic Plus
            if network_col == "hn_basic_plus":
                display_network_en = "HN Basic Plus network"
                display_network_ar = "شبكة HN Basic Plus"
                prov_name = details.get("provider_name") or norm_provider
                prov_type = details.get("type", "")
                prov_city = details.get("city", "")
                # Detect Arabic query (simple heuristic: Arabic letters or known Arabic phrases)
                is_arabic = bool(re.search(r"[\u0600-\u06FF]", query))
                if details.get("found"):
                    if details.get("in_network"):
                        if is_arabic:
                            extra = []
                            if prov_type:
                                extra.append(f"النوع: {prov_type}.")
                            if prov_city:
                                extra.append(f"المدينة: {prov_city}.")
                            extra_str = (" "+" ".join(extra)) if extra else ""
                            return f"[NETWORK] المزود {prov_name} داخل {display_network_ar}.{extra_str}"
                        else:
                            extra = []
                            if prov_type:
                                extra.append(f"Type: {prov_type}.")
                            if prov_city:
                                extra.append(f"City: {prov_city}.")
                            extra_str = (" "+" ".join(extra)) if extra else ""
                            return f"[NETWORK] {prov_name} is in {display_network_en}.{extra_str}"
                    else:
                        if is_arabic:
                            return f"[NETWORK] المزود {prov_name} غير موجود داخل {display_network_ar}."
                        else:
                            return f"[NETWORK] {prov_name} is not in {display_network_en}."
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
        # in network? (English or Arabic generic)
        if re.search(r"is .+ in the network|هل .+ داخل الشبكة|هل .+ في الشبكة", query, re.IGNORECASE):
            found = self.is_in_network(provider)
            return f"YES: {norm_provider}" if found else f"NO: {norm_provider}"

        # Minimal patch: handle network tiers, city, and type queries
        extracted_provider = self.extract_provider_from_query(query)
        row = self.find_provider(extracted_provider)
        if isinstance(row, pd.Series):
            # 1. Which network tiers is X available in?
            if re.search(r"which network tiers is .+ available in", query, re.IGNORECASE):
                tiers = []
                for col in self.network_tier_cols:
                    val = row.get(col, "")
                    if val and str(val).strip().lower() not in ("no", "0", "", "false", "n/a"):
                        tiers.append(f"{col}: {val}")
                return f"Network tiers for {extracted_provider}: {', '.join(tiers) if tiers else 'None'}"
            # 2. What city is X located in?
            if re.search(r"what city is .+ located in", query, re.IGNORECASE):
                city = row.get("city", "")
                return f"City for {extracted_provider}: {city if city else 'Unknown'}"
            # 3. What type of provider is X?
            if re.search(r"what type of provider is .+\??$", query, re.IGNORECASE):
                ptype = row.get("type", "")
                return f"Type for {extracted_provider}: {ptype if ptype else 'Unknown'}"

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
