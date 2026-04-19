# Demo Expected Outcomes

## 1. Network/Provider Queries

### 1. Is Accuracy Plus Medical Laboratory in the network?
- **Why it matters:** Verifies provider access for a member.
- **Expected output:** "In network" or "Provider not found" with provider details.
- **Fallback:** If provider not found, returns clear not found message.

### 2. Which network tiers is Aster Hospital (Qusais) available in?
- **Why it matters:** Shows tiered access for a major hospital.
- **Expected output:** List of network tiers (e.g., "HN Basic Plus, HN Premier").
- **Fallback:** If not found, returns "Provider not found".

### 3. What city is International Modern Hospital located in?
- **Why it matters:** Location is key for member convenience.
- **Expected output:** City name (e.g., "Dubai").
- **Fallback:** If not found, returns "Provider not found".

### 4. What type of provider is Burjeel Specialty Hospital Sharjah?
- **Why it matters:** Confirms provider specialization.
- **Expected output:** Type (e.g., "Hospital").
- **Fallback:** If not found, returns "Provider not found".

### 5. Is Ajman Specialty Hospital covered under HN Basic Plus?
- **Why it matters:** Confirms network coverage for a specific plan.
- **Expected output:** "In network" or "Not in network" for HN Basic Plus.
- **Fallback:** If ambiguous, returns "Ambiguous provider match".

## 2. Plan/Benefit Queries

### 6. What is the annual limit for Remedy 02?
- **Why it matters:** Core financial coverage question.
- **Expected output:** AED value (e.g., "AED. 150,000").
- **Fallback:** If plan not found, prompts for valid plan.

### 7. What is the pharmacy benefit for Remedy 02?
- **Why it matters:** Key for medication access.
- **Expected output:** Pharmacy benefit summary (e.g., "Maximum AED 3,000/year 30% payable by member...").
- **Fallback:** If field not found, returns fallback message.

### 8. Compare Remedy 02 and Remedy 03 for maternity cover.
- **Why it matters:** Shows plan differentiation for a critical benefit.
- **Expected output:** Side-by-side maternity cover details.
- **Fallback:** If field not found, returns fallback message.

### 9. What is the co-pay for outpatient services in Remedy 03?
- **Why it matters:** Out-of-pocket cost is a top member concern.
- **Expected output:** Co-pay percentage or summary.
- **Fallback:** If field not found, returns fallback message.

### 10. Summarize the key exclusions for Remedy 02.
- **Why it matters:** Exclusions are critical for risk and compliance.
- **Expected output:** Bullet or paragraph summary of exclusions.
- **Fallback:** If exclusions not found, returns fallback message.

## 3. Arabic Queries

### 11. هل مختبر Accuracy Plus الطبي داخل الشبكة؟
- **Why it matters:** Arabic-speaking member access.
- **Expected output:** Arabic "داخل الشبكة" or "المزود غير موجود".
- **Fallback:** Arabic not found/ambiguous message.

### 12. ما هي حدود التغطية السنوية لخطة Remedy 02؟
- **Why it matters:** Arabic financial coverage.
- **Expected output:** Arabic summary of annual limit.
- **Fallback:** Arabic fallback if plan/field not found.

### 13. ما هي مزايا الصيدلية في Remedy 03؟
- **Why it matters:** Arabic medication access.
- **Expected output:** Arabic summary of pharmacy benefit.
- **Fallback:** Arabic fallback if field not found.

### 14. هل مستشفى أستر (القصيص) مشمول في الشبكة؟
- **Why it matters:** Arabic provider access.
- **Expected output:** Arabic "داخل الشبكة" or not found.
- **Fallback:** Arabic fallback if provider not found.

### 15. ما هي المستشفيات المتاحة في شبكة HN Basic Plus؟
- **Why it matters:** Arabic network access.
- **Expected output:** List of hospitals in Arabic or fallback.
- **Fallback:** Arabic fallback if network not found.
