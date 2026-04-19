# System Overview

## User Input
- User enters a question or query (English or Arabic) via CLI
- Example: "What is the annual limit for Remedy 02?" or "هل مستشفى أستر (القصيص) مشمول في الشبكة؟"

## Query Routing
- System detects intent: plan/benefit vs. network/provider
- Routes query to the correct logic module

## Plan Lookup
- For plan/benefit queries, system loads structured plan data (from JSON)
- Retrieves requested field, summary, or comparison

## Network Lookup
- For provider/network queries, system loads normalized provider data (from CSV)
- Finds provider, network tier, city, and type

## Rules/Benefits Lookup
- System can extract and summarize exclusions, co-pays, limits, and other key rules

## Structured Data Source
- All answers are based on curated, versioned data files (no live scraping or AI generation)
- Ensures reliability and auditability for business use
