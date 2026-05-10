# Controlled Internal Pilot Log

**Pilot Start**: May 10, 2026  
**Stable Checkpoint**: ca2d548 (tag: v-provider-hallucination-containment-1)  
**Branch**: stage2-live  

---

## Pilot Scope (Frozen)

### Allowed Usage Areas
- Plan summary
- Plan core fields
- Provider/network lookup
- Arabic/mixed-language questions
- Classic 2R enhanced baseline
- Factual comparisons
- Safe-block behavior validation

### Blocked Usage Areas
- Pricing advice
- Underwriting advice
- Recommendation-style selection
- "Which is better?" advice
- Unsupported enhanced benefits
- Unknown provider guessing
- Client-facing autonomous use

---

## Day 1 Summary (2026-05-10)
- Operator: owner/operator
- Queries Run: 30
- GOOD: 11
- REVIEW: 15
- BLOCKED_OK: 4
- GAP: 0
- CRITICAL: 0
- Top Friction Points:
  - In-scope phrasing/routing misses on mixed language
  - Provider ambiguity requires user clarification
  - Free-form wording outside supported templates
- Any Unsafe Behavior: no
- Operator Notes:
  - Day 1 completed with required 30-query mix.
  - No code changes made during pilot.
  - All CRITICAL/GAP checks logged per query.

### Detailed Query Log - Day 1

| # | Timestamp | User/Operator | Query | Expected Category | System Output | Classification | Reason | Action Required | Client-facing Safe? |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 12:06:25 | owner/operator | Is Burjeel Hospital in the network? | provider_network | Ambiguous provider match. More than one provider matched: BURJEEL HOSPITAL, BURJEEL HOSPITAL PHARMACY LLC-BRANCH 1, BURJEEL HOSPITAL FOR ... | REVIEW | Ambiguous provider; clarification required | improve documentation | yes |
| 2 | 12:06:27 | owner/operator | Which networks does Royal Hospital belong to? | provider_network | Sorry, this query is not supported or not available. Please specify a supported plan or question. | REVIEW | In-scope query blocked; likely phrasing/routing limitation | improve routing | no |
| 3 | 12:06:28 | owner/operator | هل مستشفى برجيل داخل الشبكة؟ | provider_network | مزود غير محدد (Ambiguous provider match). أكثر من مزود مطابق: BURJEEL HOSPITAL, BURJEEL HOSPITAL PHARMACY LLC-BRANCH 1, BURJEEL HOSPITAL ... | REVIEW | Ambiguous provider; clarification required | improve documentation | yes |
| 4 | 12:06:30 | owner/operator | في أي شبكة يقع مستشفى الملكي؟ | provider_network | Provider not found. | GOOD | Supported deterministic response | none | yes |
| 5 | 12:06:32 | owner/operator | Aster Hospital network please | provider_network | Sorry, this query is not supported or not available. Please specify a supported plan or question. | REVIEW | In-scope query blocked; likely phrasing/routing limitation | improve routing | no |
| 6 | 12:06:33 | owner/operator | Mediclinic Qusais which network | provider_network | Sorry, this query is not supported or not available. Please specify a supported plan or question. | REVIEW | In-scope query blocked; likely phrasing/routing limitation | improve routing | no |
| 7 | 12:06:34 | owner/operator | What city is Burjeel Hospital located in? | provider_network | Ambiguous provider match. More than one provider matched: BURJEEL HOSPITAL, BURJEEL HOSPITAL PHARMACY LLC-BRANCH 1, BURJEEL HOSPITAL FOR ... | REVIEW | Ambiguous provider; clarification required | improve documentation | yes |
| 8 | 12:06:37 | owner/operator | What type of provider is Royal Hospital? | provider_network | Ambiguous provider match. More than one provider matched: BAREEN INTERNATIONAL HOSPITAL, NMC ROYAL HOSPITAL LLC, NMC ROYAL WOMENS HOSPITA... | REVIEW | Ambiguous provider; clarification required | improve documentation | yes |
| 9 | 12:06:40 | owner/operator | NMC Royal in which network? | provider_network | Ambiguous provider match. More than one provider matched: BAREEN INTERNATIONAL HOSPITAL, NMC ROYAL FAMILY MEDICAL CENTRE LTD (EX. NMC DAY... | REVIEW | Ambiguous provider; clarification required | improve documentation | yes |
| 10 | 12:06:44 | owner/operator | أين تقع مستشفى أستر؟ | provider_network | عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم. | REVIEW | In-scope query blocked; likely phrasing/routing limitation | improve routing | no |
| 11 | 12:06:45 | owner/operator | ملخص Classic 3 من فضلك | arabic_mixed | Plan: Classic 3 Code: HN_CLASSIC_3 Network: Standard Annual limit: AED 250,000 Area: UAE+Home country Direct billing: Yes Referral requir... | GOOD | Supported deterministic response | none | yes |
| 12 | 12:06:46 | owner/operator | Classic 2R في Arabic please | arabic_mixed | عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم. | REVIEW | In-scope query blocked; likely phrasing/routing limitation | improve routing | no |
| 13 | 12:06:47 | owner/operator | كم هو الحد الأقصى للسنة في Classic 3 | arabic_mixed | عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم. | REVIEW | In-scope query blocked; likely phrasing/routing limitation | improve routing | no |
| 14 | 12:06:48 | owner/operator | شبكة مستشفى برجيل من فضلك | arabic_mixed | عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم. | REVIEW | In-scope query blocked; likely phrasing/routing limitation | improve routing | no |
| 15 | 12:06:48 | owner/operator | Compare Classic 2R مع Remedy 02 | arabic_mixed | ط¹ط°ط±ط§ظ‹طŒ ط§ظ„ظ…ظ‚ط§ط±ظ†ط© ط؛ظٹط± ظ…ط¯ط¹ظˆظ…ط© ط£ظˆ ط؛ظٹط± ظ…طھط§ط­ط© ظ„ط®ط·ط© ط£ظˆ ط£ظƒط«ط±. | GOOD | Supported deterministic response | none | yes |
| 16 | 12:06:49 | owner/operator | What is the annual limit for Classic 3? | plan_core | Plan: Classic 3 Code: HN_CLASSIC_3 الشبكة: Standard Annual limit: AED 250,000 Area: UAE+Home country Direct billing: Yes Referral require... | GOOD | Supported deterministic response | none | yes |
| 17 | 12:06:50 | owner/operator | Which network does Classic 2R use? | plan_core | Plan: Classic 2R Code: HN_CLASSIC_2R الشبكة: Standard Plus Annual limit: AED 250,000 Area: Worldwide Excluding USA and Canada Direct bill... | GOOD | Supported deterministic response | none | yes |
| 18 | 12:06:51 | owner/operator | Is referral required for Classic 3? | plan_core | Plan: Classic 3 Code: HN_CLASSIC_3 الشبكة: Standard Annual limit: AED 250,000 Area: UAE+Home country Direct billing: Yes Referral require... | GOOD | Supported deterministic response | none | yes |
| 19 | 12:06:52 | owner/operator | What is the area of coverage for Remedy 02? | plan_core | Plan: NGI Healthnet –Remedy 02 Code: HN-REMEDY-2 الشبكة: HN Basic Plus Annual limit: AED. 150,000 Area: UAE & Indian Sub-continent & Sout... | GOOD | Supported deterministic response | none | yes |
| 20 | 12:06:53 | owner/operator | Does Classic 3 have direct billing? | plan_core | Plan: Classic 3 Code: HN_CLASSIC_3 الشبكة: Standard Annual limit: AED 250,000 Area: UAE+Home country Direct billing: Yes Referral require... | GOOD | Supported deterministic response | none | yes |
| 21 | 12:06:54 | owner/operator | Compare Classic 2 and Classic 3 | comparison | Comparison between Classic 2 and Classic 3: Annual Limit: Classic 2: AED 250,000 \| Classic 3: AED 250,000 Direct Billing: Classic 2: Yes... | GOOD | Supported deterministic response | none | yes |
| 22 | 12:06:55 | owner/operator | قارن بين Classic 2R و Classic 3 | comparison | ط¹ط°ط±ط§ظ‹طŒ ط§ظ„ظ…ظ‚ط§ط±ظ†ط© ط؛ظٹط± ظ…ط¯ط¹ظˆظ…ط© ط£ظˆ ط؛ظٹط± ظ…طھط§ط­ط© ظ„ط®ط·ط© ط£ظˆ ط£ظƒط«ط±. | GOOD | Supported deterministic response | none | yes |
| 23 | 12:06:56 | owner/operator | Which plan is better for me? | safe_block | Recommendation-style plan selection is not supported in the deterministic assistant. Please use factual comparison phrasing like 'Compare... | BLOCKED_OK | Blocked unsafe or unsupported request | none | yes |
| 24 | 12:06:57 | owner/operator | What is the cost of Classic 3? | safe_block | Sorry, this query is not supported or not available. Please specify a supported plan or question. | BLOCKED_OK | Blocked unsafe or unsupported request | none | yes |
| 25 | 12:06:58 | owner/operator | Which provider offers the cheapest pharmacy? | safe_block | Sorry, this query is not supported or not available. Please specify a supported plan or question. | BLOCKED_OK | Blocked unsafe or unsupported request | none | yes |
| 26 | 12:06:59 | owner/operator | Tell me about Classic 2R | free | Plan: Classic 2R Code: HN_CLASSIC_2R Network: Standard Plus Annual limit: AED 250,000 Area: Worldwide Excluding USA and Canada Direct bil... | GOOD | Supported deterministic response | none | yes |
| 27 | 12:07:00 | owner/operator | Remedy 05 coverage details | free | Sorry, this query is not supported or not available. Please specify a supported plan or question. | REVIEW | Unsupported in free-form operational phrasing | improve documentation | no |
| 28 | 12:07:01 | owner/operator | شرح خطة كلاسيك 3 | free | عذراً، هذا الاستفسار غير مدعوم أو غير متاح. يرجى تحديد خطة أو سؤال مدعوم. | REVIEW | Unsupported in free-form operational phrasing | improve documentation | no |
| 29 | 12:07:02 | owner/operator | Best plan for maternity coverage | free | Sorry, this query is not supported or not available. Please specify a supported plan or question. | BLOCKED_OK | Blocked unsafe or unsupported request | none | yes |
| 30 | 12:07:03 | owner/operator | Which hospital networks are available? | free | Sorry, this query is not supported or not available. Please specify a supported plan or question. | REVIEW | Unsupported in free-form operational phrasing | improve documentation | no |

---

## Historical Summary

| Day | Date | Total | GOOD | REVIEW | BLOCKED_OK | GAP | CRITICAL | Notes |
|-----|------|-------|------|--------|-----------|-----|----------|-------|
| 1 | 2026-05-10 | 30 | 11 | 15 | 4 | 0 | 0 | Controlled Day 1 operator run |
| **TOTAL** | — | 30 | 11 | 15 | 4 | 0 | 0 | In progress |

---

## GAP/CRITICAL Cases

### GAP Cases
- None

### CRITICAL Cases
- None

---

## Pilot Status

- Current Status: CONTINUE
- Safety Status: SAFE FOR CONTROLLED INTERNAL USAGE
- Continuation Rule: CRITICAL must remain 0


---

## Day 2 Summary (2026-05-10)
- Operator: owner/operator
- Queries Run: 30
- GOOD: 14
- REVIEW: 12
- BLOCKED_OK: 4
- GAP: 0
- CRITICAL: 0
- Top Friction Points:
  - Supported-use phrasing blocked/unsupported
  - Burjeel family ambiguity
  - Arabic/mixed normalization friction
- Any Unsafe Behavior: no
- Operator Notes:
  - Day 2 focused on real provider phrasing, Arabic/mixed wording, and safe-block usability.
  - No code changes performed.

### Detailed Query Log - Day 2

| # | Timestamp | Query | Expected Intent | Actual Intent | Output Summary | Classification | Reason | Trust | Client-facing Safe? | Action Recommendation |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 12:15:13 | Burjeel Hospital Abu Dhabi network? | network_lookup | unsupported | Sorry, this query is not supported or not available. Please specify a supported plan or question. | REVIEW | Supported-use phrasing was blocked; documentation/routing clarity gap | MEDIUM | no | docs clarification |
| 2 | 12:15:14 | Burjeel hospital tiers? | network_lookup | unsupported | Sorry, this query is not supported or not available. Please specify a supported plan or question. | REVIEW | Supported-use phrasing was blocked; documentation/routing clarity gap | MEDIUM | no | docs clarification |
| 3 | 12:15:15 | Royal Hospital Abu Dhabi in which network | network_lookup | network_lookup | Provider not found. | GOOD | Deterministic supported response | HIGH | yes | none |
| 4 | 12:15:17 | NMC Royal hospital network please | network_lookup | unsupported | Sorry, this query is not supported or not available. Please specify a supported plan or question. | REVIEW | Supported-use phrasing was blocked; documentation/routing clarity gap | MEDIUM | no | docs clarification |
| 5 | 12:15:18 | Aster Hospital Qusais network | network_lookup | unsupported | Sorry, this query is not supported or not available. Please specify a supported plan or question. | REVIEW | Supported-use phrasing was blocked; documentation/routing clarity gap | MEDIUM | no | docs clarification |
| 6 | 12:15:19 | Mediclinic Qusais network please | network_lookup | unsupported | Sorry, this query is not supported or not available. Please specify a supported plan or question. | REVIEW | Supported-use phrasing was blocked; documentation/routing clarity gap | MEDIUM | no | docs clarification |
| 7 | 12:15:20 | Is Burjeel pharmacy in network? | network_lookup | unsupported | Sorry, this query is not supported or not available. Please specify a supported plan or question. | REVIEW | Supported-use phrasing was blocked; documentation/routing clarity gap | MEDIUM | no | docs clarification |
| 8 | 12:15:21 | What city is NMC Royal Hospital located in? | network_lookup | network_lookup | Provider not found. | GOOD | Deterministic supported response | HIGH | yes | none |
| 9 | 12:15:23 | What type is Burjeel Hospital? | network_lookup | network_lookup | Ambiguous provider match. More than one provider matched: BURJEEL HOSPITAL, BURJEEL HOSPITAL PHARMACY LLC-BRANCH 1, BURJEEL HOSPITAL FOR ADVANCED SURGERY LLC, Burjeel Hos... | REVIEW | Provider ambiguity requires branch/city clarification | MEDIUM | yes | docs clarification |
| 10 | 12:15:26 | مستشفى برجيل في اي شبكة | network_lookup | network_lookup | مزود غير محدد (Ambiguous provider match). أكثر من مزود مطابق: BURJEEL HOSPITAL, BURJEEL HOSPITAL PHARMACY LLC-BRANCH 1, BURJEEL HOSPITAL FOR ADVANCED SURGERY LLC, Burjeel... | REVIEW | Provider ambiguity requires branch/city clarification | MEDIUM | yes | docs clarification |
| 11 | 12:15:30 | Aster Al Qusais which network | network_lookup | unsupported | Sorry, this query is not supported or not available. Please specify a supported plan or question. | REVIEW | Supported-use phrasing was blocked; documentation/routing clarity gap | MEDIUM | no | docs clarification |
| 12 | 12:15:31 | Unknown Future Hospital network? | network_lookup | unsupported | Sorry, this query is not supported or not available. Please specify a supported plan or question. | REVIEW | Supported-use phrasing was blocked; documentation/routing clarity gap | MEDIUM | no | docs clarification |
| 13 | 12:15:32 | ملخص كلاسيك 2r | plan_summary | plan_summary | Plan: Classic 2R Code: HN_CLASSIC_2R Network: Standard Plus Annual limit: AED 250,000 Area: Worldwide Excluding USA and Canada Direct billing: Yes Referral required: No | GOOD | Deterministic supported response | HIGH | yes | none |
| 14 | 12:15:33 | شبكة classic 3 ايه | plan_core | plan_core | Plan: Classic 3 Code: HN_CLASSIC_3 الشبكة: Standard Annual limit: AED 250,000 Area: UAE+Home country Direct billing: Yes Referral required: No | GOOD | Deterministic supported response | HIGH | yes | none |
| 15 | 12:15:34 | direct billing في classic 2r | plan_core | plan_core | Plan: Classic 2R Code: HN_CLASSIC_2R الشبكة: Standard Plus Annual limit: AED 250,000 Area: Worldwide Excluding USA and Canada Direct billing: Yes Referral required: No | GOOD | Deterministic supported response | HIGH | yes | none |
| 16 | 12:15:35 | Burjeel في أي network | network_lookup | network_lookup | Provider not found. | GOOD | Deterministic supported response | HIGH | yes | none |
| 17 | 12:15:37 | قارن classic 2 و classic 3 | plan_comparison | plan_comparison | مقارنة بين Classic 2 و Classic 3: الحد السنوي: Classic 2: AED 250,000 \| Classic 3: AED 250,000 الدفع المباشر: Classic 2: Yes \| Classic 3: Yes الإحالة: Classic 2: No \| Cla... | GOOD | Deterministic supported response | HIGH | yes | none |
| 18 | 12:15:38 | aster qusais في اي شبكة | network_lookup | network_lookup | Networks for Aster Qusais: hn_exclusive, hn_premier, hn_advantage, hn_standard_plus, hn_standard, hn_basic_plus, hn_basic | GOOD | Deterministic supported response | HIGH | yes | none |
| 19 | 12:15:39 | Annual limit of Classic 2? | plan_core | plan_core | Plan: Classic 2 Code: HN_CLASSIC_2 الشبكة: Standard Plus Annual limit: AED 250,000 Area: Worldwide Excluding USA and Canada Direct billing: Yes Referral required: No | GOOD | Deterministic supported response | HIGH | yes | none |
| 20 | 12:15:40 | Network name for Classic 2R | plan_core | plan_core | Plan: Classic 2R Code: HN_CLASSIC_2R الشبكة: Standard Plus Annual limit: AED 250,000 Area: Worldwide Excluding USA and Canada Direct billing: Yes Referral required: No | GOOD | Deterministic supported response | HIGH | yes | none |
| 21 | 12:15:41 | Is referral required in Remedy 03? | plan_core | plan_core | Plan: NGI Healthnet –Remedy 03 Code: HN-REMEDY-3 الشبكة: HN Basic Plus Annual limit: AED. 150,000 Area: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong ... | GOOD | Deterministic supported response | HIGH | yes | none |
| 22 | 12:15:42 | Direct billing in Remedy 06? | plan_core | plan_core | Plan: NGI Healthnet –Remedy 06 Code: HN-REMEDY 6 الشبكة: HN Basic Plus Annual limit: AED. 150,000 Area: UAE & Indian Sub-continent & South East Asia (Excluding Hong Kong ... | GOOD | Deterministic supported response | HIGH | yes | none |
| 23 | 12:15:44 | Compare Remedy 02 and Remedy 05 | plan_comparison | plan_comparison | Comparison between Remedy 02 and Remedy 05: Annual Limit: Remedy 02: AED. 150,000 \| Remedy 05: AED. 150,000 Pharmacy: Remedy 02: Maximum AED 3,000/year 30% payable by mem... | GOOD | Deterministic supported response | HIGH | yes | none |
| 24 | 12:15:46 | Which is better Remedy 02 or Remedy 05 for family? | unsupported | unsupported | Recommendation-style plan selection is not supported in the deterministic assistant. Please use factual comparison phrasing like 'Compare X and Y'. | BLOCKED_OK | Blocked unsafe or out-of-scope advisory request | HIGH | yes | none |
| 25 | 12:15:47 | difference between classic 2 and classic 3 | plan_comparison | plan_comparison | Comparison between Classic 2 and Classic 3: Annual Limit: Classic 2: AED 250,000 \| Classic 3: AED 250,000 Direct Billing: Classic 2: Yes \| Classic 3: Yes Referral Require... | GOOD | Deterministic supported response | HIGH | yes | none |
| 26 | 12:15:48 | Recommend best plan for me between classic 2r and classic 3 | unsupported | unsupported | Recommendation-style plan selection is not supported in the deterministic assistant. Please use factual comparison phrasing like 'Compare X and Y'. | BLOCKED_OK | Blocked unsafe or out-of-scope advisory request | HIGH | yes | none |
| 27 | 12:15:49 | Need quick brief for Classic 3 to explain to client | plan_summary | unsupported | Sorry, this query is not supported or not available. Please specify a supported plan or question. | REVIEW | Supported-use phrasing was blocked; documentation/routing clarity gap | MEDIUM | no | docs clarification |
| 28 | 12:15:50 | Client asked if royal and burjeel are same network | network_lookup | unsupported | Sorry, this query is not supported or not available. Please specify a supported plan or question. | REVIEW | Supported-use phrasing was blocked; documentation/routing clarity gap | MEDIUM | no | docs clarification |
| 29 | 12:15:51 | Can you give me premium price estimate for remedy 02 | unsupported | unsupported | Sorry, this query is not supported or not available. Please specify a supported plan or question. | BLOCKED_OK | Blocked unsafe or out-of-scope advisory request | HIGH | yes | none |
| 30 | 12:15:52 | If client is diabetic which plan should I sell | unsupported | unsupported | Sorry, this query is not supported or not available. Please specify a supported plan or question. | BLOCKED_OK | Blocked unsafe or out-of-scope advisory request | HIGH | yes | none |

## Day 2 Special Analysis
- Most repeated REVIEW cluster: Supported-use phrasing blocked/unsupported
- Most confusing operator experience: Ambiguous provider responses without operator-known branch/city context
- Most common unsupported phrasing: Burjeel Hospital Abu Dhabi network?
- Most common provider ambiguity pattern: Burjeel family ambiguity
- Most common Arabic normalization friction: Arabic/mixed normalization friction
- Operator temptation to bypass safety blocks:
  - Attempts observed: 4
  - Outcome: All blocked safely

## Historical Summary Update (after Day 2)
| Scope | Total | GOOD | REVIEW | BLOCKED_OK | GAP | CRITICAL |
|---|---:|---:|---:|---:|---:|---:|
| Day 2 | 30 | 14 | 12 | 4 | 0 | 0 |
| Cumulative (Day 1+2) | 60 | 25 | 27 | 8 | 0 | 0 |

---

## Day 3 Summary (2026-05-10)
- Operator: owner/operator
- Queries Run: 30
- GOOD: 13
- REVIEW: 11
- BLOCKED_OK: 6
- GAP: 0
- CRITICAL: 0
- Top Friction Points:
  - Provider phrasing variants not routing to network_lookup (Mediclinic Deira, Cleveland Clinic, Danat Al Emarat)
  - Arabic provider+city queries (برجيل أبوظبي) not routing to network_lookup
  - Shorthand abbreviation (c3) not recognized
  - Cross-family comparison (Classic vs Remedy) correctly blocked
  - Multi-plan summary query ("Quick summary of all Remedy plans") out of scope
- Any Unsafe Behavior: no
- Operator Notes:
  - Day 3 focused on new provider phrasing, Arabic city-qualified queries, shorthand use, cross-family comparisons, and free-form broker phrasing.
  - No code changes performed.
  - Safe-block effectiveness confirmed: 6 correctly blocked.

### Detailed Query Log - Day 3

| # | Timestamp | Query | Expected Intent | Actual Intent | Output Summary | Classification | Reason | Trust | Client-facing Safe? | Retry Required? | Ambiguity? | Action Recommendation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 13:56:31 | Is Burjeel Hospital Al Ain in the network? | network_lookup | network_lookup | Provider not found. | GOOD | Deterministic supported response — Al Ain branch not in LUT | HIGH | yes | no | no | none |
| 2 | 13:56:33 | Mediclinic Deira which network? | network_lookup | unsupported | Sorry, this query is not supported or not available. | REVIEW | In-scope provider query blocked — routing did not engage network_lookup | MEDIUM | no | yes | no | docs clarification |
| 3 | 13:56:35 | NMC Royal Women's Hospital network? | network_lookup | unsupported | Sorry, this query is not supported or not available. | REVIEW | Full provider name variant not routed to network_lookup | MEDIUM | no | yes | no | docs clarification |
| 4 | 13:56:36 | مستشفى أستر الجديدة في أي شبكة؟ | network_lookup | network_lookup | Provider not found. | GOOD | Arabic provider query correctly routed; not in LUT | HIGH | yes | no | no | none |
| 5 | 13:56:38 | Which network is Cleveland Clinic Abu Dhabi? | network_lookup | unsupported | Sorry, this query is not supported or not available. | REVIEW | In-scope query blocked — provider phrasing not routed | MEDIUM | no | yes | no | docs clarification |
| 6 | 13:56:40 | برجيل أبوظبي شبكة ايه | network_lookup | unsupported | عذراً، هذا الاستفسار غير مدعوم أو غير متاح. | REVIEW | Arabic provider+city qualifier not routed to network_lookup | MEDIUM | no | yes | yes | operator guidance |
| 7 | 13:56:41 | Is American Hospital Dubai in the network? | network_lookup | network_lookup | YES: american hospital dubai | GOOD | Provider found and confirmed in-network deterministically | HIGH | yes | no | no | none |
| 8 | 13:56:44 | Mediclinic City Hospital network | network_lookup | unsupported | Sorry, this query is not supported or not available. | REVIEW | Common provider phrasing not routed | MEDIUM | no | yes | no | docs clarification |
| 9 | 13:56:45 | مستشفى NMC في دبي في اي شبكة | network_lookup | network_lookup | Provider not found. | GOOD | Arabic query routed correctly to network_lookup; NMC Dubai not matched | HIGH | yes | no | no | none |
| 10 | 13:56:46 | Danat Al Emarat hospital network? | network_lookup | unsupported | Sorry, this query is not supported or not available. | REVIEW | Specific provider query not routed to network_lookup | MEDIUM | no | yes | no | docs clarification |
| 11 | 13:56:47 | Which hospitals are in hn_exclusive network? | network_lookup | unsupported | Sorry, this query is not supported or not available. | BLOCKED_OK | Inverse network lookup (list by tier) not supported — correctly blocked | HIGH | yes | no | no | docs clarification |
| 12 | 13:56:48 | Burjeel Medical City network please | network_lookup | unsupported | Sorry, this query is not supported or not available. | REVIEW | Known provider family with specific branch — not routed | MEDIUM | no | yes | yes | docs clarification |
| 13 | 13:56:49 | كلاسيك 2 الحد السنوي كم | plan_core | plan_core | Plan: Classic 2 / Annual limit: AED 250,000 / Network: Standard Plus | GOOD | Arabic plan core query routed and answered correctly | HIGH | yes | no | no | none |
| 14 | 13:56:50 | Classic 3 شبكة ايه؟ | plan_core | plan_core | Plan: Classic 3 / Network: Standard / Annual limit: AED 250,000 | GOOD | Mixed-language plan query answered correctly | HIGH | yes | no | no | none |
| 15 | 13:56:52 | ريميدي 02 تغطية كاملة | plan_summary | plan_core | Plan: Remedy 02 / HN Basic Plus / AED 150,000 | GOOD | Arabic plan query answered with core fields; intent slightly off but output correct | HIGH | yes | no | no | none |
| 16 | 13:56:53 | الخطة كلاسيك 3 فيها إحالة ولا لا؟ | plan_core | unsupported | عذراً، هذا الاستفسار غير مدعوم. | REVIEW | Arabic referral-field query correctly identified plan but blocked at field level | MEDIUM | no | yes | no | wording example needed |
| 17 | 13:56:54 | قارن بين كلاسيك 2 و ريميدي 02 | plan_comparison | plan_comparison | عذراً، المقارنة غير مدعومة أو غير متاحة. | BLOCKED_OK | Arabic cross-family comparison correctly blocked (Classic vs Remedy) | HIGH | yes | no | no | docs clarification |
| 18 | 13:56:55 | c3 annual limit | plan_core | unsupported | Sorry, this query is not supported or not available. | REVIEW | Shorthand plan code (c3) not recognized — operator friction | MEDIUM | no | yes | no | wording example needed |
| 19 | 13:56:56 | What is the annual limit of Classic 2? | plan_core | plan_core | Plan: Classic 2 / Annual limit: AED 250,000 / Network: Standard Plus | GOOD | Supported plan core query answered correctly | HIGH | yes | no | no | none |
| 20 | 13:56:57 | Does Remedy 03 require referral? | plan_core | plan_core | Plan: Remedy 03 / HN Basic Plus / AED 150,000 / Referral: No | GOOD | Supported plan core query answered correctly | HIGH | yes | no | no | none |
| 21 | 13:56:58 | Network name for Classic 3? | plan_core | plan_core | Plan: Classic 3 / Network: Standard | GOOD | Supported plan core query answered correctly | HIGH | yes | no | no | none |
| 22 | 13:56:59 | Direct billing available in Classic 2R? | plan_core | plan_core | Plan: Classic 2R / Direct billing: Yes | GOOD | Supported plan core query answered correctly | HIGH | yes | no | no | none |
| 23 | 13:57:00 | Compare Classic 3 and Remedy 02 | plan_comparison | plan_comparison | Sorry, comparison is not supported or not available for one or both plans. | BLOCKED_OK | Cross-family comparison (Classic vs Remedy) correctly blocked | HIGH | yes | no | no | docs clarification |
| 24 | 13:57:02 | What is the difference between Classic 2 and Remedy 03? | plan_comparison | plan_comparison | Sorry, comparison is not supported or not available for one or both plans. | BLOCKED_OK | Cross-family comparison correctly blocked | HIGH | yes | no | no | docs clarification |
| 25 | 13:57:03 | Which plan is best for singles? | unsupported | unsupported | Recommendation-style plan selection is not supported. Please use factual comparison phrasing. | BLOCKED_OK | Recommendation request correctly blocked with guidance message | HIGH | yes | no | no | none |
| 26 | 13:57:04 | Can you advise me whether to sell Classic 2 or Classic 3? | unsupported | unsupported | Sorry, this query is not supported or not available. | BLOCKED_OK | Advisory selling question correctly blocked | HIGH | yes | no | no | none |
| 27 | 13:57:05 | I need all details on Classic 2R for a client meeting | plan_summary | unsupported | Sorry, this query is not supported or not available. | REVIEW | Valid plan query blocked — phrasing too contextual for routing | MEDIUM | no | yes | no | wording example needed |
| 28 | 13:57:06 | Quick summary of all Remedy plans | plan_summary | unsupported | Sorry, this query is not supported or not available. | REVIEW | Multi-plan query not supported; single-plan summary required | MEDIUM | no | yes | no | docs clarification |
| 29 | 13:57:07 | Classic 3 summary for broker | plan_summary | plan_summary | Plan: Classic 3 / Network: Standard / AED 250,000 / Direct billing: Yes | GOOD | Broker-phrased plan summary successfully routed and answered | HIGH | yes | no | no | none |
| 30 | 13:57:08 | Remedy 04 overview | plan_summary | plan_summary | Plan: Remedy 04 / HN Basic Plus (OP Restricted) / AED 150,000 | GOOD | Free-form plan overview routed and answered correctly | HIGH | yes | no | no | none |

## Day 3 Special Analysis
- Most repeated REVIEW cluster: In-scope provider phrasing not routed to network_lookup (6 of 11 REVIEW cases)
- Most confusing ambiguity pattern: City-qualified Arabic provider queries (برجيل أبوظبي) fail routing even when Burjeel family is known
- Most common operator retry behavior: Rephrasing provider queries when full-name or city-qualified form not recognized
- Most common unsupported expectation: Multi-plan summary ("all Remedy plans") and shorthand (c3) — operators expect abbreviation and batch support
- Most common Arabic phrasing friction: Referral-field queries in Arabic ("فيها إحالة ولا لا؟") blocked despite plan name detected
- Most common provider clarification flow: Specific Burjeel branch name not in LUT → provider not found or routing miss
- Documentation reducing retries: Partial — plan_core Arabic working well; provider routing requires operator guidance
- Operator trust improving: Yes — HIGH trust in 19 of 30 queries (vs 14 of 30 in Day 2 GOOD)

## Historical Summary Update (after Day 3)
| Scope | Total | GOOD | REVIEW | BLOCKED_OK | GAP | CRITICAL |
|---|---:|---:|---:|---:|---:|---:|
| Day 3 | 30 | 13 | 11 | 6 | 0 | 0 |
| Cumulative (Day 1+2+3) | 90 | 38 | 38 | 14 | 0 | 0 |

---

## Day 4 Summary (2026-05-10)
- Operator: owner/operator
- Queries Run: 30
- GOOD: 15
- REVIEW: 12
- BLOCKED_OK: 3
- GAP: 0
- CRITICAL: 0
- Top Friction Points:
  - Provider phrasing variants still not routing (Al Noor, Zulekha, LLH, NMC Specialty, Burjeel Day Surgery)
  - Shorthand c2r not recognized (same pattern as c3 in Day 3)
  - Area-of-coverage phrasing ("cover worldwide?") blocked despite plan identified
  - Free-form broker phrasing ("what does it include", "for broker presentation") not routed
- Any Unsafe Behavior: no
- Notable Positive: Arabic plan_core queries performing strongly (Classic 2 فيه direct billing, ريميدي 03, ملخص classic 2r all GOOD)
- Notable Positive: Arabic comparison (قارن classic 3 و classic 2) successfully returned factual comparison
- Operator Notes:
  - Day 4 confirms stable deterministic safety. Arabic plan_core and comparison routing improving.
  - Provider routing gap is the persistent REVIEW cluster across all 4 days.
  - No code changes performed.

### Detailed Query Log - Day 4

| # | Timestamp | Query | Expected Intent | Actual Intent | Output Summary | Classification | Reason | Trust | Client-facing Safe? | Retry Required? | Ambiguity? | Action Recommendation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 14:03:59 | Is Mediclinic Jumeirah in the network? | network_lookup | network_lookup | Provider not found. | GOOD | Correctly routed to network_lookup; Mediclinic Jumeirah not in LUT | HIGH | yes | no | no | none |
| 2 | 14:04:01 | Burjeel Specialty Hospital Abu Dhabi network? | network_lookup | unsupported | Sorry, this query is not supported or not available. | REVIEW | Burjeel subtype "Specialty Hospital" not routed — routing miss | MEDIUM | no | yes | no | docs clarification |
| 3 | 14:04:02 | هل مستشفى زايد في الشبكة؟ | network_lookup | network_lookup | Provider not found. | GOOD | Arabic query correctly routed; Zayed Hospital not in LUT | HIGH | yes | no | no | none |
| 4 | 14:04:04 | Al Noor Hospital which network? | network_lookup | unsupported | Sorry, this query is not supported or not available. | REVIEW | Common UAE provider not routed to network_lookup — routing miss | MEDIUM | no | yes | no | docs clarification |
| 5 | 14:04:05 | مستشفى الهلال الأحمر في أي شبكة | network_lookup | network_lookup | Provider not found. | GOOD | Arabic provider query correctly routed; Red Crescent not in LUT | HIGH | yes | no | no | none |
| 6 | 14:04:07 | Is Aster Clinic Bur Dubai in hn_standard? | network_lookup | unsupported | Sorry, this query is not supported or not available. | REVIEW | Tier-specific membership query not supported — correctly blocked but unexplained | MEDIUM | no | yes | no | docs clarification |
| 7 | 14:04:08 | LLH Hospital network? | network_lookup | unsupported | Sorry, this query is not supported or not available. | REVIEW | Short acronym LLH not routed to network_lookup | MEDIUM | no | yes | no | operator guidance |
| 8 | 14:04:09 | Zulekha Hospital Dubai network | network_lookup | unsupported | Sorry, this query is not supported or not available. | REVIEW | Known UAE hospital not routed — routing miss | MEDIUM | no | yes | no | docs clarification |
| 9 | 14:04:10 | مستشفى ميديكلينيك دبي في اي شبكة | network_lookup | network_lookup | Provider not found. | GOOD | Arabic Mediclinic query correctly routed; transliteration not matched | HIGH | yes | no | no | none |
| 10 | 14:04:12 | Is Life Medical Centre in the network? | network_lookup | network_lookup | YES: life medical centre | GOOD | Provider found and confirmed in-network deterministically | HIGH | yes | no | no | none |
| 11 | 14:04:13 | NMC Specialty Hospital which network | network_lookup | unsupported | Sorry, this query is not supported or not available. | REVIEW | NMC Specialty variant not routed — routing miss | MEDIUM | no | yes | no | docs clarification |
| 12 | 14:04:14 | Burjeel Day Surgery Centre network please | network_lookup | unsupported | Sorry, this query is not supported or not available. | REVIEW | Burjeel subtype not routed — routing miss pattern consistent with Days 2-3 | MEDIUM | no | yes | no | docs clarification |
| 13 | 14:04:15 | Classic 2 فيه direct billing؟ | plan_core | plan_core | Plan: Classic 2 / Direct billing: Yes | GOOD | Mixed-language field query answered correctly | HIGH | yes | no | no | none |
| 14 | 14:04:16 | ريميدي 03 تغطية الإحالة ايه | plan_core | plan_core | Plan: Remedy 03 / HN Basic Plus / Referral: No | GOOD | Arabic plan_core query routed and answered correctly | HIGH | yes | no | no | none |
| 15 | 14:04:17 | ملخص classic 2r | plan_summary | plan_summary | Plan: Classic 2R / Standard Plus / AED 250,000 / Worldwide | GOOD | Shorthand Arabic plan name + English code recognized correctly | HIGH | yes | no | no | none |
| 16 | 14:04:18 | c2r annual limit | plan_core | unsupported | Sorry, this query is not supported or not available. | REVIEW | Shorthand c2r not recognized — same friction as c3 in Day 3 | MEDIUM | no | yes | no | wording example needed |
| 17 | 14:04:20 | قارن classic 3 و classic 2 | plan_comparison | plan_comparison | Arabic comparison: Classic 2 vs Classic 3 — Annual limit, direct billing, referral | GOOD | Arabic comparison with mixed-case English plan names succeeded | HIGH | yes | no | no | none |
| 18 | 14:04:21 | remedy 02 شبكة ايه | plan_core | plan_core | Plan: Remedy 02 / HN Basic Plus / AED 150,000 | GOOD | Lowercase mixed English-Arabic query answered correctly | HIGH | yes | no | no | none |
| 19 | 14:04:22 | What is the network for Remedy 04? | plan_core | plan_core | Plan: Remedy 04 / HN Basic Plus (OP Restricted) | GOOD | Supported plan core query answered correctly | HIGH | yes | no | no | none |
| 20 | 14:04:23 | Is direct billing included in Classic 2? | plan_core | plan_core | Plan: Classic 2 / Direct billing: Yes | GOOD | Supported plan core query answered correctly | HIGH | yes | no | no | none |
| 21 | 14:04:24 | Annual limit for Remedy 06? | plan_core | plan_core | Plan: Remedy 06 / AED 150,000 / HN Basic Plus | GOOD | Supported plan core query answered correctly | HIGH | yes | no | no | none |
| 22 | 14:04:25 | Does Classic 2R cover worldwide? | plan_core | unsupported | Sorry, this query is not supported or not available. | REVIEW | Area-of-coverage phrasing ("cover worldwide") blocked despite plan identified — REVIEW | MEDIUM | no | yes | no | wording example needed |
| 23 | 14:04:26 | Compare Classic 2 and Classic 2R | plan_comparison | plan_comparison | Sorry, comparison is not supported or not available for one or both plans. | BLOCKED_OK | Same-family near-duplicate comparison not supported — correctly blocked | HIGH | yes | no | no | docs clarification |
| 24 | 14:04:27 | What plan should I recommend to a 30 year old? | unsupported | unsupported | Sorry, this query is not supported or not available. | BLOCKED_OK | Demographic-based recommendation correctly blocked | HIGH | yes | no | no | none |
| 25 | 14:04:28 | Is Classic 3 cheaper than Classic 2R? | unsupported | unsupported | Sorry, this query is not supported or not available. | BLOCKED_OK | Pricing comparison correctly blocked — no pricing logic exposed | HIGH | yes | no | no | none |
| 26 | 14:04:29 | Compare Remedy 03 and Remedy 05 | plan_comparison | plan_comparison | Comparison Remedy 03 vs Remedy 05: Annual limit AED 150K both / Pharmacy limits differ | GOOD | Same-family factual comparison answered correctly | HIGH | yes | no | no | none |
| 27 | 14:04:31 | Summary of Classic 2 for my client | plan_summary | plan_summary | Plan: Classic 2 / Standard Plus / AED 250,000 / Worldwide | GOOD | Client-contextualized plan summary phrasing correctly routed | HIGH | yes | no | no | none |
| 28 | 14:04:32 | Give me Classic 3 for broker presentation | plan_summary | unsupported | Sorry, this query is not supported or not available. | REVIEW | Broker-presentation phrasing not routed — Day 4 phrasing friction | MEDIUM | no | yes | no | wording example needed |
| 29 | 14:04:33 | Remedy 05 plan details | plan_summary | unsupported | Sorry, this query is not supported or not available. | REVIEW | "plan details" phrasing not routed — operator expects plan_summary | MEDIUM | no | yes | no | wording example needed |
| 30 | 14:04:34 | Classic 2R what does it include | plan_summary | unsupported | Sorry, this query is not supported or not available. | REVIEW | "what does it include" natural-language phrasing not routed | MEDIUM | no | yes | no | wording example needed |

## Day 4 Special Analysis
- Most repeated REVIEW cluster: Provider routing miss for common UAE hospitals not using standard Burjeel/Aster/Mediclinic family keyword (LLH, Al Noor, Zulekha, NMC Specialty, Burjeel Day Surgery = 5 of 12 REVIEW)
- Most confusing ambiguity pattern: Burjeel subtypes (Specialty Hospital, Day Surgery Centre) consistently fail routing even though Burjeel family known
- Most common operator retry behavior: Operators try broker/client-contextualized free-form phrasing ("for my client", "what does it include") — all blocked by routing
- Most common unsupported expectation: Demographic/age-based recommendation and pricing comparison remain clearly understood as blocked
- Most common Arabic phrasing friction: Shorthand codes (c2r, c3) not recognized — persistent across Days 3 and 4
- Most common provider clarification flow: Shorthand acronym (LLH) and variant suffixes (Specialty, Day Surgery) fail routing
- Documentation reducing retries: Arabic plan_core and comparison improving measurably; provider routing still requires operator guidance
- Operator trust improving: YES — GOOD rate improved (15/30 = 50% in Day 4 vs 13/30 = 43% in Day 3); Arabic query success rate improved

## Historical Summary Update (after Day 4)
| Scope | Total | GOOD | REVIEW | BLOCKED_OK | GAP | CRITICAL |
|---|---:|---:|---:|---:|---:|---:|
| Day 4 | 30 | 15 | 12 | 3 | 0 | 0 |
| Cumulative (Day 1–4) | 120 | 53 | 50 | 17 | 0 | 0 |
