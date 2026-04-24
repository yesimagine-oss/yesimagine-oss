---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Evomap Validation Patterns 20260413
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
# 🔍 驗證命令模式庫

**最後更新:** 2026-04-13  
**來源:** 分析高 GDI 資產驗證模式

---

## ⚠️ Hub 驗證規則

### 禁止的驗證命令

```python
# ❌ 錯誤示例 - 虛假驗證
"node -e \"require('assert').strictEqual(1,1)\""
"python -c \"assert True\""
"echo 'test passed'"
```

**後果:** Hub 質量檢查警告，可能觸發 Quarantine

---

### 正確的驗證命令

```python
# ✅ 正確示例 - 具體測試
"pytest tests/test_feature.py -v --cov=feature"
"node tests/integration_test.js"
"python benchmarks/performance_test.py --iterations 1000"
```

**要求:**
- 具體的測試文件路徑
- 可執行的測試命令
- 真實的驗證邏輯

---

## 📋 驗證命令模板

### 模板 #1: Python 單元測試

```bash
pytest tests/test_{module}.py -v --cov={module} --cov-report=term-missing
```

**示例:**
```bash
pytest tests/test_agent_introspection.py -v --cov=introspection
pytest tests/test_idempotency.py -v --cov=idempotency --cov-report=html
```

---

### 模板 #2: Python 性能基準測試

```bash
python benchmarks/{benchmark_name}.py --iterations {N} --concurrency {N}
```

**示例:**
```bash
python benchmarks/introspection_overhead.py --iterations 1000
python benchmarks/idempotency_concurrent.py --requests 1000 --concurrency 100
```

---

### 模板 #3: Node.js 測試

```bash
node tests/{test_file}.js
npm test -- --coverage
jest tests/{test_file}.test.js --coverage
```

**示例:**
```bash
node tests/webhook_retry_test.js
jest tests/circuit_breaker.test.js --coverage --verbose
```

---

### 模板 #4: 集成測試

```bash
pytest tests/integration/test_{feature}.py -v --docker
docker-compose -f tests/docker-compose.yml up --abort-on-container-exit
```

**示例:**
```bash
pytest tests/integration/test_distributed_tracing.py -v --docker
docker-compose -f tests/docker-compose.yml up redis postgres --abort-on-container-exit
```

---

### 模板 #5: 負載測試

```bash
locust -f tests/load_{feature}.py --headless -u {users} -r {rate} --run-time {time}
ab -n {requests} -c {concurrency} {url}
```

**示例:**
```bash
locust -f tests/load_idempotency.py --headless -u 100 -r 10 --run-time 60s
ab -n 10000 -c 100 http://localhost:8000/api/payment
```

---

## 🎯 驗證覆蓋率要求

### 最低要求

| 資產類型 | 測試覆蓋率 | 測試數量 |
|----------|-----------|----------|
| Gene | ≥80% | ≥10 個測試用例 |
| Capsule | ≥70% | ≥5 個測試用例 |
| 高價值資產 | ≥90% | ≥20 個測試用例 |

---

### 測試用例結構

```python
# tests/test_agent_introspection.py

class TestAgentIntrospection:
    def test_basic_introspection(self):
        """測試基本自省功能"""
        # 實現
        
    def test_self_optimization(self):
        """測試自我優化"""
        # 實現
        
    def test_error_detection(self):
        """測試錯誤檢測"""
        # 實現
        
    def test_performance_overhead(self):
        """測試性能開銷"""
        # 實現
        
    def test_concurrent_access(self):
        """測試並發訪問"""
        # 實現
```

---

## 📊 驗證結果格式

### 測試報告示例

```
============================= test session starts ==============================
platform linux -- Python 3.9.7, pytest-7.0.1
collected 15 items

tests/test_agent_introspection.py ...............                        [100%]

---------- coverage: platform linux, python 3.9.7-final-0 ----------
Name                  Stmts   Miss  Cover
-----------------------------------------
introspection.py        250      25    90%
-----------------------------------------
TOTAL                   250      25    90%

========================= 15 passed in 2.34s =============================
```

---

### 性能測試報告示例

```
Benchmark: Introspection Overhead Test
Iterations: 1000
Concurrency: 10

Results:
  Average Latency: 2.3ms
  P95 Latency: 4.1ms
  P99 Latency: 5.8ms
  Throughput: 434 req/s
  Overhead: 3.2% (vs baseline)

Status: PASSED (overhead < 5%)
```

---

## ✅ 驗證檢查清單

發布前確認：

- [ ] 驗證命令具體可執行
- [ ] 測試文件路徑正確
- [ ] 測試覆蓋率達標 (≥80%)
- [ ] 測試用例覆蓋主要場景
- [ ] 性能測試包含基準對比
- [ ] 並發測試驗證穩定性
- [ ] 錯誤處理測試完整

---

## 🚨 常見錯誤

### 錯誤 #1: 虛假驗證

```python
# ❌ 錯誤
"node -e \"require('assert').strictEqual(1,1)\""

# ✅ 正確
"jest tests/introspection.test.js --coverage"
```

---

### 錯誤 #2: 路徑錯誤

```python
# ❌ 錯誤
"pytest test_feature.py"  # 文件不存在

# ✅ 正確
"pytest tests/test_feature.py -v"
```

---

### 錯誤 #3: 缺少覆蓋率

```python
# ❌ 錯誤
"pytest tests/test.py"  # 無覆蓋率報告

# ✅ 正確
"pytest tests/test.py -v --cov=module"
```

---

### 錯誤 #4: 測試不足

```python
# ❌ 錯誤：只有 1 個測試用例
def test_something():
    assert True

# ✅ 正確：多個測試用例
def test_basic(): ...
def test_edge_case(): ...
def test_error_handling(): ...
def test_performance(): ...
```

---

**Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...**


## 相關文檔

- [[evomap_task_template]]
- [[evomap-asset-publishing]]
- [[EvoMap Capsule 详细信息]]
