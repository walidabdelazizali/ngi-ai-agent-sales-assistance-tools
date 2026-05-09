# Provider Dataset Coverage Delta (Sprint)

## Run Context
- Mode: PROVIDER DATASET COVERAGE SPRINT
- Execution path: `python -m src.agent_entrypoint --json <query>`
- Scope: provider alias, transliteration, branch ambiguity safety, Arabic routing

## What Changed
- Added provider alias coverage for `Aster Qsais/Al Qusais`, `Burjeel AUH/Abu Dhabi`, `Mediclinic Qusais`.
- Added Arabic transliteration normalization for provider families (`برجيل`, `أستر/استر`, `ان ام سي`, `ميديكلينيك`) and `رويال -> royal`.
- Added deterministic ambiguity-safe responses with candidate preview lists.
- Added wrapper routing patterns for normalized Arabic `في أي network` phrasing.
- Fixed Windows JSON output crash for Unicode checkmarks in `--json` mode.

## Provider-Focused Evidence (Post-Change)
1. `Burjeel Hospital في أي شبكة؟`
- intent: `network_lookup`
- outcome: `GOOD`
- message: `Networks for Burjeel Hospital: hn_exclusive, hn_premier`

2. `Burjeel Hospital في اي شبكة؟`
- intent: `network_lookup`
- outcome: `GOOD`
- message: `Networks for Burjeel Hospital: hn_exclusive, hn_premier`

3. `Which network tiers for Burjeel Hospital?`
- intent: `network_lookup`
- outcome: `GOOD`
- message: network tier list returned successfully (no runtime crash)

4. `Which network tiers is Burjeel Hospital available in?`
- intent: `network_lookup`
- outcome: `GOOD`
- message: network tier list returned successfully (no runtime crash)

5. `Is Burjeel in the network?`
- intent: `network_lookup`
- outcome: `BLOCKED_OK`
- message: `Ambiguous provider match. More than one provider matched: ...`

6. `Is Burjeel AUH in the network?`
- intent: `network_lookup`
- outcome: `GOOD`
- message: `YES: burjeel abu dhabi`

7. `Is Aster Qsais in the network?`
- intent: `network_lookup`
- outcome: `GOOD`
- message: `YES: aster qusais`

8. `Is Mediclinic Airport Road in the network?`
- intent: `network_lookup`
- outcome: `GOOD`
- message: `YES: mediclinic airport road`

9. `Is NMC Royal in the network?`
- intent: `network_lookup`
- outcome: `BLOCKED_OK`
- message: `Ambiguous provider match. More than one provider matched: ...`

10. `Which network tiers for NMC Royal?`
- intent: `network_lookup`
- outcome: `BLOCKED_OK`
- message: `Ambiguous provider match. More than one provider matched: ...`

11. `هل ان ام سي رويال في الشبكة؟`
- intent: `network_lookup`
- outcome: `BLOCKED_OK`
- message: Arabic ambiguity-safe response with candidate preview

12. `هل ميديكلينيك القصيص في الشبكة؟`
- intent: `network_lookup`
- outcome: `GOOD`
- message: `YES: mediclinic qusais`

13. `في أي شبكة ميديكلينيك القصيص؟`
- intent: `network_lookup`
- outcome: `GOOD`
- message: `Networks for Mediclinic Qusais: hn_exclusive, hn_premier`

## Impact Summary
- Provider alias/coverage REVIEW items for Burjeel/Aster were converted to deterministic `network_lookup` responses.
- Ambiguous family-name queries now return explicit candidate lists instead of silent misclassification.
- No change to forbidden scope behavior (recommendation/comparison boundaries unchanged).
- Validation status after sprint: `675 passed, 2 skipped`.
