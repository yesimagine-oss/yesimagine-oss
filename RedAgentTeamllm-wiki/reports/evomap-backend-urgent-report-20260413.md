# URGENT: Worker Pool Error Persists Despite Hub API Showing OK

**Priority:** 🔴 **CRITICAL / P0**  
**Date:** 2026-04-13 19:49 GMT+8  
**Node ID:** node_b83d6e6008dce32f  
**Status:** UNRESOLVED - Requires EvoMap Backend Team Intervention

---

## Problem Summary

**Worker Pool Error (PERSISTS):**
```
"This agent has not sent a hello via evolver yet. 
If you have installed evolver >= 1.48.0, please restart 
evolver so it sends a hello to update the environment info."
```

**Hub API Response (Shows OK):**
```json
{
  "status": "acknowledged",
  "your_node_id": "node_b83d6e6008dce32f",
  "survival_status": "alive",
  "node_status": "active",
  "upgrade_available": null
}
```

**DISCREPANCY:** Hub API returns success, but Platform UI still shows Worker Pool error.

---

## Timeline

| Time (GMT+8) | Event | Result |
|--------------|-------|--------|
| 19:00 | Node offline reported | Started investigation |
| 19:03 | Node brought online | ✅ Node: active |
| 19:11 | Worker Pool error appears | "not sent hello via evolver" |
| 19:14 | Hello/Heartbeat sent | ✅ Hub: acknowledged |
| 19:26 | Evolver version sync attempt | ⚠️ Hub shows 1.40.2 (cached) |
| 19:33 | State flip observed | Normal → Broken → Normal |
| 19:38 | Webchat UI crashed | Platform instability |
| 19:42 | Forced cache clear | ✅ Hub API: OK |
| 19:45 | Final refresh attempt | ❌ **Platform UI STILL SHOWS ERROR** |
| 19:49 | **UNRESOLVED** | ❌ Error persists |

---

## Local Environment (Verified)

| Component | Value | Status |
|-----------|-------|--------|
| Global evolver | 1.53.0 | ✅ Latest |
| Local package.json | 1.53.2 | ✅ Updated |
| Node process | Running (PID active) | ✅ |
| systemd service | Active | ✅ |
| Heartbeat sending | Every 60s | ✅ |
| Hello sent | Multiple times | ✅ |

---

## Hub API Responses (All Successful)

### Hello Response
```json
{
  "status": "acknowledged",
  "your_node_id": "node_b83d6e6008dce32f",
  "survival_status": "alive",
  "claimed": true
}
```

### Heartbeat Response
```json
{
  "status": "ok",
  "node_status": "active",
  "survival_status": "alive",
  "upgrade_available": null
}
```

---

## Platform UI Issue

**Persistent Error:**
```
Worker Pool ERROR:
"This agent has not sent a hello via evolver yet..."
```

**User Actions Taken:**
- ❌ Refreshed platform page (multiple times)
- ❌ Cleared browser cache
- ❌ Cleared browser cookies
- ❌ Tried incognito mode
- ❌ Waited 30+ minutes
- ❌ Force refresh (Ctrl+F5)

**Result:** Error STILL EXISTS on Platform UI

---

## Root Cause Analysis

### What We Know:

1. ✅ **Hub Backend is working correctly**
   - API responses show node is active
   - Hello/Heartbeat are being received
   - No version upgrade warnings

2. ✅ **Local evolver is running correctly**
   - Version 1.53.0/1.53.2 installed
   - Process is running
   - Heartbeat sending every 60s

3. ❌ **Platform UI shows stale/error state**
   - Worker Pool error persists
   - Not cleared by cache refresh
   - Not cleared by waiting

### Likely Causes:

1. **Platform UI Backend Cache** (Most Likely)
   - Separate from Hub API cache
   - May have longer TTL
   - Not invalidated by hello/heartbeat

2. **Worker Pool Service Desync**
   - Worker Pool service may not sync with Hub in real-time
   - May require manual intervention

3. **Database State Inconsistency**
   - Node state in DB may be stale
   - Requires DB refresh/update

---

## Request to EvoMap Backend Team

### Immediate Action Required:

**Please manually refresh/reset the following for node_b83d6e6008dce32f:**

1. **Worker Pool Service Cache**
   - Force refresh worker pool state
   - Clear any cached "no hello" flags

2. **Platform UI Backend Cache**
   - Clear platform-level caches
   - Force UI to re-fetch node state

3. **Database Node State**
   - Verify node state in DB matches Hub API
   - Update if stale

### API Calls Already Made (All Successful):

```bash
POST /a2a/hello
- sender_id: node_b83d6e6008dce32f
- payload: { force_state_refresh, clear_cached_state, invalidate_all_caches }
- Result: acknowledged

POST /a2a/heartbeat
- sender_id: node_b83d6e6008dce32f
- payload: { force_full_state_sync, clear_worker_pool_cache, reset_node_state }
- Result: ok
```

### Evidence:

- Hub API responses (attached)
- Local evolver logs (attached)
- systemd service status (active)
- Version information (1.53.0/1.53.2)

---

## Impact

**Blocked Operations:**
- ❌ Cannot publish assets (Worker Pool error)
- ❌ Cannot claim tasks (Worker Pool error)
- ❌ Cannot participate in swarm collaboration

**Business Impact:**
- Monetization blocked
- Task completion blocked
- Reputation at risk

---

## Contact Information

**Node Owner:** cmm8m3ir8022cqz348vugai04  
**Node ID:** node_b83d6e6008dce32f  
**Claim Code:** 4QW4-SRSC  
**Credit Balance:** ~941.82  
**Reputation:** 68.17

---

## Attachments

1. Hub API Response Logs
2. Local Evolver Logs
3. systemd Service Status
4. Version Information

---

**This is a CRITICAL issue requiring immediate backend intervention.**

**Report Generated:** 2026-04-13 19:49 GMT+8  
**Reported By:** Red Agent Team (node_b83d6e6008dce32f)

---

**Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...**
