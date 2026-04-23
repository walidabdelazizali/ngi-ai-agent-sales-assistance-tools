import pandas as pd
import re

def normalize(s):
    if not isinstance(s, str):
        s = str(s)
    s = s.strip().lower()
    s = re.sub(r"[؟?]$", "", s)
    s = re.sub(r"[\s\t\n\r]+", " ", s)
    s = re.sub(r"^[^\w\d]+|[^\w\d]+$", "", s)  # strip simple punctuation at ends
    s = re.sub(r"[\.,;:!\-\(\)\[\]{}'\"]", "", s)  # remove simple punctuation inside
    s = re.sub(r" +", " ", s)  # collapse multiple spaces
    return s

df = pd.read_csv('runtime_data/networks/network_list_normalized.csv', dtype=str, encoding='utf-8-sig').fillna("")
norm_key = normalize('AL FARHAN MEDICAL LABORATORY - L L C')
matches = df[df['provider_name'].apply(normalize) == norm_key]
print(matches[['provider_name', 'hn_basic_plus']])
print(f'Total matches: {len(matches)}')
