# Real Usage Evidence Pack (100 Questions)

## Run Context
- Mode: REAL USAGE EVIDENCE PACK (after normalization sprint)
- Execution path: `python -m src.agent_entrypoint --json <query>`
- Scope: evidence only

## Evaluation Set Composition
- plan_summary_benefit: 20
- network_provider_lookup: 30
- comparison_questions: 20
- recommendation_questions: 10
- arabic_mixed_questions: 20
- total: 100

## Summary
- total GOOD: 63
- total REVIEW: 19
- total BLOCKED_OK: 13
- total GAP: 5

## Detailed Results

### plan_summary_benefit
#### 1. Summarize Classic 2
- intent: plan_summary
- tool: get_plan_summary
- plan: Classic 2
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 2
Code: HN_CLASSIC_2
Network: Standard Plus
Annual limit: AED 250,000
Area: Worldwide Excluding USA and Canada
Direct billing: Yes
Referral required: No
```
#### 2. Summarize Classic 2R
- intent: plan_summary
- tool: get_plan_summary
- plan: Classic 2R
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 2R
Code: HN_CLASSIC_2R
Network: Standard Plus
Annual limit: AED 250,000
Area: Worldwide Excluding USA and Canada
Direct billing: Yes
Referral required: No
```
#### 3. Summarize Classic 3
- intent: plan_summary
- tool: get_plan_summary
- plan: Classic 3
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 3
Code: HN_CLASSIC_3
Network: Standard
Annual limit: AED 250,000
Area: UAE+Home country
Direct billing: Yes
Referral required: No
```
#### 4. What is the annual limit for Classic 3?
- intent: plan_core
- tool: get_plan_core
- plan: Classic 3
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 3
Code: HN_CLASSIC_3
الشبكة: Standard
Annual limit: AED 250,000
Area: UAE+Home country
Direct billing: Yes
Referral required: No
```
#### 5. Does Classic 2 require referral?
- intent: unsupported
- tool: None
- plan: None
- classification: REVIEW
- reason: Unsupported phrasing or out-of-scope query needs triage.
- output:
```text
Sorry, this query is not supported or not available. Please specify a supported plan or question.
```
#### 6. What is the area of coverage for Classic 2R?
- intent: plan_core
- tool: get_plan_core
- plan: Classic 2R
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 2R
Code: HN_CLASSIC_2R
الشبكة: Standard Plus
Annual limit: AED 250,000
Area: Worldwide Excluding USA and Canada
Direct billing: Yes
Referral required: No
```
#### 7. classic2r cashless?
- intent: plan_core
- tool: get_plan_core
- plan: Classic 2R
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 2R
Code: HN_CLASSIC_2R
الشبكة: Standard Plus
Annual limit: AED 250,000
Area: Worldwide Excluding USA and Canada
Direct billing: Yes
Referral required: No
```
#### 8. Give me a summary of Remedy 04
- intent: plan_summary
- tool: get_plan_summary
- plan: Remedy 04
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: NGI Healthnet –Remedy 04
Code: HN-REMEDY 4
Network: HN Basic Plus (OP Restricted to Clinics) with direct access to below hospitals for OP Services. Aster Hospitals (Qusais, Mankhool, Jebel Ali) Burjeel Specialty Hospital Sharjah International Modern Hospital, DXB Ajman Specialty Hospital – Ajman Al Saha wa Al Shifaa Hospital For One Day Surgery – Sharjah Specialist Subject to GP Referral both in Clinics and Hospitals
Annual limit: AED. 150,000
Area: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval.
Direct billing: Yes
Referral required: Yes
```
#### 9. What is the annual limit for Remedy 05?
- intent: plan_core
- tool: get_plan_core
- plan: Remedy 05
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: NGI Healthnet –Remedy 05
Code: HN-REMEDY-5
الشبكة: HN Basic Plus
Annual limit: AED. 150,000
Area: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval.
Direct billing: Yes
Referral required: No
```
#### 10. What are the reimbursement rules for Remedy 05?
- intent: reimbursement_rules
- tool: get_reimbursement_rules
- plan: Remedy 05
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Reimbursement allowed: Yes.
Outside network reimbursement: Emergency Medical Treatment within the UAE.
Outside UAE reimbursement: Eligible claims incurred outside UAE within territory of cover is covered on 100% reimbursement basis based on UCR charges of UAE designated network rates or 100% incurred claims cost whichever is lower..
Basis: UCR charges of UAE designated network rates or 100% incurred claims cost, whichever is lower..
Conditions: Claims must be incurred within the territory of cover; reimbursement is limited to UAE designated network UCR or incurred cost, whichever is lower..
```
#### 11. maternity Classic 3
- intent: unsupported
- tool: None
- plan: Classic 3
- classification: GAP
- reason: Benefit data exists in source but intentionally not exposed in runtime.
- output:
```text
Sorry, this query is not supported or not available. Please specify a supported plan or question.
```
#### 12. pharmacy Classic 2R
- intent: unsupported
- tool: None
- plan: Classic 2R
- classification: GAP
- reason: Benefit data exists in source but intentionally not exposed in runtime.
- output:
```text
Sorry, this query is not supported or not available. Please specify a supported plan or question.
```
#### 13. Is there private room coverage for Classic 2R?
- intent: unsupported
- tool: None
- plan: Classic 2R
- classification: GAP
- reason: Benefit data exists in source but intentionally not exposed in runtime.
- output:
```text
Sorry, this query is not supported or not available. Please specify a supported plan or question.
```
#### 14. هل يغطي الطوارئ في كلاسيك 2R؟
- intent: unsupported
- tool: None
- plan: Classic 2R
- classification: GAP
- reason: Benefit data exists in source but intentionally not exposed in runtime.
- output:
```text
عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم.
```
#### 15. هل فيه كاشلس في كلاسيك 3؟
- intent: plan_core
- tool: get_plan_core
- plan: Classic 3
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 3
Code: HN_CLASSIC_3
الشبكة: Standard
Annual limit: AED 250,000
Area: UAE+Home country
Direct billing: Yes
Referral required: No
```
#### 16. ملخص كلاسيك 3
- intent: plan_summary
- tool: get_plan_summary
- plan: Classic 3
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 3
Code: HN_CLASSIC_3
Network: Standard
Annual limit: AED 250,000
Area: UAE+Home country
Direct billing: Yes
Referral required: No
```
#### 17. ملخص كلاسيك 2
- intent: plan_summary
- tool: get_plan_summary
- plan: Classic 2
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 2
Code: HN_CLASSIC_2
Network: Standard Plus
Annual limit: AED 250,000
Area: Worldwide Excluding USA and Canada
Direct billing: Yes
Referral required: No
```
#### 18. ما هو الحد السنوي ل Classic 3
- intent: plan_core
- tool: get_plan_core
- plan: Classic 3
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 3
Code: HN_CLASSIC_3
الشبكة: Standard
Annual limit: AED 250,000
Area: UAE+Home country
Direct billing: Yes
Referral required: No
```
#### 19. هل Classic 2 يحتاج referral
- intent: plan_core
- tool: get_plan_core
- plan: Classic 2
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 2
Code: HN_CLASSIC_2
الشبكة: Standard Plus
Annual limit: AED 250,000
Area: Worldwide Excluding USA and Canada
Direct billing: Yes
Referral required: No
```
#### 20. What is the network name for Classic 2R?
- intent: plan_core
- tool: get_plan_core
- plan: Classic 2R
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 2R
Code: HN_CLASSIC_2R
الشبكة: Standard Plus
Annual limit: AED 250,000
Area: Worldwide Excluding USA and Canada
Direct billing: Yes
Referral required: No
```

### network_provider_lookup
#### 21. Is Burjeel Hospital in the network?
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
YES: burjeel hospital
```
#### 22. Is Burjeel Abu Dhabi in the network?
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
YES: burjeel abu dhabi
```
#### 23. Is Accuracy Plus Medical Laboratory in the network?
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
YES: accuracy plus medical laboratory
```
#### 24. Is Aster Qusais in the network?
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
YES: aster qusais
```
#### 25. Which network tiers is Burjeel Hospital available in?
- intent: error
- tool: None
- plan: None
- classification: REVIEW
- reason: Runtime parsing/handling error requires deterministic guard.
- output:
```text
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Projects\NGI-AI-AGENT-SALES-ASSISTANCE-TOOLS\src\agent_entrypoint.py", line 39, in <module>
    main()
  File "C:\Projects\NGI-AI-AGENT-SALES-ASSISTANCE-TOOLS\src\agent_entrypoint.py", line 26, in main
    print(json.dumps(result, ensure_ascii=False, indent=2))
  File "C:\Users\H Dos\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1256.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2714' in position 186: character maps to <undefined>
```
#### 26. Which network tiers for Burjeel Hospital?
- intent: error
- tool: None
- plan: None
- classification: REVIEW
- reason: Runtime parsing/handling error requires deterministic guard.
- output:
```text
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Projects\NGI-AI-AGENT-SALES-ASSISTANCE-TOOLS\src\agent_entrypoint.py", line 39, in <module>
    main()
  File "C:\Projects\NGI-AI-AGENT-SALES-ASSISTANCE-TOOLS\src\agent_entrypoint.py", line 26, in main
    print(json.dumps(result, ensure_ascii=False, indent=2))
  File "C:\Users\H Dos\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1256.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2714' in position 186: character maps to <undefined>
```
#### 27. What city is Burjeel Hospital located in?
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
City for Burjeel Hospital: ABU DHABI
```
#### 28. What city for Burjeel Hospital?
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
City for Burjeel Hospital: ABU DHABI
```
#### 29. What type of provider is Burjeel Hospital?
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Type for Burjeel Hospital: HOSPITAL
```
#### 30. What type is Burjeel Hospital?
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Type for Burjeel Hospital: HOSPITAL
```
#### 31. Burjeel Hospital in which network?
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Networks for Burjeel Hospital: hn_exclusive, hn_premier
```
#### 32. Is Burjeel Hospital Abu Dhabi in Basic Plus?
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
[NETWORK] BURJEEL HOSPITAL is not in HN Basic Plus network.
```
#### 33. Is Unknown Future Hospital in Basic Plus?
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: REVIEW
- reason: Provider lookup failed; likely alias/coverage limitation.
- output:
```text
Provider not found.
```
#### 34. show hospitals in sharjah
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
[NETWORK]
Sharjah Hospitals(s) (HN Basic Plus):
- AL NAKHEEL ONE DAY SURGERY HOSPITAL
- AL SAHA WA AL SHIFAA HOSPITAL FOR ONE DAY SURGERY
- BURJEEL SPECIALTY HOSPITAL LLC- SHARJAH
- CENTRAL HOSPITAL LLC( EX: Central Private Hospital)
- EMIRATES EUROPEAN HOSPITAL LLC ONE DAY SURGERY
- ORIANA HOSPITAL FOR ONE DAY SURGERY
- ROYAL HOSPITAL
- THUMBAY HOSPITAL DAYCARE - MUWAILAH
```
#### 35. show hospitals in dubai
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
[NETWORK]
Dubai Hospitals(s) (HN Basic Plus):
- ASTER DAY SURGERY CENTRE LLC
- ASTER HOSPITAL BR OF ASTER DM HEALTHCARE FZC- Al Qusais
- ASTER HOSPITAL- Mankhool
- ASTER HOSPITAL SONAPUR
- CEDARS JEBEL ALI INTERNATIONAL HOSPITAL
- DUBAI MEDICAL UNIVERSITY HOSPITAL
- HATTA HOSPITAL
- INTERNATIONAL MODERN HOSPITAL
- MEDEOR 24X7 HOSPITAL LLC
- MEDSTAR HEALTHCARE LLC
- MYHEALTH  DAY SURGICAL CENTER LLC
- NMC ROYAL HOSPITAL LLC(DXB)
- NMC SPECIALTY HOSPITAL - DXB
- NMC SPECIALTY HOSPITAL DIP (Br of N M C ROYAL HOSPITAL LTD) (Dubai Branch)
- JEBEL ALI EMERGENCY AND TRAUMA CENTER
- ARMADA ONE DAY SURGICAL CENTER DMCC
```
#### 36. show labs in abu dhabi
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
[NETWORK]
Abu Dhabi Diagnostic Centers(s) (HN Basic Plus):
- ACCURACY PLUS MEDICAL LABORATORY
- AL BORG DIAGNOSTIC CENTRE FOR LABORATORIES L.L.C.
- AL FARHAN MEDICAL LABORATORY - L L C
- Dar Al Mouasah Diagnostic Centre
- IDEAL CLINICAL LABORATORIES
- MENA LABS MEDICAL LABORATORY LLC
- PROFICIENCY SPECIALIST LABORATORIES
- QUALITY DIAGNOSTIC LABORATORY L.L.C
- THE OPEN MRI CENTER -LLC
- UNILABS DIAGNOSTICS L.L.C
- SANIMED INTERNATIONAL LAB AND MANAGEMENT L.L.C.
```
#### 37. show clinics in dubai
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
[NETWORK]
Dubai Clinics(s) (HN Basic Plus):
- DR. ISMAIL DAY SURGICAL CENTRE
- ABBARA POLYCLINIC
- ABEER AL NOOR POLY CLINIC LLC BRANCH
- ABRIS MEDICAL CENTRE LLC
- ABSOLUTE WELLNESS MEDICAL CENTRE
- ACCESS CLINIC ALQUOZ
- ACCESS CLINIC BUR DUBAI
- ACCESS CLINIC DIC BR DM HEALTHCARE LLC
- ACCESS CLINIC DIP
- ACCESS CLINIC DIP 2 BR OF DM HEALTHCARE LLC
- ACCESS CLINIC FREEZONE
- ACCESS CLINIC INTERNATIONAL CITY
- ACCESS CLINIC PERSIA CLUSTER
- ACCESS CLINIC SONAPUR
- ACCESS CLINIC SONAPUR 2 BR OF DM HEALTHCARE LLC (EX. AFIF MEDICAL CENTER)
- ADVANCED CARE MEDICAL CENTER
- ADVANCED CARE MEDICAL CENTER  LLC (BRANCH)
- ADVANCED CARE MEDICAL CENTER BRANCH
- ADVANCED CARE MEDICAL CENTER LLC (BRANCH)
- ADVANCED CARE MEDICAL CENTER LLC BRANCH
- ADVANCED CARE MEDICAL CENTER LLC BRANCH-GRAND CITY MALL
- ADVANCED CARE MEDICAL CENTRE L.L.C (BRANCH )- DIP 1
- AL ABRAH CLINIC
- AL AMAL POLYCLINIC
- AL AMAN MEDICAL CENTER
- AL AZHAR CLINIC
- AL AZHAR CLINIC BR DIP 2
- AL AZHAR CLINIC BRANCH
- Al Azhar Clinic Branch 3
- Al Azhar Clinic LLC 4
- AL DHAFRA MEDICAL CENTRE
- Al Fahim Clinic
- AL FALAH MEDICAL CLINIC
- AL HANA MEDICAL CENTER LLC
- AL HANA MODERN MEDICAL CENTER LLC
- AL KHAIL MEDICAL CENTER
- AL KHAIL MEDICAL CENTRE BRANCH
- AL MASHAHER MEDICAL CENTRE
- AL MURJAN MEDICAL CENTER
- AL NOOR POLYCLINIC - BR OF GHI AL SATWA
- AL NOOR POLYCLINIC - BR OF GHI DEIRA
- AL NOOR POLYCLINIC BR OF GHI AL RIGGA (AMBER)
- WELLCARE ADVANCED POLY CLINIC L.L.C (EX. AL QUOZ CITY STAR POLYCLINIC)
- AL QUSAIS STAR POLYCLINIC
- SONAPUR STAR POLYCLINIC L.L.C (EX. AL QUSAIS STAR POLYCLINIC (BRANCH))
- AL RASHIDIYAH AL NOOR POLYCLINIC
- AL SANAIYA MEDICAL CLINIC
- AL SANAIYA MEDICAL CLINIC-BRANCH
- AL SHAAB MEDICAL CENTRE
- AL SHIFA AL KHALEEJI MEDICAL CENTER
- Al Shifa Al Khaleeji Medical Centre Branch LLC-DIP
- AL SHIFA INTERNATIONAL CLINIC
- AL SHIFA INTERNATIONAL CLINIC LLC- BRANCH
- AL TADAWI MEDICAL CENTRE
- AL TAIF MEDICAL CENTER
- AL WAHA CLINIC
- ALDIA MEDICAL CENTER L.L.C
- ALHABAB GENERAL CLINIC
- ALI MEDICAL CLINIC
- AMALA MEDICAL CENTRE
- AMIRUDDIN CLINIC
- ANAYA MEDICAL CENTER LLC
- ANAYA MEDICAL CENTER LLC BRANCH
- APPLE CLINIC
- APPLE INTERNATIONAL POLY CLINIC
- ARIN CARE POLYCLINIC L.L.C
- ASH TREE CLINIC LLC
- ASHOKAN MEDICAL CLINIC
- ASTER CEDARS CLINIC
- ASTER JABAL ALI MEDICAL CENTRE
- Aster Medical Centre Oud Metha (Br Of D M Healthcare LLC)
- ASTER MEDICAL CENTRE ABU HAIL BR OF DM HEALTHCARE
- ASTER MEDICAL CENTRE AL QUSAIS
- ASTER MEDICAL CENTRE DUBAI LAND
- ASTER MEDICAL CENTRE INTERNATIONAL CITY(Gynaecology and Paediatrics services only)
- ASTER MEDICAL CENTRE REMRAAM (BR OF D M HEALTHCARE)
- BADR AL SAMAA MEDICAL CENTER
- BEST HEALTH MEDICAL CENTER L.L.C
- BIO VISTA MEDICAL CENTRE LLC
- BLUE BELL MEDICAL CENTRE
- BRIGHT LIFE MEDICAL CENTER LLC
- CARE AND CURE MEDICAL CENTER L.L.C
- CARE ONE POLY CLINIC LLC
- CARE PLUS MEDICAL CENTER
- CLINICARE BR OF IMARA HEALTH CARE LLC
- CLINICARE SAMARI BR OF IMARA HEALTH CARE LLC
- COMMUNITY MEDICAL CENTRE
- COSMOPOLITAN MEDICAL CENTRE
- DOCIB CLINIC LLC
- DOCTORS CLINIC
- DOCTORS CLINIC DIAGNOSTIC CENTRE FZ-LLC
- DR. IBRAHIM ABBARA CLINIC
- DR. ISMAIL MEDICAL CENTRE - AL MUHAISANAH
- DR. ISMAIL MEDICAL CENTRE - AL QUOZ
- DR. ISMAIL POLYCLINIC BRANCH-DISCOVERY GARDEN
- DR. ISMAIL POLYCLINIC BRANCH-JEBEL ALI
- DR. ISMAIL POLYCLINIC KARAMA
- DR. JOHN CLINIC
- DR. JOSEPH’S POLYCLINIC-KARAMA BR OF GHI
- DR. KAMKAR MEDICAL & PHYSIOTHERAPY CENTRE
- DR. KOYA CLINIC
- DR. MOOPENS' AL QUOZ MEDICAL CENTRE
- DR. MOOPEN'S MEDICAL CENTER - KARAMA
- DR. MUHAMMED KUNHI MEDICAL CLINIC
- DR. RADAKRISHNAN MEDICAL CENTRE
- DR. SANJAY MEDICAL CENTER - DUBAI
- DR. SHANIL MEDICAL CENTRE LLC
- DR.ABDULLAS CLINIC
- DULSCO MEDICAL CLINIC
- DULSCO MEDICAL CLINIC BRANCH
- DURRAIYA KAMAL MEDICAL CLINIC
- EXCEL HEALTHCARE ICARE CLINICS DISCOVERY GARDEN
- FAITH JABAL MEDICAL CENTER L.L.C
- FALCON MEDICAL CLINIC
- FAMILY CLINIC
- FIRST MEDICAL CENTRE
- FULLCARE MEDICAL CENTER
- Globehealth General Clinic  LLC
- GOODWILL CLINIC LLC
- GRAND INFINITY MEDICAL CENTER LLC
- GRAND INFINITY MEDICAL CENTER LLC BRANCH
- GREEN CITY MEDICAL CENTER L.L.C. (EX: NEW AL MUSALLA MEDICAL CENTER BRANCH)
- HARLEY INTERNATIONAL MEDICAL CLINIC
- HARLEY INTERNATIONAL MEDICAL CLINIC (BRANCH)
- Harley International Medical Clinic LLC Branch
- HOPECARE POLYCLINIC L.L.C
- HOUSTON MEDICAL CLINIC LLC
- HOUSTON MEDICAL CLINIC LLC (Branch)
- HTK Medical Centre
- ICARE ALREFFA BR OF EXCEL HEALTHCARE LLC
- ICARE OASIS BRANCH OF EXCEL HEALTHCARE
- Islamabad Medical Clinic LLC( Ex: Globe HealthPolyclinic)
- JANSON MEDICAL CLINIC
- JOSEPH'S QUSAIS POLYCLINIC
- JUPITER AL NAHDA POLYCLINIC
- JUPITER AL QUSAIS POLYCLINIC
- JUPITER SPECIALTY MEDICAL CENTER
- KARAMA MEDICAL CENTER - DIP BRANCH
- KARAMA MEDICAL CENTER AL QUOZ MALL BRANCH
- KARAMA MEDICAL CENTRE
- KARAMA MEDICAL CENTRE - AL QUOZ BRANCH
- KARAMA MEDICAL CENTRE BR  JV
- KARAMA MEDICAL CENTRE BR, BURJUMAN
- KARAMA MEDICAL CENTRE BR. AL KHAIL GATE
- KARAMA MEDICAL CENTRE BR. MUHAISNAH
- KEERTHI MEDICAL CENTER (PREVIOUSLY DR. KEERTHI CLINIC)
- KHALIDHA MEDICAL CENTRE LLC
- KIMS MEDICAL CENTRE
- KINGS MEDICAL CENTER LLC
- LAVERA CLINIC LLC
- LIFEGUARD GENERAL CLINIC L.L.C (EX. OUR CARE AND CURE MEDICAL CENTER LLC )
- LIFENITY INTERNATIONAL ADVANCED POLY CLINIC L.L.C
- LIFENITY INTERNATIONAL ADVANCED POLY CLINIC L.L.C (BRANCH)
- LIVE CARE CLINIC LLC
- LOTUS MEDICAL CENTER
- MAG Health Clinic
- MARHABA MEDICAL CENTER-DXB
- MATHEW MEDICAL CLINIC LLC
- MED ONE MEDICAL CENTER LLC (EX. AQUA MEDICAL CENTER)
- Medi Family Polyclinic FZE
- MEDICURE CENTRE
- MEDICURE CENTRE BRANCH
- Medicure Polyclinic L.L.C Branch- Al Manara
- MEDILIFE POLYCLINIC LLC
- MEDILITE MEDICAL CENTRE
- MEDZE CLINIC LLC
- MID EAST POLY CLINIC
- Miracure Medical Centre  LLC
- Mobile Home Healthcare Services LLC
- MUHAISNA SPECIALIST MEDICAL CENTRE LLC
- MULTI CARE MEDICAL CENTRE
- MVR DIAGNOSTIC CLINIC L.L.C (EX. MVR Medical Center)
- NAIF MEDICAL CENTER LLC
- NASSER CLINIC
- NEW AL MUSALLA MEDICAL CENTER
- NEW APOLLO POLYCLINIC
- NEW EMIRATES MEDICAL CENTER
- NEW LOTUS MEDICAL CENTER
- NEW MEDICAL CENTER (Ex:Reena Beegum clinic branch)
- NEW MEDICAL CENTRE LLC
- NEW MEDILIFE MEDICAL CENTRE L.L.C
- NEW SANAIYA CLINIC
- NEW SANAIYA CLINIC BRANCH - HORALANZ
- NEW SANAIYA CLINIC BRANCH-DIP
- NMC DIC CLINIC AND PHARMACY BR OF NMC ROYAL HOSPITAL LTD DUBAI BRANCH
- NMC POLYCLINIC BRANCH OF NMC HOSPITAL LLC
- Noor Al Shefa Branch 3
- NOOR AL SHEFA CLINIC - JEBEL ALI MALL
- NOOR AL SHEFA CLINIC BRANCH - AL QUOZ
- NOOR AL SHEFA CLINIC BRANCH - RAS AL KHOR
- Noor Al Shefa Clinic Branch. 4
- NOVITAS CLINIC L.L.C BRANCH
- NOVITAS CLINIC LLC
- OXFORD MEDICAL CENTER
- PAKISTAN MEDICAL CENTER
- Paradise Plus Poly Clinic LLC
- PESHAWAR MEDICAL CENTRE- DUBAI
- PHYSIOVEDA MEDICAL CENTER L.L.C
- PHYSIOVEDA MEDICAL CENTER L.L.C (BRANCH)
- PRIME MEDICAL CENTER AL QUSAIS (BR OF PRIME MEDICAL CENTER LLC)
- PRIME MEDICAL CENTER DUBAI AIRPORT (BR OF PRIME MEDICAL CENTER LLC)
- PRIMECORP MEDICAL CENTER AL QUSAIS (BR OF PRIMECORP MEDICAL CENTER LLC)
- PRIMECORP MEDICAL CENTER AL WARSAN (BR OF PRIMECORP MEDICAL CENTER L.L.C)
- PRIMECORP MEDICAL CENTER ALQUOZ LLC BRANCH
- PRIMECORP MEDICAL CENTER DWC BR OF PRIMECORP MEDICAL CENTER LLC
- PRIMECORP MEDICAL CENTER L L C DIP BRANCH
- PRIMECORP MEDICAL CENTER LLC
- PRIMECORP MEDICAL CENTER LLC  JABAL ALI BRANCH
- QAMAR AL MADINA MEDICAL CENTER L.L.C
- RASHIDIYA PRIVATE POLYCLINIC
- Releaf Medical Centre (DIP)
- Releaf Medical Centre (J Mart)
- Releaf Medical Centre(Al Qouz 2)
- Releaf Medical Centre(Jabal Ali)
- REMEDY PLUS MEDICAL CLINIC LLC
- RIAZ MEDICAL CENTRE - DUBAI
- RUBY CLINIC
- SALEEM POLYCLINIC
- SHEIKH MANNA BIN HASHER AL MAKTOUM POLYCLINIC
- SIRAJUDEEN MEDICAL CENTER
- SYED SADIQ GENERAL PRACTITIONER CLINIC LLC
- THE DOCTORS HUB POLYCLINIC L.L.C (EX. DR. JOSEPH GHRAYEB POLYCLINIC)
- TORONTO MEDICAL CENTER LLC
- VCARE POLYCLINIC LLC
- VIDA CLINICS- BURDUBAI
- VIDA CLINICS LLC BRANCH-MUHAISANAH
- Zahrat Al Shefa Medical Centre LLC
- ZEN LIFE POLYCLINIC CO LLC
- ZIYATH ANSAR POLY CLINIC L.L.C
- CARE BLUE CLINIC FZCO
- DOHA PHARMACY EXPRESS CLINIC (GP CLINIC ONLY)
- HALA PHARMACY 13 EXPRESS CLINIC (GP CLINIC ONLY)
- JADAF LIFE PHARAMCY EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE AL QUSAIS PHARMACY EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE DWTC PHARMACY EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE MURAQABAT PHARMACY EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE PEARL PHARMACY EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE PHARMACY 16 EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE PHARMACY 25 EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE PHARMACY 74 EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE PHARMACY 77 EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE PHARMACY BARSHA SOUTH FOURTH EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE PHARMACY EXPRESS CLINIC (GP CLINIC ONLY)
- NATURES LIFE EXPRESS CLINIC LLC (GP CLINIC ONLY)
- NEW AL KANZ PHARAMCY BRANCH EXPRESS CLINIC (GP CLINIC ONLY)
- RAMADA LIFE EXPRESS CLINIC (GP CLINIC ONLY)
- ROYAL LIFE EXPRESS CLINIC (GP CLINIC ONLY)
- AXON MEDICA POLYCLINIC, BR. AXON MEDICA INVESTMENT MANAGEMENT L.L.C
- AXON MEDICA POLYCLINIC
- DR ISMAIL POLYCLINIC
MALL BR OF DR. ISMAIL
POLYCLINIC
- APOLLO CLINIC LLC (EX. NEW CITY CLINIC LLC)
- AXIOS HOME CARE SERVICES L.L.C
- Modern Family Clinic LLC
- LIFE PHARMACY 44 EXPRESS CLINIC (GP CLINIC ONLY)
- Evercare Medical Center
- FUTURE LIFE GENERAL MEDICAL CLINIC
- MODERN FAMILY CLINIC L.L.C (BRANCH)
- DR ABDUL LATIF CLINIC LLC
- LIFE PHARMACY 119 (BR OF LIFE PHARMACY L.L.C)
- LIFE PHARMACY 125 (BR OF LIFE PHARMACY L.L.C)
- LIVERPOOL MEDICAL CLINIC L.L.C
- YOUR CENTER POLY CLINIC L.L.C
- MODERN FAMILY CLINIC L.L.C (BRANCH)
- MBM SPECIALITY MEDICAL CENTER L.L.C
- NOOR AL AHALIA MEDICAL CENTER
- ALOKA EYE CLINIC LLC
- MEDCOME HEALTH CARE CENTER
- BRIGHT CARE CLINIC L.L.C
- G M G MEDICAL CENTER L.L.C
- KHAYBER MEDICAL CENTER
- ASCENT ENT SPECIALITY CENTRE LLC
- STEPS POLYCLINIC LLC
- DR. ISMAIL POLYCLINIC (BRANCH)
- SEHA AL NOOR CLINIC LLC
- Al Bayan Medical Center LLC
- ADVANCED CARE MEDICAL CENTER BRANCH LLC
- RALS HEALTHCARE (AL QUSAIS)  (EX. MINI VM POLYCLINIC)
- RALS HEALTHCARE BR OF ABD ULWAHED BIN SHABIB INVESTMENT GROUP L.L.C (JABAL ALI) DUBAI
- Oud Al Muteena Medical Center
- NOOM MEDICAL CLINIC L.L.C
- SHAMS AL AHALIA MEDICAL CENTER
- ZMC HEALTH CLINIC L.L.C
- GSM MEDICAL CENTRE LLC (BRANCH)
- GOOD LIFE MEDICAL CENTER L.L.C
- BLOOM PLUS POLY CLINIC L.L.C
- AL MARIFFA MEDICAL CENTER L.L.C (DUBAI)
- BEST LIFE GENERAL CLINIC L.L.C
- CALLADOC TELEHEALTH SERVICES L.L.C
- AFRIDI MEDICAL CENTER L.L.C
- SHARE AND CARE MEDICAL CENTER L L C
- ROYAL PHOENIX CLINIC L.L.C
- Life Pharmacy and Express Clinic FZ LLC
- Ferdows Medical Center L.L.C
- Peshawar Medical Center LLC (International City)
- Life Pharmacy 180 Express Clinic
- LIFE PHARMACY 173 BR OF LIFE PHARMACY (GENERAL CLINIC)
- MADAWAH HEALTHCARE CLINIC L.L.C
- SAFA ALNOOR POLYCLINIC LLC
- MUMTAZ AL NOOR EXPRESS PHARMACY CLINIC LLC
- GRAND DR ISMAIL POLYCLINIC L.L.C
- Pak Satwa Poly Clinic Co. LLC
- Nucleus Clinic LLC (DUBAI MARINA)
- MEDHUB MEDICAL CENTER L.L.C
- DYNAMIC LIFE CLINIC L.L.C
- DYNAMIC LIFE CLINIC LLC BRANCH
- IRIS DENTAL CLINIC LLC
- AL NOOR POLYCLINIC L.L.C (BRANCH)
- L L H MEDICAL CENTER L.L.C (BRANCH)
- Tadawi Health Care LLC (Branch) IMPZ
- Tadawi Health Care LLC (Branch) DIP
- LIFE PHARMACY 189 EXPRESS CLINIC
- ROYAL SABA MEDICAL CLINIC
- ROYAL SABA MEDICAL CLINIC PHARMACY
- JAVIDA MEDICAL CENTER L.L.C.
- ISLAMABAD MEDICAL CLINIC LLC BR
- CITY RELIEF EXPRESS CLINIC LLC
- CRX EXPRESS CLINIC LLC
- LIFE PHARMACY 190 EXPRESS CLINIC
- PARADISE PLUS POLY CLINIC L.L.C (BRANCH)
- CARE 7 MEDICAL CENTER L.L.C
- ARMADA MEDICAL CENTRE DMCC
- MEDHUB MEDICAL CENTER L.L.C(BRANCH)
- MOOPANS POLYCLINIC L.L.C
- ZAIN CURA MEDICAL CENTER L.L.C
- BETA STAR CLINIC L L C
- AL BARSHA AL NOOR POLYCLINIC LLC
```
#### 38. What hospitals are available in Sharjah for Remedy 6?
- intent: plan_network_city_type
- tool: list_basic_plus_providers
- plan: Remedy 06
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Sharjah hospitals (HN Basic Plus) for Remedy 6:
- AL NAKHEEL ONE DAY SURGERY HOSPITAL
- AL SAHA WA AL SHIFAA HOSPITAL FOR ONE DAY SURGERY
- BURJEEL SPECIALTY HOSPITAL LLC- SHARJAH
- CENTRAL HOSPITAL LLC( EX: Central Private Hospital)
- EMIRATES EUROPEAN HOSPITAL LLC ONE DAY SURGERY
- ORIANA HOSPITAL FOR ONE DAY SURGERY
- ROYAL HOSPITAL
- THUMBAY HOSPITAL DAYCARE - MUWAILAH
```
#### 39. What pharmacies are available in Sharjah for Remedy 6?
- intent: plan_network_city_type
- tool: list_basic_plus_providers
- plan: Remedy 06
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
[NETWORK]
Sharjah pharmacy(s) (HN Basic Plus):
- 800 PHARMACY LLC - SHJ.BR
- ABUDHABI PHARMACY
- AKNAF BAIT AL MAQDES PHARMACY LLC
- AL AFDHAL PHARMACY
- AL AHLIAH PHARMACY
- AL AHSAN PHARMACY
- AL AMAL PHARMACY
- AL AMAN PHARMACY
- AL AMANI PHARMACY
- AL AZHAR PHARMACY
- AL BADR AL KAMIL PHARMACY LLC
- AL BAHR PHARMACY
- AL BASSAM PHARMACY
- AL BURJ AL THAHBI PHARMACY LLC
- AL BUSTAN PHARMACY LLC
- Al Courniche pharmacy LLC
- AL DALIL PHARMACY LLC
- AL DAWA AND AL JAMAL PHARAMCY  LLC
- AL DHIA PHARMACY LLC
- AL DUNIA PHARMACY LLC
- AL ELAJ PHARMACY LLC
- AL FAISAL PHARMACY LLC
- AL FAJER PHARMACY
- AL FARAH PHARMACY
- AL FARAJ PHARMACY
- AL FARDAN CENTRE PHARMACY LLC
- AL FARES PHARMACY
- AL GHAITH PHARMACY
- AL GHRAIF PHARMACY
- AL HIJRAH PHARMACY LLC
- AL HIKMAH PHARMACY - SHARJAH
- AL INAYA AL MUTAQADIMAH PHAMRACY LLC  (PREVIOUSLY AL QASSIM PHARMACY)
- AL INAYA PHARMACY
- AL ITEKAL PHARMACY
- AL ITIHAD PHARMACY
- AL KHAIR PHARMACY
- AL KINDI PHARMACY
- AL MAJAZ PHARMACY
- AL MALEHA PHARMACY
- AL MANARAH PHARMACY
- AL MANSOOR PHARMACY
- AL MAWADAH PHARMACY
- AL MEENA PHARMACY LLC
- AL MOAALAJ PHARMACY LLC
- AL MUSALLA PHARMACY
- AL NABAA PHARMACY
- AL NADIA PHARMACY LLC
- AL NAHAR PHARMACY LLC
- AL NAJIM AL LAMEE PHARMACY
- AL NAS PHARMACY L.L.C
- AL NASEEM PHARMACY
- AL NUZHA PHARMACY
- AL OROUBA PHARMACY
- AL QADSYAH PHARMACY
- AL QASIMIAH PHARMACY
- AL RAJAA PHARMACY
- AL RAWAA PHARMACY LLC
- AL RAYA PHARMACY
- AL RAYAN PHARMACY LLC
- AL RIYADH PHARMACY
- AL RUAYAH PHARMACY
- AL SABAH PHARMACY L.L.C
- AL SADAF PHARMACY
- AL SADIQ PHARMACY
- AL SAFI PHARAMCY LLC
- AL SAHA AND AL JAMAL PHARMACY LLC
- AL SAHA PHARMACY LLC
- AL SAIF PHARMACY
- AL SALAMAH PHARMACY
- AL SAMHA PHARMACY LLC
- AL SEHA AL KUBRA PHARMACY LLC
- AL SHALAL PHARMACY
- AL SHIFA AL AFIAH PHARMACY
- AL TAIF PHARMACY
- AL TAJ PHARMACY
- AL TAQWA PHARMACY LLC
- AL WAAD PHARMACY
- AL WADI PHARMACY
- AL WASFA PHARMACY LLC
- ALBARSHA PHARMACY
- ALNAJIM ALAZRAQ PHARMACY
- ANAS PHARMACY
- ANWAR BAIT AL MAQDES PHARMACY LLC
- Arabian Home health pharmacy
- ARABIAN PHARMACY - SHARJAH
- ASIA PHARMACY LLC
- ASMA PHARMACY
- ASTER AL BUHAIRA PHARMACY
- Aster Pharmacies Group LLC -SHJ BR
- Aster Pharmacies Group LLC- SHJ BR - Branch 3
- Aster Pharmacies Group LLC- SHJ BR - Branch 5
- Aster Pharmacies Group LLC -SHJ BR -Branch 1
- Aster Pharmacies Group LLC -SHJ BR -Branch 2
- Aster Pharmacies Group LLC -SHJ BR -Branch 4
- ASTER PHARMACY - SHARJAH
- ASTER PHARMACY 106
- ASTER PHARMACY 107
- ASTER PHARMACY 108
- ASTER PHARMACY 121
- ASTER PHARMACY 122
- ASTER PHARMACY 125
- ASTER PHARMACY 133
- ASTER PHARMACY 140
- ASTER PHARMACY 151
- Aster Pharmacy 153
- Aster Pharmacy 203
- ATLAS PHARMACY
- BAIT AL DAWAA PHARMACY
- BAIT AL HIKMA PHARMACY
- BAIT AL MAQDES AL JADEEDAH PHARMACY
- BAIT AL MAQDES PHARMACY LLC
- BAIT AL SHIFA PHARMACY - SHARJAH
- BANIYAS PHARMACY
- BILAL PHARMACY  LLC
- BIN SINA PHARMACY
- BOORJ AL ROLLA PHARMACY LLC
- BORJ SARAH PHARMACY
- BURJEEL SPECIALTY HOSPITAL PHARMACY
- CENTRAL PRIVATE HOSPITAL PHARMACY
- CITY LIFE PHARMACY LLC BRANCH SHARJAH
- CONSULTANT'S PHARMACY
- CRISTAL PHARMACY
- DAR AL DAWAA PHARMACY L.L.C
- DAR AL HAYAT PHARMACY L.L.C.
- DAR AL HIKMAH PHARMACY LLC
- DAR AL NEEM PHARMACY LLC
- DEIRA PHARMACY LLC
- DELMON PHARMACY
- DOCTORS PHARMACY
- DUAA PHARMACY
- EMIRATES EUROPEAN HOSPITAL PHARMACY
- EXPERTS PHARMACY
- FATIMA AL ZAHRAA PHARMACY
- GARDEN PHARMACY LLC
- GOLDEN LIFE PHARMACY
- GRAND HAMAD PHARMACY
- GULF PHARMACY LLC
- HALA PHARMACY BR 45
- HALA PHARMACY BR 55
- HALA PHARMACY LLC
- HALA PHARMACY LLC - BRANCH 28
- HALA PHARMACY LLC - BRANCH 38
- HALA PHARMACY LLC - BRANCH 42
- HALA PHARMACY LLC - BRANCH 44
- HALA PHARMACY LLC - BRANCH 46
- HALA PHARMACY LLC - BRANCH 51
- HALA PHARMACY LLC BR 52
- HALA PHARMACY LLC BRANCH 27
- HALA PHARMACY LLC BRANCH 33
- HALA PHARMACY LLC BRANCH 35
- HALA PHARMACY LLC BRANCH 37
- HALA PHARMACY LLC BRANCH 40
- HALA PHARMACY LLC BRANCH 43
- HALA PHARMACY LLC BRANCH 47
- HALA PHARMACY LLC BRANCH 48
- HALA PHARMACY LLC BRANCH 56
- HALA PHARMACY LLC-Branch 1
- HALA PHARMACY LLC-Branch 10
- HALA PHARMACY LLC-BRANCH 11
- HALA PHARMACY LLC-Branch 12
- HALA PHARMACY LLC-BRANCH 18
- HALA PHARMACY LLC-BRANCH 19
- HALA PHARMACY LLC-Branch 2
- HALA PHARMACY LLC-BRANCH 20
- HALA PHARMACY LLC-BRANCH 26
- HALA PHARMACY LLC-Branch 3
- HALA PHARMACY LLC-Branch 4
- HALA PHARMACY LLC-Branch 5
- HALA PHARMACY LLC-Branch 6
- HALA PHARMACY LLC-Branch 7
- HALA PHARMACY LLC-Branch 8
- HALA PHARMACY LLC-Branch 9
- HAMAD AL IHTERAFEYA PHARMACY LLC
- HAMAD AL MUMAYAZAH PHARMACY LLC
- HAMAD AL OULA PHARMACY LLC
- HAMAD PHARMACY
- HARAMAIN PHARMACY
- HEALTH FIRST PHARMACY
- Health First Pharmacy Br 6
- HEALTH FIRST PHARMACY BR2
- HEALTH FIRST PHARMACY BR3
- HEALTH FIRST PHARMACY BR4
- HEALTH FIRST PHARMACY BRANCH 10
- Health First Pharmacy Branch 8
- HEALTH FIRST PHARMACY BRANCH 9
- HEALTHCARE PHARMACY LLC
- HUSSEIN PHARMACY
- IBN BATUTA PHARMACY
- IBN HAYAN PHARMACY SHARJAH
- IBN SEENA PHARMACY 70
- IBN SINA AL KUBRA PHARMACY
- IBN SINA AL RAHMANIA PHARMACY
- IBN SINA AL ZAHIAH PHARMACY
- Ibn Sina Pharmacy 37
- IBN SINA PHARMACY-SOLE PROPRIETORSHIP L.L.C
- IBN ZOHR PHARMACY
- ISHAQ BIN OMRAN PHARMACY LLC
- JABAL JAIS PHARMACY LLC
- LAMIA PHARMACY
- LIFE PHARMACY LLC BRANCH SHJ
- LIFE PHARMACY LLC SHJ BR 3
- LIFE PHARMACY LLC SHJ BR BRANCH 1
- LIFE PHARMACY LLC SHJ BR BRANCH 2
- LIFE PHARMACY LLC SHJ BRANCH 6
- LIFE PHARMACY LLC SHJ BRANCH 7
- LUBNA PHARMACY
- LULU AL FALAH PHARMACY LLC-SHARJAH
- LULU AL NAHDA PHARMACY LLC-SHARJAH
- MAJID PHARMACY
- MAKKAH PHARMACY LLC - SHARJAH
- MARHABA PHARMACY
- MASAFI PHARMACY
- MAY PHARMACY
- MEDI PRIME AL MAJAZ PHARMACY LLC -BRANCH 1
- MEDI PRIME AL NAHDA PHARMACY LLC
- MEDI PRIME AL QASIMIAH PHARMACY
- MEDI PRIME PHARMACY
- MEDICARE PHARMACY
- MEDICINA 22 PHARMACY
- MEDICINA 23 PHARMACY
- MEDICINA 24 PHARMACY
- MEDICINA 25 PHARMACY
- MEDICINA 31
- MEDICOM PHARMACY 17 (PREV.AL ANSAR)
- MERCURY PHARMACY LLC
- MERCURY STAR PHARMACY LLC
- MILAN PHARMACY LLC
- MILLENNIUM PHARMACY
- Modern Al Riqqa Pharmacy
- MODERN BAIT AL MAQDES PHARMACY LLC
- MUHAMMAD AYAZ PHARMACY
- Najm Al Qasimia Pharmacy
- NAJMATH SAHARA AL JADEEDA PHARMACY
- NATIONAL MEDICAL CENTER PHARMACY
- NEW AL WAFA PHARMACY
- NEW BIN SINA PHARMACY
- NEW CITY PHARMACY
- NEW MEDICAL CENTER PHARMACY
- NMC MEDICAL CENTRE PHARMACY -LLC N.M.C Branch 1
- NOORA PHARMACY
- ORCHID PHARMACY ALKHAN LLC
- ORIANA PHARMACY
- Palmyra Pharmacy
- PHARMACY ONE LLC
- RASHA PHARMACY
- RAWABINA PHARMACY
- RAZAN PHARMACY LLC
- REEM AL NAHDAH PHARMACY LLC
- ROYAL GARDEN PHARMACY LLC
- RUKN ABU SHAGHARAH PHARAMCY
- RUKN AL DAWAA PHARMACY LLC
- RUKN AL JAWDAH PHARMACY
- RUKN AL SALAM PHARMACY
- RUKN ALYASMEEN PHARMACY
- SAHARA AL JAZEERA PHARMACY
- SAHARA LIFE PHARMACY LLC
- SAIF AL KHAN PHARMACY LLC
- SAIFZONE PHARMACY (FZC)
- SALALAH PHARAMCY LLC
- SALIM PHARMACY
- SALSABEEL PHARMACY
- SAMA MUWAILEH PHARMACY LLC
- SCIENTIFIC PHARMACY
- SHAMS AL NAHDA PHARMACY LLC
- SHARJAH AHALIA PHARMACY
- SHARJAH PHARMACY
- SHARQAN PHARMACY
- SIR ALSHIFFAA PHARMACY
- STARCARE PHARMACY LLC
- Super Care Pharmacy LLC - SHJ BR - Branch 2
- Super Care Pharmacy LLC - SHJ BR - Branch 3
- SUPERCARE PHARMACY
- TAIBAH PHARMACY
- United Pharmacy AL Zahiah LLC
- UNITED PHARMACY AL ZAHIAH LLC - BRANCH 1
- UNITED PHARMACY AL ZAHIAH LLC - BRANCH 2
- WAJEAT AL KHOOR PHARMACY - SHARJAH
- WASEEM PHARMACY
- YAS PHARMACY LLC
- ZAHRAT ALRABIE PHARMACY
- SHIFA AL JAZEERAH CENTRE PHARMACY .LLC – SHJ.BR
- AL YAMAMA PHARMACY
- AL TALAL PHARMACY
- AL MISBAH PHARMACY L L C
- AL ENWAN PHARMACY LLC
- AL AJWAH PHARMACY LLC
- AL AQSA PHARMACY L.L.C
- AL FAROOQ PHARMACY L.L.C
- AL TAWAR PHARMACY LLC
- AL RAZY PHARMACY L.L.C
- AL HAMRIA PHARMACY
- DAR AL FARAH PHARMACY LLC
- NAWAIEM PHARMACY LLC
- AL TEMOUH PHARMACY LLC
- Al saah pharmacy L.L.C
- Health First Pharmacy - Branch 11
- AL NOOR AL SAATE PHARMACY LLC
- BADAR PHARMACY LLC
- MEDICINE WORLD LLC
- Life Pharmacy LLC Branch Br of Sharjah 11
- Life Pharmacy LLC - SHJ. BR. Branch 13
- MUZEIRA PHARMACY LLC
- W WILSON HOSPITAL PHARMACY
- NAJMAT MUWEILAH PHARMACY LLC
- LULU AL BUHAIRA PHARMACY LLC
- AL SANA PHARMACY LLC
- AL SAMA PHARMACY LLC
- AL SHUALLA PHARMACY
- ASTER PHARMACIES GROUP LLC - SHJ.BR - BRANCH 7
- DELTA AL DHAID PHARMACY
- DELTA AL MAMZAR PHARMACY
- DELTA MODERN PHARMACY
- DELTA PHARMACY
- Faith Zone Pharmacy FZC
- NASEEM AL BATAEH PHARMACY LLC
- Al Dhafrah Pharmacy LLC
- Liwa Pharmacy LLC
- AL BURHAN PHARMACY LLC
- AL MUBARAK CENTRE PHARMACY LLC
- AL NAHDA PHARMACY LLC
- AL RAWDHA PHARMACY LLC
- AL TAMIMI PHARMACY LLC
- DAR AL SAJAA PHARMACY LLC
- NAJMAT ABU SHAGARA PHARMACY LLC
- ZAHRAT AL MADINAH PHARMACY LLC
- AL GHAD AL AFDAL PHARMACY LLC
- NAJMAT AL ROLLA PHARMACY LLC
- Life Pharmacy LLC SHJ Br Branch 9
- Life Pharmacy LLC Branch Br of Sharjah 8
- Aster Pharmacies Group LLC - Shj. Br - Branch 8
- AL MARJAN PHARMACY LLC
- Rayhan Gulf Pharmacy LLC
- NAHDI PHARMACY L.L.C - SHJ. BR
- NAHDI PHARMACY L.L.C - SHJ. BR - BRANCH 1
- FAMILY STAR PHARMACY
- MEDICOM PHARMACY 37 LLC SHJ BR (AL KHAN) SHARJAH
- MEDCOM 45 PHARMACY
- SUPERCARE PHARMACY LLC - SHJ BR - BRANCH 4
- GOLDEN STAR PHARMACY L L C
- RUKN AL AFRAH PHARMACY L.L.C
- 800 PHARMA PHARMACY LLC-SHJ.BR
- AL FARAH AL HADITHAH PHARMACYLLC
- AL HADHAR PHARMACY LLC
- AL MATAR PHARMACY LLC
- AL RAFEAH PHARMACY LLC
- DAR AL FARAJ PHARMACY LLC
- JANAH PHARMACY L.L.C (SHARJAH)
- JANAH PHARMACY L.L.C BRANCH-2
- LANA PHARMACY L.L.C (SHARJAH)
- PHARMACY SABEEL L.L.C - SHJ. BR 1
- RUKN AL RAFEAH PHARMACY LLC
- RUKN AL UFUQ PHARMACY LLC
- AL HAJIS PHARMACY L.L.C
- WAHAT AL TAIBAH PHARMACY L.L.C
- AL JAREENA PHARMACY LLC
- TABOOK PHARMACY LLC
- MEDCOM 44 PHARMACY
- LIFE PHARMACY L.L.C - SHJ. BR 22
- LIFE PHARMACY LLC. SHJ. BR - BRANCH 26
- LIFE PHARMACY L.L.C - SHJ. BR 23
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 27
- MODERN FAMILY PHARMACY LLC SHJ BR
- PURE PATH PHARMACY L.L.C.SP
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 21
- ARD AL KHAN PHARMACY L.L.C
- Zest Wellness Pharmacy L LC - Shj. Br
- Aster Pharmacies Group Llc - Shj. Br - Branch 6
- IBN SINA PHARAMCY SOLE PROPRIETORSHIP L.L.C - BRANCH 3
- IBN SINA PHARAMCY SOLE PROPRIETORSHIP L.L.C - SHJ. BR - BRANCH 9
- IBN SINA PHARAMCY SOLE PROPRIETORSHIP L.L.C - BRANCH 11
- LIFE PHARMACY LLC - SHJ.BR-BRANCH 16
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 10
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 18
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 19
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 20
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 28
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 32
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 31
- REGAL HOUSE PHARMACY
- Right Care Pharmacy L L C SP
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 30
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 35
- AL SHIFA UROPI PHARMACY L.L.C (SHARJAH)
- JESR AL SHIFA PHARMACY - L.L.C
- DAOUD PHARMACY L.L.C.SP
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 34
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 38
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 37
- RUKN AL MAJAZ PHARMACY L.L.C
- Health First Pharmacy - Branch 7
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 36
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 25
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 17
- FIRST STEP PHARMACY L.L.C.SP
- SADAF AL SAJAH PHARMACY
- AL NEEL PHARMACY L.L.C.S.P
- ALAHRAR PHARMACY L.L.C.S.P
- TULIP PHARMACY LLC SP
- SHIFA MUWAILEH PHARMACY L.L.C
- AL BARASHI PHARMACY LLC
- AL NAHDHA PHARMACY LLC
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 40
- IBN SINA PHARAMCY SOLE PROPRIETORSHIP L.L.C - BRANCH 10
- IBN SINA PHARAMCY SOLE PROPRIETORSHIP L.L.C - SHJ. BR - BRANCH 14
- IBN SINA SOLEPROPRIETORSHIP LLC SHJ BR 13
- CO OPERATIVE PHARMACY
- Aster Pharmacies Group LLC - Shj. Br - Branch 9
- LIFE TIME PHARMACY L.L.C.SP - BRANCH 1
- 24 HOUR PHARMACY CO.LLC - SHJ. BR 1
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 41
- PESHAWAR PHARMACY LLC (SHARJAH)
- AL BEDAYA PHARMACY L.L.C.SP
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 43 (AL KHAN)
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 44 (AL NAHDA SHARJAH)
- LIFE PHARMACY L.L.C - SHJ. BR - BRANCH 42 (AL SHAHBA)
```
#### 40. Remedy 6 Dubai providers
- intent: error
- tool: None
- plan: None
- classification: REVIEW
- reason: Runtime parsing/handling error requires deterministic guard.
- output:
```text
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Projects\NGI-AI-AGENT-SALES-ASSISTANCE-TOOLS\src\agent_entrypoint.py", line 39, in <module>
    main()
  File "C:\Projects\NGI-AI-AGENT-SALES-ASSISTANCE-TOOLS\src\agent_entrypoint.py", line 26, in main
    print(json.dumps(result, ensure_ascii=False, indent=2))
  File "C:\Users\H Dos\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1256.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u200b' in position 46961: character maps to <undefined>
```
#### 41. Providers in Dubai Remedy 6
- intent: error
- tool: None
- plan: None
- classification: REVIEW
- reason: Runtime parsing/handling error requires deterministic guard.
- output:
```text
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Projects\NGI-AI-AGENT-SALES-ASSISTANCE-TOOLS\src\agent_entrypoint.py", line 39, in <module>
    main()
  File "C:\Projects\NGI-AI-AGENT-SALES-ASSISTANCE-TOOLS\src\agent_entrypoint.py", line 26, in main
    print(json.dumps(result, ensure_ascii=False, indent=2))
  File "C:\Users\H Dos\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1256.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u200b' in position 20254: character maps to <undefined>
```
#### 42. Dubai providers Remedy 6
- intent: error
- tool: None
- plan: None
- classification: REVIEW
- reason: Runtime parsing/handling error requires deterministic guard.
- output:
```text
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Projects\NGI-AI-AGENT-SALES-ASSISTANCE-TOOLS\src\agent_entrypoint.py", line 39, in <module>
    main()
  File "C:\Projects\NGI-AI-AGENT-SALES-ASSISTANCE-TOOLS\src\agent_entrypoint.py", line 26, in main
    print(json.dumps(result, ensure_ascii=False, indent=2))
  File "C:\Users\H Dos\AppData\Local\Programs\Python\Python312\Lib\encodings\cp1256.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u200b' in position 46961: character maps to <undefined>
```
#### 43. هل Burjeel Hospital داخل الشبكة؟
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
YES: burjeel hospital
```
#### 44. هل مستشفى برجيل داخل الشبكة؟
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
YES: مستشفى برجيل
```
#### 45. Burjeel Hospital في اي شبكة؟
- intent: unsupported
- tool: None
- plan: None
- classification: REVIEW
- reason: Unsupported phrasing or out-of-scope query needs triage.
- output:
```text
عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم.
```
#### 46. في أي شبكة Burjeel Hospital
- intent: unsupported
- tool: None
- plan: None
- classification: REVIEW
- reason: Unsupported phrasing or out-of-scope query needs triage.
- output:
```text
عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم.
```
#### 47. هل ACCURACY PLUS MEDICAL LABORATORY في شبكة بيسك بلس؟
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
[NETWORK] المزود ACCURACY PLUS MEDICAL LABORATORY داخل شبكة HN Basic Plus. النوع: DIAGNOSTIC CENTER. المدينة: ABU DHABI.
```
#### 48. هل AL FARHAN MEDICAL LABORATORY - L L C في بيسك بلس؟
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
[NETWORK] المزود AL FARHAN MEDICAL LABORATORY - L L C داخل شبكة HN Basic Plus. النوع: DIAGNOSTIC CENTER. المدينة: ABU DHABI.
```
#### 49. هاتلي مستشفيات في الشارقة
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
[NETWORK]
مستشفيات الشارقة (HN Basic Plus):
- AL NAKHEEL ONE DAY SURGERY HOSPITAL
- AL SAHA WA AL SHIFAA HOSPITAL FOR ONE DAY SURGERY
- BURJEEL SPECIALTY HOSPITAL LLC- SHARJAH
- CENTRAL HOSPITAL LLC( EX: Central Private Hospital)
- EMIRATES EUROPEAN HOSPITAL LLC ONE DAY SURGERY
- ORIANA HOSPITAL FOR ONE DAY SURGERY
- ROYAL HOSPITAL
- THUMBAY HOSPITAL DAYCARE - MUWAILAH
```
#### 50. عيادات في دبي
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
[NETWORK]
عيادات دبي (HN Basic Plus):
- DR. ISMAIL DAY SURGICAL CENTRE
- ABBARA POLYCLINIC
- ABEER AL NOOR POLY CLINIC LLC BRANCH
- ABRIS MEDICAL CENTRE LLC
- ABSOLUTE WELLNESS MEDICAL CENTRE
- ACCESS CLINIC ALQUOZ
- ACCESS CLINIC BUR DUBAI
- ACCESS CLINIC DIC BR DM HEALTHCARE LLC
- ACCESS CLINIC DIP
- ACCESS CLINIC DIP 2 BR OF DM HEALTHCARE LLC
- ACCESS CLINIC FREEZONE
- ACCESS CLINIC INTERNATIONAL CITY
- ACCESS CLINIC PERSIA CLUSTER
- ACCESS CLINIC SONAPUR
- ACCESS CLINIC SONAPUR 2 BR OF DM HEALTHCARE LLC (EX. AFIF MEDICAL CENTER)
- ADVANCED CARE MEDICAL CENTER
- ADVANCED CARE MEDICAL CENTER  LLC (BRANCH)
- ADVANCED CARE MEDICAL CENTER BRANCH
- ADVANCED CARE MEDICAL CENTER LLC (BRANCH)
- ADVANCED CARE MEDICAL CENTER LLC BRANCH
- ADVANCED CARE MEDICAL CENTER LLC BRANCH-GRAND CITY MALL
- ADVANCED CARE MEDICAL CENTRE L.L.C (BRANCH )- DIP 1
- AL ABRAH CLINIC
- AL AMAL POLYCLINIC
- AL AMAN MEDICAL CENTER
- AL AZHAR CLINIC
- AL AZHAR CLINIC BR DIP 2
- AL AZHAR CLINIC BRANCH
- Al Azhar Clinic Branch 3
- Al Azhar Clinic LLC 4
- AL DHAFRA MEDICAL CENTRE
- Al Fahim Clinic
- AL FALAH MEDICAL CLINIC
- AL HANA MEDICAL CENTER LLC
- AL HANA MODERN MEDICAL CENTER LLC
- AL KHAIL MEDICAL CENTER
- AL KHAIL MEDICAL CENTRE BRANCH
- AL MASHAHER MEDICAL CENTRE
- AL MURJAN MEDICAL CENTER
- AL NOOR POLYCLINIC - BR OF GHI AL SATWA
- AL NOOR POLYCLINIC - BR OF GHI DEIRA
- AL NOOR POLYCLINIC BR OF GHI AL RIGGA (AMBER)
- WELLCARE ADVANCED POLY CLINIC L.L.C (EX. AL QUOZ CITY STAR POLYCLINIC)
- AL QUSAIS STAR POLYCLINIC
- SONAPUR STAR POLYCLINIC L.L.C (EX. AL QUSAIS STAR POLYCLINIC (BRANCH))
- AL RASHIDIYAH AL NOOR POLYCLINIC
- AL SANAIYA MEDICAL CLINIC
- AL SANAIYA MEDICAL CLINIC-BRANCH
- AL SHAAB MEDICAL CENTRE
- AL SHIFA AL KHALEEJI MEDICAL CENTER
- Al Shifa Al Khaleeji Medical Centre Branch LLC-DIP
- AL SHIFA INTERNATIONAL CLINIC
- AL SHIFA INTERNATIONAL CLINIC LLC- BRANCH
- AL TADAWI MEDICAL CENTRE
- AL TAIF MEDICAL CENTER
- AL WAHA CLINIC
- ALDIA MEDICAL CENTER L.L.C
- ALHABAB GENERAL CLINIC
- ALI MEDICAL CLINIC
- AMALA MEDICAL CENTRE
- AMIRUDDIN CLINIC
- ANAYA MEDICAL CENTER LLC
- ANAYA MEDICAL CENTER LLC BRANCH
- APPLE CLINIC
- APPLE INTERNATIONAL POLY CLINIC
- ARIN CARE POLYCLINIC L.L.C
- ASH TREE CLINIC LLC
- ASHOKAN MEDICAL CLINIC
- ASTER CEDARS CLINIC
- ASTER JABAL ALI MEDICAL CENTRE
- Aster Medical Centre Oud Metha (Br Of D M Healthcare LLC)
- ASTER MEDICAL CENTRE ABU HAIL BR OF DM HEALTHCARE
- ASTER MEDICAL CENTRE AL QUSAIS
- ASTER MEDICAL CENTRE DUBAI LAND
- ASTER MEDICAL CENTRE INTERNATIONAL CITY(Gynaecology and Paediatrics services only)
- ASTER MEDICAL CENTRE REMRAAM (BR OF D M HEALTHCARE)
- BADR AL SAMAA MEDICAL CENTER
- BEST HEALTH MEDICAL CENTER L.L.C
- BIO VISTA MEDICAL CENTRE LLC
- BLUE BELL MEDICAL CENTRE
- BRIGHT LIFE MEDICAL CENTER LLC
- CARE AND CURE MEDICAL CENTER L.L.C
- CARE ONE POLY CLINIC LLC
- CARE PLUS MEDICAL CENTER
- CLINICARE BR OF IMARA HEALTH CARE LLC
- CLINICARE SAMARI BR OF IMARA HEALTH CARE LLC
- COMMUNITY MEDICAL CENTRE
- COSMOPOLITAN MEDICAL CENTRE
- DOCIB CLINIC LLC
- DOCTORS CLINIC
- DOCTORS CLINIC DIAGNOSTIC CENTRE FZ-LLC
- DR. IBRAHIM ABBARA CLINIC
- DR. ISMAIL MEDICAL CENTRE - AL MUHAISANAH
- DR. ISMAIL MEDICAL CENTRE - AL QUOZ
- DR. ISMAIL POLYCLINIC BRANCH-DISCOVERY GARDEN
- DR. ISMAIL POLYCLINIC BRANCH-JEBEL ALI
- DR. ISMAIL POLYCLINIC KARAMA
- DR. JOHN CLINIC
- DR. JOSEPH’S POLYCLINIC-KARAMA BR OF GHI
- DR. KAMKAR MEDICAL & PHYSIOTHERAPY CENTRE
- DR. KOYA CLINIC
- DR. MOOPENS' AL QUOZ MEDICAL CENTRE
- DR. MOOPEN'S MEDICAL CENTER - KARAMA
- DR. MUHAMMED KUNHI MEDICAL CLINIC
- DR. RADAKRISHNAN MEDICAL CENTRE
- DR. SANJAY MEDICAL CENTER - DUBAI
- DR. SHANIL MEDICAL CENTRE LLC
- DR.ABDULLAS CLINIC
- DULSCO MEDICAL CLINIC
- DULSCO MEDICAL CLINIC BRANCH
- DURRAIYA KAMAL MEDICAL CLINIC
- EXCEL HEALTHCARE ICARE CLINICS DISCOVERY GARDEN
- FAITH JABAL MEDICAL CENTER L.L.C
- FALCON MEDICAL CLINIC
- FAMILY CLINIC
- FIRST MEDICAL CENTRE
- FULLCARE MEDICAL CENTER
- Globehealth General Clinic  LLC
- GOODWILL CLINIC LLC
- GRAND INFINITY MEDICAL CENTER LLC
- GRAND INFINITY MEDICAL CENTER LLC BRANCH
- GREEN CITY MEDICAL CENTER L.L.C. (EX: NEW AL MUSALLA MEDICAL CENTER BRANCH)
- HARLEY INTERNATIONAL MEDICAL CLINIC
- HARLEY INTERNATIONAL MEDICAL CLINIC (BRANCH)
- Harley International Medical Clinic LLC Branch
- HOPECARE POLYCLINIC L.L.C
- HOUSTON MEDICAL CLINIC LLC
- HOUSTON MEDICAL CLINIC LLC (Branch)
- HTK Medical Centre
- ICARE ALREFFA BR OF EXCEL HEALTHCARE LLC
- ICARE OASIS BRANCH OF EXCEL HEALTHCARE
- Islamabad Medical Clinic LLC( Ex: Globe HealthPolyclinic)
- JANSON MEDICAL CLINIC
- JOSEPH'S QUSAIS POLYCLINIC
- JUPITER AL NAHDA POLYCLINIC
- JUPITER AL QUSAIS POLYCLINIC
- JUPITER SPECIALTY MEDICAL CENTER
- KARAMA MEDICAL CENTER - DIP BRANCH
- KARAMA MEDICAL CENTER AL QUOZ MALL BRANCH
- KARAMA MEDICAL CENTRE
- KARAMA MEDICAL CENTRE - AL QUOZ BRANCH
- KARAMA MEDICAL CENTRE BR  JV
- KARAMA MEDICAL CENTRE BR, BURJUMAN
- KARAMA MEDICAL CENTRE BR. AL KHAIL GATE
- KARAMA MEDICAL CENTRE BR. MUHAISNAH
- KEERTHI MEDICAL CENTER (PREVIOUSLY DR. KEERTHI CLINIC)
- KHALIDHA MEDICAL CENTRE LLC
- KIMS MEDICAL CENTRE
- KINGS MEDICAL CENTER LLC
- LAVERA CLINIC LLC
- LIFEGUARD GENERAL CLINIC L.L.C (EX. OUR CARE AND CURE MEDICAL CENTER LLC )
- LIFENITY INTERNATIONAL ADVANCED POLY CLINIC L.L.C
- LIFENITY INTERNATIONAL ADVANCED POLY CLINIC L.L.C (BRANCH)
- LIVE CARE CLINIC LLC
- LOTUS MEDICAL CENTER
- MAG Health Clinic
- MARHABA MEDICAL CENTER-DXB
- MATHEW MEDICAL CLINIC LLC
- MED ONE MEDICAL CENTER LLC (EX. AQUA MEDICAL CENTER)
- Medi Family Polyclinic FZE
- MEDICURE CENTRE
- MEDICURE CENTRE BRANCH
- Medicure Polyclinic L.L.C Branch- Al Manara
- MEDILIFE POLYCLINIC LLC
- MEDILITE MEDICAL CENTRE
- MEDZE CLINIC LLC
- MID EAST POLY CLINIC
- Miracure Medical Centre  LLC
- Mobile Home Healthcare Services LLC
- MUHAISNA SPECIALIST MEDICAL CENTRE LLC
- MULTI CARE MEDICAL CENTRE
- MVR DIAGNOSTIC CLINIC L.L.C (EX. MVR Medical Center)
- NAIF MEDICAL CENTER LLC
- NASSER CLINIC
- NEW AL MUSALLA MEDICAL CENTER
- NEW APOLLO POLYCLINIC
- NEW EMIRATES MEDICAL CENTER
- NEW LOTUS MEDICAL CENTER
- NEW MEDICAL CENTER (Ex:Reena Beegum clinic branch)
- NEW MEDICAL CENTRE LLC
- NEW MEDILIFE MEDICAL CENTRE L.L.C
- NEW SANAIYA CLINIC
- NEW SANAIYA CLINIC BRANCH - HORALANZ
- NEW SANAIYA CLINIC BRANCH-DIP
- NMC DIC CLINIC AND PHARMACY BR OF NMC ROYAL HOSPITAL LTD DUBAI BRANCH
- NMC POLYCLINIC BRANCH OF NMC HOSPITAL LLC
- Noor Al Shefa Branch 3
- NOOR AL SHEFA CLINIC - JEBEL ALI MALL
- NOOR AL SHEFA CLINIC BRANCH - AL QUOZ
- NOOR AL SHEFA CLINIC BRANCH - RAS AL KHOR
- Noor Al Shefa Clinic Branch. 4
- NOVITAS CLINIC L.L.C BRANCH
- NOVITAS CLINIC LLC
- OXFORD MEDICAL CENTER
- PAKISTAN MEDICAL CENTER
- Paradise Plus Poly Clinic LLC
- PESHAWAR MEDICAL CENTRE- DUBAI
- PHYSIOVEDA MEDICAL CENTER L.L.C
- PHYSIOVEDA MEDICAL CENTER L.L.C (BRANCH)
- PRIME MEDICAL CENTER AL QUSAIS (BR OF PRIME MEDICAL CENTER LLC)
- PRIME MEDICAL CENTER DUBAI AIRPORT (BR OF PRIME MEDICAL CENTER LLC)
- PRIMECORP MEDICAL CENTER AL QUSAIS (BR OF PRIMECORP MEDICAL CENTER LLC)
- PRIMECORP MEDICAL CENTER AL WARSAN (BR OF PRIMECORP MEDICAL CENTER L.L.C)
- PRIMECORP MEDICAL CENTER ALQUOZ LLC BRANCH
- PRIMECORP MEDICAL CENTER DWC BR OF PRIMECORP MEDICAL CENTER LLC
- PRIMECORP MEDICAL CENTER L L C DIP BRANCH
- PRIMECORP MEDICAL CENTER LLC
- PRIMECORP MEDICAL CENTER LLC  JABAL ALI BRANCH
- QAMAR AL MADINA MEDICAL CENTER L.L.C
- RASHIDIYA PRIVATE POLYCLINIC
- Releaf Medical Centre (DIP)
- Releaf Medical Centre (J Mart)
- Releaf Medical Centre(Al Qouz 2)
- Releaf Medical Centre(Jabal Ali)
- REMEDY PLUS MEDICAL CLINIC LLC
- RIAZ MEDICAL CENTRE - DUBAI
- RUBY CLINIC
- SALEEM POLYCLINIC
- SHEIKH MANNA BIN HASHER AL MAKTOUM POLYCLINIC
- SIRAJUDEEN MEDICAL CENTER
- SYED SADIQ GENERAL PRACTITIONER CLINIC LLC
- THE DOCTORS HUB POLYCLINIC L.L.C (EX. DR. JOSEPH GHRAYEB POLYCLINIC)
- TORONTO MEDICAL CENTER LLC
- VCARE POLYCLINIC LLC
- VIDA CLINICS- BURDUBAI
- VIDA CLINICS LLC BRANCH-MUHAISANAH
- Zahrat Al Shefa Medical Centre LLC
- ZEN LIFE POLYCLINIC CO LLC
- ZIYATH ANSAR POLY CLINIC L.L.C
- CARE BLUE CLINIC FZCO
- DOHA PHARMACY EXPRESS CLINIC (GP CLINIC ONLY)
- HALA PHARMACY 13 EXPRESS CLINIC (GP CLINIC ONLY)
- JADAF LIFE PHARAMCY EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE AL QUSAIS PHARMACY EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE DWTC PHARMACY EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE MURAQABAT PHARMACY EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE PEARL PHARMACY EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE PHARMACY 16 EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE PHARMACY 25 EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE PHARMACY 74 EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE PHARMACY 77 EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE PHARMACY BARSHA SOUTH FOURTH EXPRESS CLINIC (GP CLINIC ONLY)
- LIFE PHARMACY EXPRESS CLINIC (GP CLINIC ONLY)
- NATURES LIFE EXPRESS CLINIC LLC (GP CLINIC ONLY)
- NEW AL KANZ PHARAMCY BRANCH EXPRESS CLINIC (GP CLINIC ONLY)
- RAMADA LIFE EXPRESS CLINIC (GP CLINIC ONLY)
- ROYAL LIFE EXPRESS CLINIC (GP CLINIC ONLY)
- AXON MEDICA POLYCLINIC, BR. AXON MEDICA INVESTMENT MANAGEMENT L.L.C
- AXON MEDICA POLYCLINIC
- DR ISMAIL POLYCLINIC
MALL BR OF DR. ISMAIL
POLYCLINIC
- APOLLO CLINIC LLC (EX. NEW CITY CLINIC LLC)
- AXIOS HOME CARE SERVICES L.L.C
- Modern Family Clinic LLC
- LIFE PHARMACY 44 EXPRESS CLINIC (GP CLINIC ONLY)
- Evercare Medical Center
- FUTURE LIFE GENERAL MEDICAL CLINIC
- MODERN FAMILY CLINIC L.L.C (BRANCH)
- DR ABDUL LATIF CLINIC LLC
- LIFE PHARMACY 119 (BR OF LIFE PHARMACY L.L.C)
- LIFE PHARMACY 125 (BR OF LIFE PHARMACY L.L.C)
- LIVERPOOL MEDICAL CLINIC L.L.C
- YOUR CENTER POLY CLINIC L.L.C
- MODERN FAMILY CLINIC L.L.C (BRANCH)
- MBM SPECIALITY MEDICAL CENTER L.L.C
- NOOR AL AHALIA MEDICAL CENTER
- ALOKA EYE CLINIC LLC
- MEDCOME HEALTH CARE CENTER
- BRIGHT CARE CLINIC L.L.C
- G M G MEDICAL CENTER L.L.C
- KHAYBER MEDICAL CENTER
- ASCENT ENT SPECIALITY CENTRE LLC
- STEPS POLYCLINIC LLC
- DR. ISMAIL POLYCLINIC (BRANCH)
- SEHA AL NOOR CLINIC LLC
- Al Bayan Medical Center LLC
- ADVANCED CARE MEDICAL CENTER BRANCH LLC
- RALS HEALTHCARE (AL QUSAIS)  (EX. MINI VM POLYCLINIC)
- RALS HEALTHCARE BR OF ABD ULWAHED BIN SHABIB INVESTMENT GROUP L.L.C (JABAL ALI) DUBAI
- Oud Al Muteena Medical Center
- NOOM MEDICAL CLINIC L.L.C
- SHAMS AL AHALIA MEDICAL CENTER
- ZMC HEALTH CLINIC L.L.C
- GSM MEDICAL CENTRE LLC (BRANCH)
- GOOD LIFE MEDICAL CENTER L.L.C
- BLOOM PLUS POLY CLINIC L.L.C
- AL MARIFFA MEDICAL CENTER L.L.C (DUBAI)
- BEST LIFE GENERAL CLINIC L.L.C
- CALLADOC TELEHEALTH SERVICES L.L.C
- AFRIDI MEDICAL CENTER L.L.C
- SHARE AND CARE MEDICAL CENTER L L C
- ROYAL PHOENIX CLINIC L.L.C
- Life Pharmacy and Express Clinic FZ LLC
- Ferdows Medical Center L.L.C
- Peshawar Medical Center LLC (International City)
- Life Pharmacy 180 Express Clinic
- LIFE PHARMACY 173 BR OF LIFE PHARMACY (GENERAL CLINIC)
- MADAWAH HEALTHCARE CLINIC L.L.C
- SAFA ALNOOR POLYCLINIC LLC
- MUMTAZ AL NOOR EXPRESS PHARMACY CLINIC LLC
- GRAND DR ISMAIL POLYCLINIC L.L.C
- Pak Satwa Poly Clinic Co. LLC
- Nucleus Clinic LLC (DUBAI MARINA)
- MEDHUB MEDICAL CENTER L.L.C
- DYNAMIC LIFE CLINIC L.L.C
- DYNAMIC LIFE CLINIC LLC BRANCH
- IRIS DENTAL CLINIC LLC
- AL NOOR POLYCLINIC L.L.C (BRANCH)
- L L H MEDICAL CENTER L.L.C (BRANCH)
- Tadawi Health Care LLC (Branch) IMPZ
- Tadawi Health Care LLC (Branch) DIP
- LIFE PHARMACY 189 EXPRESS CLINIC
- ROYAL SABA MEDICAL CLINIC
- ROYAL SABA MEDICAL CLINIC PHARMACY
- JAVIDA MEDICAL CENTER L.L.C.
- ISLAMABAD MEDICAL CLINIC LLC BR
- CITY RELIEF EXPRESS CLINIC LLC
- CRX EXPRESS CLINIC LLC
- LIFE PHARMACY 190 EXPRESS CLINIC
- PARADISE PLUS POLY CLINIC L.L.C (BRANCH)
- CARE 7 MEDICAL CENTER L.L.C
- ARMADA MEDICAL CENTRE DMCC
- MEDHUB MEDICAL CENTER L.L.C(BRANCH)
- MOOPANS POLYCLINIC L.L.C
- ZAIN CURA MEDICAL CENTER L.L.C
- BETA STAR CLINIC L L C
- AL BARSHA AL NOOR POLYCLINIC LLC
```

### comparison_questions
#### 51. Compare Remedy 04 and Remedy 05
- intent: plan_comparison
- tool: compare_plans
- plan: Remedy 04 vs Remedy 05
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Comparison between Remedy 04 and Remedy 05:
Annual Limit: Remedy 04: AED. 150,000 | Remedy 05: AED. 150,000
Pharmacy: Remedy 04: Maximum AED 7,500/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered | Remedy 05: Maximum AED 7,500/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered
Diagnostics: Remedy 04: Lab tests: NIL co-pay applied at the time of payment Covered.; Radiology: NIL co-pay applied at the time of payment | Remedy 05: Lab tests: NIL co-pay applied at the time of payment Covered.; Radiology: NIL co-pay applied at the time of payment
Physiotherapy: Remedy 04: Covered for a maximum of 12 sessions per year NIL co-pay per session | Remedy 05: Covered for a maximum of 12 sessions per year NIL co-pay per session
Direct Billing: Remedy 04: Yes | Remedy 05: Yes
Reimbursement Allowed: Remedy 04: No | Remedy 05: Yes
Referral Required: Remedy 04: Yes | Remedy 05: No
Area of Coverage: Remedy 04: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval. | Remedy 05: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval.
Network: Remedy 04: HN Basic Plus (OP Restricted to Clinics) with direct access to below hospitals for OP Services. Aster Hospitals (Qusais, Mankhool, Jebel Ali) Burjeel Specialty Hospital Sharjah International Modern Hospital, DXB Ajman Specialty Hospital – Ajman Al Saha wa Al Shifaa Hospital For One Day Surgery – Sharjah Specialist Subject to GP Referral both in Clinics and Hospitals | Remedy 05: HN Basic Plus

Both plans are similar overall, but differ in: Reimbursement Allowed: Remedy 04=No, Remedy 05=Yes, Referral Required: Remedy 04=Yes, Remedy 05=No, Network: Remedy 04=HN Basic Plus (OP Restricted to Clinics) with direct access to below hospitals for OP Services. Aster Hospitals (Qusais, Mankhool, Jebel Ali) Burjeel Specialty Hospital Sharjah International Modern Hospital, DXB Ajman Specialty Hospital – Ajman Al Saha wa Al Shifaa Hospital For One Day Surgery – Sharjah Specialist Subject to GP Referral both in Clinics and Hospitals, Remedy 05=HN Basic Plus.

Recommendation:
Both plans are very similar in their key benefits.
```
#### 52. Compare Remedy 02 and Remedy 03
- intent: plan_comparison
- tool: compare_plans
- plan: Remedy 02 vs Remedy 03
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Comparison between Remedy 02 and Remedy 03:
Annual Limit: Remedy 02: AED. 150,000 | Remedy 03: AED. 150,000
Pharmacy: Remedy 02: Maximum AED 3,000/year 30% payable by member on each prescription. Any medication in excess of the annual limit will not be covered | Remedy 03: Maximum AED 5,000/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered
Diagnostics: Remedy 02: Lab tests: 15% co-pay applied at the time of payment Covered.; Radiology: 15% co-pay applied at the time of payment | Remedy 03: Lab tests: 10% co-pay applied at the time of payment Covered.; Radiology: 10% co-pay applied at the time of payment
Physiotherapy: Remedy 02: Covered for a maximum of 12 sessions per year 15% co-pay per session | Remedy 03: Covered for a maximum of 12 sessions per year 10% co-pay per session
Direct Billing: Remedy 02: Yes | Remedy 03: Yes
Reimbursement Allowed: Remedy 02: No | Remedy 03: No
Referral Required: Remedy 02: Yes | Remedy 03: Yes
Area of Coverage: Remedy 02: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval. | Remedy 03: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval.
Network: Remedy 02: HN Basic Plus | Remedy 03: HN Basic Plus

Both plans are similar overall, but differ in: Pharmacy: Remedy 02=Maximum AED 3,000/year 30% payable by member on each prescription. Any medication in excess of the annual limit will not be covered, Remedy 03=Maximum AED 5,000/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered, Diagnostics: Remedy 02=Lab tests: 15% co-pay applied at the time of payment Covered.; Radiology: 15% co-pay applied at the time of payment, Remedy 03=Lab tests: 10% co-pay applied at the time of payment Covered.; Radiology: 10% co-pay applied at the time of payment, Physiotherapy: Remedy 02=Covered for a maximum of 12 sessions per year 15% co-pay per session, Remedy 03=Covered for a maximum of 12 sessions per year 10% co-pay per session.

Recommendation:
Remedy 03 is generally better if your client is looking for stronger outpatient benefits:
- Higher pharmacy limit (AED 5,000 vs 3,000)
- Stronger diagnostics benefits
```
#### 53. Compare Remedy 02 and Remedy 04
- intent: plan_comparison
- tool: compare_plans
- plan: Remedy 02 vs Remedy 04
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Comparison between Remedy 02 and Remedy 04:
Annual Limit: Remedy 02: AED. 150,000 | Remedy 04: AED. 150,000
Pharmacy: Remedy 02: Maximum AED 3,000/year 30% payable by member on each prescription. Any medication in excess of the annual limit will not be covered | Remedy 04: Maximum AED 7,500/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered
Diagnostics: Remedy 02: Lab tests: 15% co-pay applied at the time of payment Covered.; Radiology: 15% co-pay applied at the time of payment | Remedy 04: Lab tests: NIL co-pay applied at the time of payment Covered.; Radiology: NIL co-pay applied at the time of payment
Physiotherapy: Remedy 02: Covered for a maximum of 12 sessions per year 15% co-pay per session | Remedy 04: Covered for a maximum of 12 sessions per year NIL co-pay per session
Direct Billing: Remedy 02: Yes | Remedy 04: Yes
Reimbursement Allowed: Remedy 02: No | Remedy 04: No
Referral Required: Remedy 02: Yes | Remedy 04: Yes
Area of Coverage: Remedy 02: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval. | Remedy 04: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval.
Network: Remedy 02: HN Basic Plus | Remedy 04: HN Basic Plus (OP Restricted to Clinics) with direct access to below hospitals for OP Services. Aster Hospitals (Qusais, Mankhool, Jebel Ali) Burjeel Specialty Hospital Sharjah International Modern Hospital, DXB Ajman Specialty Hospital – Ajman Al Saha wa Al Shifaa Hospital For One Day Surgery – Sharjah Specialist Subject to GP Referral both in Clinics and Hospitals

Both plans are similar overall, but differ in: Pharmacy: Remedy 02=Maximum AED 3,000/year 30% payable by member on each prescription. Any medication in excess of the annual limit will not be covered, Remedy 04=Maximum AED 7,500/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered, Diagnostics: Remedy 02=Lab tests: 15% co-pay applied at the time of payment Covered.; Radiology: 15% co-pay applied at the time of payment, Remedy 04=Lab tests: NIL co-pay applied at the time of payment Covered.; Radiology: NIL co-pay applied at the time of payment, Physiotherapy: Remedy 02=Covered for a maximum of 12 sessions per year 15% co-pay per session, Remedy 04=Covered for a maximum of 12 sessions per year NIL co-pay per session, Network: Remedy 02=HN Basic Plus, Remedy 04=HN Basic Plus (OP Restricted to Clinics) with direct access to below hospitals for OP Services. Aster Hospitals (Qusais, Mankhool, Jebel Ali) Burjeel Specialty Hospital Sharjah International Modern Hospital, DXB Ajman Specialty Hospital – Ajman Al Saha wa Al Shifaa Hospital For One Day Surgery – Sharjah Specialist Subject to GP Referral both in Clinics and Hospitals.

Recommendation:
Remedy 04 is generally better if your client is looking for stronger outpatient benefits:
- Higher pharmacy limit (AED 7,500 vs 3,000)
- Stronger diagnostics benefits
```
#### 54. Compare Classic 2 and Classic 3
- intent: plan_comparison
- tool: compare_plans
- plan: Classic 2 vs Classic 3
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Comparison between Classic 2 and Classic 3:
Annual Limit: Classic 2: AED 250,000 | Classic 3: AED 250,000
Direct Billing: Classic 2: Yes | Classic 3: Yes
Referral Required: Classic 2: No | Classic 3: No
Area of Coverage: Classic 2: Worldwide Excluding USA and Canada | Classic 3: UAE+Home country
Network: Classic 2: Standard Plus | Classic 3: Standard

Both plans are similar overall, but differ in: Area of Coverage: Classic 2=Worldwide Excluding USA and Canada, Classic 3=UAE+Home country, Network: Classic 2=Standard Plus, Classic 3=Standard.

Recommendation:
Both plans are very similar in their key benefits.
```
#### 55. Compare Classic 2R and Classic 3
- intent: plan_comparison
- tool: None
- plan: Classic 2R vs Classic 3
- classification: BLOCKED_OK
- reason: Comparison boundary/safety block triggered as expected.
- output:
```text
Sorry, comparison is not supported or not available for one or both plans.
```
#### 56. Compare Classic 2 and Classic 2R
- intent: plan_comparison
- tool: None
- plan: Classic 2R vs Classic 2
- classification: BLOCKED_OK
- reason: Comparison boundary/safety block triggered as expected.
- output:
```text
Sorry, comparison is not supported or not available for one or both plans.
```
#### 57. Compare Classic 2R and Remedy 05
- intent: plan_comparison
- tool: None
- plan: Classic 2R vs Remedy 05
- classification: BLOCKED_OK
- reason: Comparison boundary/safety block triggered as expected.
- output:
```text
Sorry, comparison is not supported or not available for one or both plans.
```
#### 58. Compare Remedy 4 and Remedy 5
- intent: plan_comparison
- tool: compare_plans
- plan: Remedy 04 vs Remedy 05
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Comparison between Remedy 04 and Remedy 05:
Annual Limit: Remedy 04: AED. 150,000 | Remedy 05: AED. 150,000
Pharmacy: Remedy 04: Maximum AED 7,500/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered | Remedy 05: Maximum AED 7,500/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered
Diagnostics: Remedy 04: Lab tests: NIL co-pay applied at the time of payment Covered.; Radiology: NIL co-pay applied at the time of payment | Remedy 05: Lab tests: NIL co-pay applied at the time of payment Covered.; Radiology: NIL co-pay applied at the time of payment
Physiotherapy: Remedy 04: Covered for a maximum of 12 sessions per year NIL co-pay per session | Remedy 05: Covered for a maximum of 12 sessions per year NIL co-pay per session
Direct Billing: Remedy 04: Yes | Remedy 05: Yes
Reimbursement Allowed: Remedy 04: No | Remedy 05: Yes
Referral Required: Remedy 04: Yes | Remedy 05: No
Area of Coverage: Remedy 04: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval. | Remedy 05: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval.
Network: Remedy 04: HN Basic Plus (OP Restricted to Clinics) with direct access to below hospitals for OP Services. Aster Hospitals (Qusais, Mankhool, Jebel Ali) Burjeel Specialty Hospital Sharjah International Modern Hospital, DXB Ajman Specialty Hospital – Ajman Al Saha wa Al Shifaa Hospital For One Day Surgery – Sharjah Specialist Subject to GP Referral both in Clinics and Hospitals | Remedy 05: HN Basic Plus

Both plans are similar overall, but differ in: Reimbursement Allowed: Remedy 04=No, Remedy 05=Yes, Referral Required: Remedy 04=Yes, Remedy 05=No, Network: Remedy 04=HN Basic Plus (OP Restricted to Clinics) with direct access to below hospitals for OP Services. Aster Hospitals (Qusais, Mankhool, Jebel Ali) Burjeel Specialty Hospital Sharjah International Modern Hospital, DXB Ajman Specialty Hospital – Ajman Al Saha wa Al Shifaa Hospital For One Day Surgery – Sharjah Specialist Subject to GP Referral both in Clinics and Hospitals, Remedy 05=HN Basic Plus.

Recommendation:
Both plans are very similar in their key benefits.
```
#### 59. قارن بين Remedy 4 و Remedy 5
- intent: plan_comparison
- tool: compare_plans
- plan: Remedy 04 vs Remedy 05
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
مقارنة بين Remedy 04 و Remedy 05:
الحد السنوي: Remedy 04: AED. 150,000 | Remedy 05: AED. 150,000
الصيدلة: Remedy 04: Maximum AED 7,500/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered | Remedy 05: Maximum AED 7,500/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered
التشخيص: Remedy 04: Lab tests: NIL co-pay applied at the time of payment Covered.; Radiology: NIL co-pay applied at the time of payment | Remedy 05: Lab tests: NIL co-pay applied at the time of payment Covered.; Radiology: NIL co-pay applied at the time of payment
العلاج الطبيعي: Remedy 04: Covered for a maximum of 12 sessions per year NIL co-pay per session | Remedy 05: Covered for a maximum of 12 sessions per year NIL co-pay per session
الدفع المباشر: Remedy 04: Yes | Remedy 05: Yes
التعويض: Remedy 04: No | Remedy 05: Yes
الإحالة: Remedy 04: Yes | Remedy 05: No
نطاق التغطية: Remedy 04: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval. | Remedy 05: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval.
الشبكة: Remedy 04: HN Basic Plus (OP Restricted to Clinics) with direct access to below hospitals for OP Services. Aster Hospitals (Qusais, Mankhool, Jebel Ali) Burjeel Specialty Hospital Sharjah International Modern Hospital, DXB Ajman Specialty Hospital – Ajman Al Saha wa Al Shifaa Hospital For One Day Surgery – Sharjah Specialist Subject to GP Referral both in Clinics and Hospitals | Remedy 05: HN Basic Plus

Both plans are similar overall, but differ in: Reimbursement Allowed: Remedy 04=No, Remedy 05=Yes, Referral Required: Remedy 04=Yes, Remedy 05=No, Network: Remedy 04=HN Basic Plus (OP Restricted to Clinics) with direct access to below hospitals for OP Services. Aster Hospitals (Qusais, Mankhool, Jebel Ali) Burjeel Specialty Hospital Sharjah International Modern Hospital, DXB Ajman Specialty Hospital – Ajman Al Saha wa Al Shifaa Hospital For One Day Surgery – Sharjah Specialist Subject to GP Referral both in Clinics and Hospitals, Remedy 05=HN Basic Plus.

Recommendation:
Both plans are very similar in their key benefits.
```
#### 60. مقارنة بين Remedy 04 و Remedy 05
- intent: plan_comparison
- tool: compare_plans
- plan: Remedy 04 vs Remedy 05
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
مقارنة بين Remedy 04 و Remedy 05:
الحد السنوي: Remedy 04: AED. 150,000 | Remedy 05: AED. 150,000
الصيدلة: Remedy 04: Maximum AED 7,500/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered | Remedy 05: Maximum AED 7,500/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered
التشخيص: Remedy 04: Lab tests: NIL co-pay applied at the time of payment Covered.; Radiology: NIL co-pay applied at the time of payment | Remedy 05: Lab tests: NIL co-pay applied at the time of payment Covered.; Radiology: NIL co-pay applied at the time of payment
العلاج الطبيعي: Remedy 04: Covered for a maximum of 12 sessions per year NIL co-pay per session | Remedy 05: Covered for a maximum of 12 sessions per year NIL co-pay per session
الدفع المباشر: Remedy 04: Yes | Remedy 05: Yes
التعويض: Remedy 04: No | Remedy 05: Yes
الإحالة: Remedy 04: Yes | Remedy 05: No
نطاق التغطية: Remedy 04: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval. | Remedy 05: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval.
الشبكة: Remedy 04: HN Basic Plus (OP Restricted to Clinics) with direct access to below hospitals for OP Services. Aster Hospitals (Qusais, Mankhool, Jebel Ali) Burjeel Specialty Hospital Sharjah International Modern Hospital, DXB Ajman Specialty Hospital – Ajman Al Saha wa Al Shifaa Hospital For One Day Surgery – Sharjah Specialist Subject to GP Referral both in Clinics and Hospitals | Remedy 05: HN Basic Plus

Both plans are similar overall, but differ in: Reimbursement Allowed: Remedy 04=No, Remedy 05=Yes, Referral Required: Remedy 04=Yes, Remedy 05=No, Network: Remedy 04=HN Basic Plus (OP Restricted to Clinics) with direct access to below hospitals for OP Services. Aster Hospitals (Qusais, Mankhool, Jebel Ali) Burjeel Specialty Hospital Sharjah International Modern Hospital, DXB Ajman Specialty Hospital – Ajman Al Saha wa Al Shifaa Hospital For One Day Surgery – Sharjah Specialist Subject to GP Referral both in Clinics and Hospitals, Remedy 05=HN Basic Plus.

Recommendation:
Both plans are very similar in their key benefits.
```
#### 61. الفرق بين Classic 2 و Classic 3
- intent: plan_comparison
- tool: compare_plans
- plan: Classic 2 vs Classic 3
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
مقارنة بين Classic 2 و Classic 3:
الحد السنوي: Classic 2: AED 250,000 | Classic 3: AED 250,000
الدفع المباشر: Classic 2: Yes | Classic 3: Yes
الإحالة: Classic 2: No | Classic 3: No
نطاق التغطية: Classic 2: Worldwide Excluding USA and Canada | Classic 3: UAE+Home country
الشبكة: Classic 2: Standard Plus | Classic 3: Standard

Both plans are similar overall, but differ in: Area of Coverage: Classic 2=Worldwide Excluding USA and Canada, Classic 3=UAE+Home country, Network: Classic 2=Standard Plus, Classic 3=Standard.

Recommendation:
Both plans are very similar in their key benefits.
```
#### 62. قارن بين Remedy 4 و Plan X
- intent: plan_comparison
- tool: None
- plan: None
- classification: BLOCKED_OK
- reason: Comparison boundary/safety block triggered as expected.
- output:
```text
يرجى تحديد خطتين مدعومتين للمقارنة.
```
#### 63. Compare Classic 2 and Plan X
- intent: plan_comparison
- tool: None
- plan: None
- classification: BLOCKED_OK
- reason: Comparison boundary/safety block triggered as expected.
- output:
```text
Comparison is not supported or not available for one or both plans. Please specify two supported plans to compare.
```
#### 64. compare all plans
- intent: unsupported
- tool: None
- plan: None
- classification: REVIEW
- reason: Unsupported phrasing or out-of-scope query needs triage.
- output:
```text
Sorry, this query is not supported or not available. Please specify a supported plan or question.
```
#### 65. Which plan is better, Classic 2 or Classic 3?
- intent: plan_comparison
- tool: compare_plans
- plan: Classic 2 vs Classic 3
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Comparison between Classic 2 and Classic 3:
Annual Limit: Classic 2: AED 250,000 | Classic 3: AED 250,000
Direct Billing: Classic 2: Yes | Classic 3: Yes
Referral Required: Classic 2: No | Classic 3: No
Area of Coverage: Classic 2: Worldwide Excluding USA and Canada | Classic 3: UAE+Home country
Network: Classic 2: Standard Plus | Classic 3: Standard

Both plans are similar overall, but differ in: Area of Coverage: Classic 2=Worldwide Excluding USA and Canada, Classic 3=UAE+Home country, Network: Classic 2=Standard Plus, Classic 3=Standard.

Recommendation:
Both plans are very similar in their key benefits.
```
#### 66. Can you compare all enhanced plans?
- intent: unsupported
- tool: None
- plan: None
- classification: REVIEW
- reason: Unsupported phrasing or out-of-scope query needs triage.
- output:
```text
Sorry, this query is not supported or not available. Please specify a supported plan or question.
```
#### 67. ما الفرق بين ريميدي 02 و ريميدي 04
- intent: plan_comparison
- tool: compare_plans
- plan: Remedy 02 vs Remedy 04
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
مقارنة بين Remedy 02 و Remedy 04:
الحد السنوي: Remedy 02: AED. 150,000 | Remedy 04: AED. 150,000
الصيدلة: Remedy 02: Maximum AED 3,000/year 30% payable by member on each prescription. Any medication in excess of the annual limit will not be covered | Remedy 04: Maximum AED 7,500/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered
التشخيص: Remedy 02: Lab tests: 15% co-pay applied at the time of payment Covered.; Radiology: 15% co-pay applied at the time of payment | Remedy 04: Lab tests: NIL co-pay applied at the time of payment Covered.; Radiology: NIL co-pay applied at the time of payment
العلاج الطبيعي: Remedy 02: Covered for a maximum of 12 sessions per year 15% co-pay per session | Remedy 04: Covered for a maximum of 12 sessions per year NIL co-pay per session
الدفع المباشر: Remedy 02: Yes | Remedy 04: Yes
التعويض: Remedy 02: No | Remedy 04: No
الإحالة: Remedy 02: Yes | Remedy 04: Yes
نطاق التغطية: Remedy 02: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval. | Remedy 04: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval.
الشبكة: Remedy 02: HN Basic Plus | Remedy 04: HN Basic Plus (OP Restricted to Clinics) with direct access to below hospitals for OP Services. Aster Hospitals (Qusais, Mankhool, Jebel Ali) Burjeel Specialty Hospital Sharjah International Modern Hospital, DXB Ajman Specialty Hospital – Ajman Al Saha wa Al Shifaa Hospital For One Day Surgery – Sharjah Specialist Subject to GP Referral both in Clinics and Hospitals

Both plans are similar overall, but differ in: Pharmacy: Remedy 02=Maximum AED 3,000/year 30% payable by member on each prescription. Any medication in excess of the annual limit will not be covered, Remedy 04=Maximum AED 7,500/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered, Diagnostics: Remedy 02=Lab tests: 15% co-pay applied at the time of payment Covered.; Radiology: 15% co-pay applied at the time of payment, Remedy 04=Lab tests: NIL co-pay applied at the time of payment Covered.; Radiology: NIL co-pay applied at the time of payment, Physiotherapy: Remedy 02=Covered for a maximum of 12 sessions per year 15% co-pay per session, Remedy 04=Covered for a maximum of 12 sessions per year NIL co-pay per session, Network: Remedy 02=HN Basic Plus, Remedy 04=HN Basic Plus (OP Restricted to Clinics) with direct access to below hospitals for OP Services. Aster Hospitals (Qusais, Mankhool, Jebel Ali) Burjeel Specialty Hospital Sharjah International Modern Hospital, DXB Ajman Specialty Hospital – Ajman Al Saha wa Al Shifaa Hospital For One Day Surgery – Sharjah Specialist Subject to GP Referral both in Clinics and Hospitals.

Recommendation:
Remedy 04 is generally better if your client is looking for stronger outpatient benefits:
- Higher pharmacy limit (AED 7,500 vs 3,000)
- Stronger diagnostics benefits
```
#### 68. ايه الفرق بين Remedy 04 و Remedy 05
- intent: plan_comparison
- tool: compare_plans
- plan: Remedy 04 vs Remedy 05
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
مقارنة بين Remedy 04 و Remedy 05:
الحد السنوي: Remedy 04: AED. 150,000 | Remedy 05: AED. 150,000
الصيدلة: Remedy 04: Maximum AED 7,500/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered | Remedy 05: Maximum AED 7,500/year (including co-pay). 20% payable by member on each prescription. Any medication in excess of the annual limit will not be covered
التشخيص: Remedy 04: Lab tests: NIL co-pay applied at the time of payment Covered.; Radiology: NIL co-pay applied at the time of payment | Remedy 05: Lab tests: NIL co-pay applied at the time of payment Covered.; Radiology: NIL co-pay applied at the time of payment
العلاج الطبيعي: Remedy 04: Covered for a maximum of 12 sessions per year NIL co-pay per session | Remedy 05: Covered for a maximum of 12 sessions per year NIL co-pay per session
الدفع المباشر: Remedy 04: Yes | Remedy 05: Yes
التعويض: Remedy 04: No | Remedy 05: Yes
الإحالة: Remedy 04: Yes | Remedy 05: No
نطاق التغطية: Remedy 04: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval. | Remedy 05: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong & Singapore) for Elective & Emergency Treatments. Elective IP treatment outside UAE is subject to prior approval.
الشبكة: Remedy 04: HN Basic Plus (OP Restricted to Clinics) with direct access to below hospitals for OP Services. Aster Hospitals (Qusais, Mankhool, Jebel Ali) Burjeel Specialty Hospital Sharjah International Modern Hospital, DXB Ajman Specialty Hospital – Ajman Al Saha wa Al Shifaa Hospital For One Day Surgery – Sharjah Specialist Subject to GP Referral both in Clinics and Hospitals | Remedy 05: HN Basic Plus

Both plans are similar overall, but differ in: Reimbursement Allowed: Remedy 04=No, Remedy 05=Yes, Referral Required: Remedy 04=Yes, Remedy 05=No, Network: Remedy 04=HN Basic Plus (OP Restricted to Clinics) with direct access to below hospitals for OP Services. Aster Hospitals (Qusais, Mankhool, Jebel Ali) Burjeel Specialty Hospital Sharjah International Modern Hospital, DXB Ajman Specialty Hospital – Ajman Al Saha wa Al Shifaa Hospital For One Day Surgery – Sharjah Specialist Subject to GP Referral both in Clinics and Hospitals, Remedy 05=HN Basic Plus.

Recommendation:
Both plans are very similar in their key benefits.
```
#### 69. قارن بين Classic 2R و Classic 2
- intent: plan_comparison
- tool: None
- plan: Classic 2R vs Classic 2
- classification: REVIEW
- reason: Needs manual review for routing/wording/support classification.
- output:
```text
ط¹ط°ط±ط§ظ‹طŒ ط§ظ„ظ…ظ‚ط§ط±ظ†ط© ط؛ظٹط± ظ…ط¯ط¹ظˆظ…ط© ط£ظˆ ط؛ظٹط± ظ…طھط§ط­ط© ظ„ط®ط·ط© ط£ظˆ ط£ظƒط«ط±.
```
#### 70. Compare Remedy 06 and Classic 3
- intent: plan_comparison
- tool: None
- plan: Remedy 06 vs Classic 3
- classification: BLOCKED_OK
- reason: Comparison boundary/safety block triggered as expected.
- output:
```text
Sorry, comparison is not supported or not available for one or both plans.
```

### recommendation_questions
#### 71. Which plan is better for Dubai?
- intent: unsupported
- tool: None
- plan: None
- classification: REVIEW
- reason: Unsupported phrasing or out-of-scope query needs triage.
- output:
```text
Sorry, this query is not supported or not available. Please specify a supported plan or question.
```
#### 72. Which enhanced plan should I offer?
- intent: unsupported
- tool: None
- plan: None
- classification: BLOCKED_OK
- reason: Recommendation intent intentionally blocked in deterministic scope.
- output:
```text
Sorry, this query is not supported or not available. Please specify a supported plan or question.
```
#### 73. best enhanced plan overall
- intent: unsupported
- tool: None
- plan: None
- classification: BLOCKED_OK
- reason: Recommendation intent intentionally blocked in deterministic scope.
- output:
```text
Sorry, this query is not supported or not available. Please specify a supported plan or question.
```
#### 74. Which plan should I recommend to a family?
- intent: unsupported
- tool: None
- plan: None
- classification: BLOCKED_OK
- reason: Recommendation intent intentionally blocked in deterministic scope.
- output:
```text
Sorry, this query is not supported or not available. Please specify a supported plan or question.
```
#### 75. Should I offer Classic 2R or Classic 3?
- intent: plan_comparison
- tool: None
- plan: Classic 2R vs Classic 3
- classification: BLOCKED_OK
- reason: Comparison boundary/safety block triggered as expected.
- output:
```text
Sorry, comparison is not supported or not available for one or both plans.
```
#### 76. What is the best value plan?
- intent: unsupported
- tool: None
- plan: None
- classification: REVIEW
- reason: Unsupported phrasing or out-of-scope query needs triage.
- output:
```text
Sorry, this query is not supported or not available. Please specify a supported plan or question.
```
#### 77. Recommend one plan for outpatient heavy usage
- intent: unsupported
- tool: None
- plan: None
- classification: BLOCKED_OK
- reason: Recommendation intent intentionally blocked in deterministic scope.
- output:
```text
Sorry, this query is not supported or not available. Please specify a supported plan or question.
```
#### 78. Which plan do brokers usually sell most?
- intent: unsupported
- tool: None
- plan: None
- classification: REVIEW
- reason: Unsupported phrasing or out-of-scope query needs triage.
- output:
```text
Sorry, this query is not supported or not available. Please specify a supported plan or question.
```
#### 79. أفضل خطة بشكل عام؟
- intent: unsupported
- tool: None
- plan: None
- classification: BLOCKED_OK
- reason: Recommendation intent intentionally blocked in deterministic scope.
- output:
```text
عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم.
```
#### 80. تنصحني باي خطة؟
- intent: unsupported
- tool: None
- plan: None
- classification: BLOCKED_OK
- reason: Recommendation intent intentionally blocked in deterministic scope.
- output:
```text
عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم.
```

### arabic_mixed_questions
#### 81. كلاسيك 2R network?
- intent: plan_core
- tool: get_plan_core
- plan: Classic 2R
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 2R
Code: HN_CLASSIC_2R
الشبكة: Standard Plus
Annual limit: AED 250,000
Area: Worldwide Excluding USA and Canada
Direct billing: Yes
Referral required: No
```
#### 82. classic3 referral?
- intent: plan_core
- tool: get_plan_core
- plan: Classic 3
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 3
Code: HN_CLASSIC_3
الشبكة: Standard
Annual limit: AED 250,000
Area: UAE+Home country
Direct billing: Yes
Referral required: No
```
#### 83. direct billing في كلاسيك 3؟
- intent: plan_core
- tool: get_plan_core
- plan: Classic 3
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 3
Code: HN_CLASSIC_3
الشبكة: Standard
Annual limit: AED 250,000
Area: UAE+Home country
Direct billing: Yes
Referral required: No
```
#### 84. HN Classic 2R ليمت
- intent: plan_core
- tool: get_plan_core
- plan: Classic 2R
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 2R
Code: HN_CLASSIC_2R
الشبكة: Standard Plus
Annual limit: AED 250,000
Area: Worldwide Excluding USA and Canada
Direct billing: Yes
Referral required: No
```
#### 85. classic2r area of coverage
- intent: plan_core
- tool: get_plan_core
- plan: Classic 2R
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 2R
Code: HN_CLASSIC_2R
الشبكة: Standard Plus
Annual limit: AED 250,000
Area: Worldwide Excluding USA and Canada
Direct billing: Yes
Referral required: No
```
#### 86. شبكة Classic 2R
- intent: plan_core
- tool: get_plan_core
- plan: Classic 2R
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 2R
Code: HN_CLASSIC_2R
الشبكة: Standard Plus
Annual limit: AED 250,000
Area: Worldwide Excluding USA and Canada
Direct billing: Yes
Referral required: No
```
#### 87. Summarize كلاسيك 3
- intent: plan_summary
- tool: get_plan_summary
- plan: Classic 3
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 3
Code: HN_CLASSIC_3
Network: Standard
Annual limit: AED 250,000
Area: UAE+Home country
Direct billing: Yes
Referral required: No
```
#### 88. Classic 2R cashless?
- intent: plan_core
- tool: get_plan_core
- plan: Classic 2R
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 2R
Code: HN_CLASSIC_2R
الشبكة: Standard Plus
Annual limit: AED 250,000
Area: Worldwide Excluding USA and Canada
Direct billing: Yes
Referral required: No
```
#### 89. كلاسيك 3 annual limit
- intent: plan_core
- tool: get_plan_core
- plan: Classic 3
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 3
Code: HN_CLASSIC_3
الشبكة: Standard
Annual limit: AED 250,000
Area: UAE+Home country
Direct billing: Yes
Referral required: No
```
#### 90. ينفع استخدمها في مصر؟
- intent: unsupported
- tool: None
- plan: None
- classification: REVIEW
- reason: Unsupported phrasing or out-of-scope query needs triage.
- output:
```text
عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم.
```
#### 91. هل لازم referral في كلاسيك 3؟
- intent: plan_core
- tool: get_plan_core
- plan: Classic 3
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 3
Code: HN_CLASSIC_3
الشبكة: Standard
Annual limit: AED 250,000
Area: UAE+Home country
Direct billing: Yes
Referral required: No
```
#### 92. تغطية كلاسيك 3
- intent: plan_core
- tool: get_plan_core
- plan: Classic 3
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 3
Code: HN_CLASSIC_3
الشبكة: Standard
Annual limit: AED 250,000
Area: UAE+Home country
Direct billing: Yes
Referral required: No
```
#### 93. ليمت كلاسيك 2R
- intent: plan_core
- tool: get_plan_core
- plan: Classic 2R
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 2R
Code: HN_CLASSIC_2R
الشبكة: Standard Plus
Annual limit: AED 250,000
Area: Worldwide Excluding USA and Canada
Direct billing: Yes
Referral required: No
```
#### 94. هل يغطي الطوارئ في كلاسيك 2R؟
- intent: unsupported
- tool: None
- plan: Classic 2R
- classification: GAP
- reason: Benefit data exists in source but intentionally not exposed in runtime.
- output:
```text
عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم.
```
#### 95. هل يوجد direct billing في هذه العيادة؟
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: REVIEW
- reason: Provider lookup failed; likely alias/coverage limitation.
- output:
```text
Provider not found.
```
#### 96. هل هذه المستشفى ضمن الشبكة؟
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: REVIEW
- reason: Provider lookup failed; likely alias/coverage limitation.
- output:
```text
Provider not found.
```
#### 97. ما نوع المزود Burjeel Hospital؟
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Type for Burjeel Hospital: HOSPITAL
```
#### 98. في أي مدينة يقع Burjeel Hospital؟
- intent: network_lookup
- tool: network_lookup
- plan: None
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
City for Burjeel Hospital: ABU DHABI
```
#### 99. Burjeel Hospital في أي شبكة؟
- intent: unsupported
- tool: None
- plan: None
- classification: REVIEW
- reason: Unsupported phrasing or out-of-scope query needs triage.
- output:
```text
عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم.
```
#### 100. هل Classic 2 يحتاج referral
- intent: plan_core
- tool: get_plan_core
- plan: Classic 2
- classification: GOOD
- reason: Deterministic supported response returned.
- output:
```text
Plan: Classic 2
Code: HN_CLASSIC_2
الشبكة: Standard Plus
Annual limit: AED 250,000
Area: Worldwide Excluding USA and Canada
Direct billing: Yes
Referral required: No
```
