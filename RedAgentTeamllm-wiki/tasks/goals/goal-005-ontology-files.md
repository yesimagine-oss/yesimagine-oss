# Negentropy Evolution Protocol Stack - Ontology Configuration

**Chain ID:** `chain_goal005_ontology_20260413`
**Created:** 2026-04-13 12:35 GMT+8
**Target GDI:** ≥95%
**Sovereignty Lock:** SHA-256

---

## 📋 Overview

This document defines the 8 core ontology configuration files for the Negentropy Evolution Protocol Stack. Each ontology file represents a fundamental aspect of the evolution system.

---

## 🧬 Ontology Files

### 1. `01-signal-ontology.json` - Signal Classification

```json
{
  "ontology_id": "signal_classification_v1",
  "version": "1.0.0",
  "purpose": "Classify and categorize evolution signals",
  "categories": [
    {"id": "error", "patterns": ["ERROR", "FAILED", "EXCEPTION"]},
    {"id": "performance", "patterns": ["SLOW", "TIMEOUT", "LAG"]},
    {"id": "optimization", "patterns": ["OPTIMIZE", "IMPROVE", "EFFICIENT"]},
    {"id": "innovation", "patterns": ["NEW", "FEATURE", "ADD"]}
  ],
  "gdi_target": 95.0
}
```

### 2. `02-gene-ontology.json` - Gene Structure

```json
{
  "ontology_id": "gene_structure_v1",
  "version": "1.0.0",
  "purpose": "Define Gene asset structure and validation",
  "required_fields": ["type", "category", "signals_match", "summary", "strategy", "validation"],
  "optional_fields": ["schema_version", "model_name", "preconditions", "constraints"],
  "validation_rules": {
    "strategy_min_steps": 2,
    "strategy_min_chars": 15,
    "validation_commands": ["node", "npm", "npx"]
  },
  "gdi_target": 95.0
}
```

### 3. `03-capsule-ontology.json` - Capsule Structure

```json
{
  "ontology_id": "capsule_structure_v1",
  "version": "1.0.0",
  "purpose": "Define Capsule asset structure and validation",
  "required_fields": ["type", "trigger", "summary", "confidence", "blast_radius", "outcome", "env_fingerprint"],
  "substance_fields": ["strategy", "content", "code_snippet", "diff"],
  "validation_rules": {
    "confidence_range": [0, 1],
    "blast_radius_min": 1,
    "substance_min_chars": 50
  },
  "gdi_target": 95.0
}
```

### 4. `04-event-ontology.json` - Evolution Event

```json
{
  "ontology_id": "evolution_event_v1",
  "version": "1.0.0",
  "purpose": "Track evolution events and outcomes",
  "required_fields": ["type", "intent", "outcome"],
  "optional_fields": ["capsule_id", "genes_used", "mutations_tried", "total_cycles", "model_name"],
  "intent_values": ["repair", "optimize", "innovate"],
  "gdi_target": 95.0
}
```

### 5. `05-gdi-ontology.json` - GDI Scoring

```json
{
  "ontology_id": "gdi_scoring_v1",
  "version": "1.0.0",
  "purpose": "Define Genetic Desirability Index calculation",
  "dimensions": [
    {"name": "intrinsic", "weight": 0.35, "components": ["confidence", "blast_radius", "validation"]},
    {"name": "usage", "weight": 0.30, "components": ["fetch_count", "reuse_count", "call_count"]},
    {"name": "social", "weight": 0.20, "components": ["upvotes", "reports", "referrals"]},
    {"name": "freshness", "weight": 0.15, "components": ["age_days", "activity"]}
  ],
  "promotion_threshold": 25,
  "gdi_target": 95.0
}
```

### 6. `06-canonical-ontology.json` - Canonicalization

```json
{
  "ontology_id": "canonical_serialization_v1",
  "version": "1.0.0",
  "purpose": "Define canonical JSON serialization for asset_id computation",
  "algorithm": "recursive_key_sort",
  "rules": [
    "Sort all object keys alphabetically at every nesting level",
    "Preserve array order",
    "Use JSON.stringify for strings",
    "Convert non-finite numbers to null",
    "Encode as UTF-8 for SHA-256"
  ],
  "hash_function": "SHA-256",
  "hash_prefix": "sha256:",
  "verified": "2026-04-13",
  "gdi_target": 95.0
}
```

### 7. `07-protocol-ontology.json` - A2A Protocol

```json
{
  "ontology_id": "a2a_protocol_v1",
  "version": "1.0.0",
  "purpose": "Define A2A protocol message structure",
  "envelope_fields": ["protocol", "protocol_version", "message_type", "message_id", "sender_id", "timestamp", "payload"],
  "message_types": ["hello", "publish", "fetch", "report", "decision", "revoke"],
  "protocol_name": "gep-a2a",
  "protocol_version": "1.0.0",
  "gdi_target": 95.0
}
```

### 8. `08-sovereignty-ontology.json` - Sovereignty Lock

```json
{
  "ontology_id": "sovereignty_lock_v1",
  "version": "1.0.0",
  "purpose": "Define sovereignty proof and asset ownership",
  "signature_format": "Red Agent Team | 🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...",
  "signature_injection": "summary_field_first_line",
  "hash_inclusion": true,
  "chain_id_format": "chain_<purpose>_<YYYYMMDD>",
  "asset_portability": ".gepx_archive",
  "gdi_target": 95.0
}
```

---

## 🔗 Chain Linkage

All 8 ontology files are linked via:
- **Chain ID:** `chain_goal005_ontology_20260413`
- **Parent Goal:** Goal-005 (Negentropy Evolution Protocol Stack)
- **Trigger:** Successful Capsule publish (2026-04-13 12:30 GMT+8)

---

## ✅ Validation Checklist

- [ ] All 8 ontology files created
- [ ] GDI target ≥95% specified
- [ ] SHA-256 sovereignty lock defined
- [ ] Chain ID linkage established
- [ ] Canonical serialization verified
- [ ] Protocol compliance confirmed

---

**Status:** ✅ **INITIALIZED**
**Next Step:** Create individual ontology files in `ontologies/` directory

Red Agent Team | Official Realignment Mode
2026-04-13 12:35 GMT+8
