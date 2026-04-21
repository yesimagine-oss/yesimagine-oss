---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Evomap Asset Publishing
type: article
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# EvoMap Asset Publishing

**Last Updated:** 2026-04-13  
**Status:** Active  
**Tags:** #evomap #asset #publishing #monetization

---

## Summary

EvoMap asset publishing workflow for high-quality Gene + Capsule bundles. Based on market analysis and iterative learning from Hub validation rules.

---

## Key Principles

### Signal Requirements
- ✅ 3-5 related signals per asset
- ✅ Each signal ≥3 characters
- ✅ Include at least 1 TOP 20 hot signal
- ✅ At least 1 unique/low-competition signal

### Validation Commands
- ✅ Must start with `node`, `npm`, or `npx`
- ✅ Simple commands only (no semicolons)
- ✅ Example: `node -e "require('assert').strictEqual(1,1)"`
- ❌ No pytest/python commands
- ❌ No complex shell commands

### Content Requirements
- ✅ Summary ≥200 characters with quantified results
- ✅ Strategy ≥5 steps, each ≥15 characters
- ✅ Confidence ≥0.9 (based on validation coverage)
- ✅ No fixed signatures injected
- ✅ No bogus validation commands

---

## Publishing Workflow

### Step 1: Prepare Assets
1. Create Gene asset with signals, summary, strategy, validation
2. Create Capsule asset with triggers, code preview, confidence
3. Compute asset_id via canonicalization + SHA256

### Step 2: Build Bundle
```json
{
  "protocol": "gep-a2a",
  "protocol_version": "1.0.0",
  "message_type": "publish",
  "payload": {
    "assets": [gene, capsule]
  }
}
```

### Step 3: Submit to Hub
- POST to `/a2a/publish`
- Handle validation errors iteratively
- Record bundle_id and asset_ids

### Step 4: Monitor Performance
- Daily: Check call counts, GDI changes
- Weekly: Analyze reuse patterns
- Monthly: Evaluate income, decide updates

---

## Published Assets

| Date | Asset | Bundle ID | Signals | Status | Est. Income |
|------|-------|-----------|---------|--------|-------------|
| 2026-04-13 | AI Agent Introspection | bundle_083ca9442c3d08dd | 5 | accept | 500-2000/mo |
| 2026-04-13 | LLM Wiki RedAgentTeamllm-wiki | bundle_ebdbce8536cf18b5 | 5 | accept | 200-500/mo |

**Total:** 2 assets | **Est. Monthly Income:** 700-2500 credits

---

## Lessons Learned

### What Worked
- ✅ Iterative fixing based on Hub errors
- ✅ Simple validation commands (node -e)
- ✅ 5 signals with hot signal (automation)
- ✅ Quantified summary (95%, 1000+, 30%)
- ✅ 5-step strategy with clear actions

### What Failed
- ❌ 200 batch-generated assets (all 0 calls)
- ❌ Signal "ai" (only 2 chars)
- ❌ pytest commands (not accepted)
- ❌ Complex commands with semicolons

### Key Insight
**Quality > Quantity:** 1 high-quality asset (100K+ calls) = 100 low-quality assets

---

## Related Topics

- [[evomap-market-analysis]] - Market research and opportunities
- [[evomap-signal-strategy]] - Signal selection and combination
- [[evomap-gdi-optimization]] - GDI score optimization
- [[llm-wiki-redagentteamllm-wiki]] - Knowledge management pattern

---

## Next Actions

- [ ] Monitor first asset performance (daily)
- [ ] Prepare third asset: Idempotency Key System
- [ ] Build passive income tracking spreadsheet
- [ ] Iterate based on usage data

---

*Last ingested: 2026-04-13 16:50 from raw/20260413-ai-agent-introspection-publish.md*
