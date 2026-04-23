# Python itertools 食譜

**創建時間**: 2026-03-19  
**階段**: 第二階段 - Day 18  
**參考文檔**: https://docs.python.org/3/library/itertools.html

---

## 📋 常用食譜速查

### 1. 鏈接與扁平化

```python
import itertools

# 鏈接多個列表
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = list(itertools.chain(list1, list2))
# [1, 2, 3, 4, 5, 6]

# 扁平化二維列表
nested = [[1, 2], [3, 4], [5, 6]]
flattened = list(itertools.chain.from_iterable(nested))
# [1, 2, 3, 4, 5, 6]

# 讀取多個文件
def read_files(*filenames):
    with open(filenames[0]) as f0, open(filenames[1]) as f1:
        for line in itertools.chain(f0, f1):
            process(line)
```

### 2. 切片與分塊

```python
# 跳過前 N 個元素
def skip_n(iterable, n):
    return itertools.islice(iterable, n, None)

# 取前 N 個元素
def take_n(iterable, n):
    return itertools.islice(iterable, n)

# 分塊處理
def chunked(iterable, size):
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk

# 使用
for batch in chunked(range(100), 10):
    process_batch(batch)
```

### 3. 過濾與選擇

```python
# 根據選擇器過濾
data = ['A', 'B', 'C', 'D']
selectors = [True, False, True, False]
filtered = list(itertools.compress(data, selectors))
# ['A', 'C']

# 丟棄直到條件為假
data = [1, 3, 5, 7, 8, 9, 10]
dropped = list(itertools.dropwhile(lambda x: x < 5, data))
# [5, 7, 8, 9, 10]

# 取直到條件為假
taken = list(itertools.takewhile(lambda x: x < 5, data))
# [1, 3]
```

### 4. 分組操作

```python
# 按條件分組 (需要先排序!)
data = [('A', 1), ('A', 2), ('B', 3), ('B', 4)]
data.sort(key=lambda x: x[0])
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")

# 計算連續出現次數
def run_length_encode(data):
    return [(key, len(list(group))) for key, group in itertools.groupby(data)]

encoded = run_length_encode('AAABBBAACCC')
# [('A', 3), ('B', 3), ('A', 2), ('C', 3)]
```

### 5. 排列組合

```python
# 笛卡爾積
for item in itertools.product('AB', '12'):
    print(item)
# ('A', '1'), ('A', '2'), ('B', '1'), ('B', '2')

# 排列 (考慮順序)
for item in itertools.permutations('ABC', 2):
    print(item)
# ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')

# 組合 (不考慮順序)
for item in itertools.combinations('ABC', 2):
    print(item)
# ('A', 'B'), ('A', 'C'), ('B', 'C')

# 可重複組合
for item in itertools.combinations_with_replacement('ABC', 2):
    print(item)
# ('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')
```

### 6. 配對與窗口

```python
# 相鄰配對
def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

for current, next_item in pairwise(range(5)):
    print(f"{current} -> {next_item}")
# 0 -> 1, 1 -> 2, 2 -> 3, 3 -> 4

# 滑動窗口
def sliding_window(iterable, n):
    iters = itertools.tee(iterable, n)
    for i, it in enumerate(iters):
        for _ in range(i):
            next(it, None)
    return zip(*iters)

for window in sliding_window(range(5), 3):
    print(window)
# (0, 1, 2), (1, 2, 3), (2, 3, 4)
```

### 7. 無限序列

```python
# 無限計數
for i in itertools.count(10, 5):
    if i > 30:
        break
    print(i)
# 10, 15, 20, 25, 30

# 循環迭代
for i, item in enumerate(itertools.cycle('AB')):
    if i >= 5:
        break
    print(item)
# A, B, A, B, A

# 重複
list(itertools.repeat('Hello', 3))
# ['Hello', 'Hello', 'Hello']
```

### 8. 聚合統計

```python
# 同時遍历兩個迭代器
for a, b in itertools.zip_longest([1, 2, 3], ['a', 'b'], fillvalue='?'):
    print(f"{a} -> {b}")
# 1 -> a, 2 -> b, 3 -> ?

# 累加
list(itertools.accumulate([1, 2, 3, 4]))
# [1, 3, 6, 10]

# 累加 (使用自定義函數)
import operator
list(itertools.accumulate([1, 2, 3, 4], operator.mul))
# [1, 2, 6, 24]
```

---

## 🎯 實戰模式

### 模式 1: 日誌分析

```python
def analyze_log(filename):
    with open(filename, 'r') as f:
        # 跳過表頭
        lines = itertools.islice(f, 1, None)
        
        # 過濾錯誤
        errors = (line for line in lines if 'ERROR' in line)
        
        # 分組統計
        from collections import defaultdict
        counts = defaultdict(int)
        for error in errors:
            # 提取錯誤類型
            error_type = extract_error_type(error)
            counts[error_type] += 1
        
        return counts
```

### 模式 2: 批量處理

```python
def batch_process(items, batch_size=100):
    # 分塊
    batches = chunked(items, batch_size)
    
    for i, batch in enumerate(batches):
        # 處理每批
        results = process_batch(batch)
        
        # 限速
        if i % 10 == 0:
            time.sleep(1)
        
        yield results
```

### 模式 3: 數據管道

```python
def create_pipeline():
    data = read_source()
    
    # 過濾
    filtered = (x for x in data if is_valid(x))
    
    # 轉換
    transformed = (transform(x) for x in filtered)
    
    # 去重
    seen = set()
    deduped = (x for x in transformed if not (x in seen or seen.add(x)))
    
    # 排序
    sorted_data = sorted(deduped, key=lambda x: x.priority)
    
    # 輸出
    for item in sorted_data:
        yield format_output(item)
```

### 模式 4: 配對比較

```python
def compare_consecutive(data):
    """比較相鄰元素"""
    for current, next_item in pairwise(data):
        if current != next_item:
            yield (current, next_item, 'changed')
        else:
            yield (current, next_item, 'same')

# 檢測變化點
changes = list(compare_consecutive([1, 1, 2, 2, 2, 3]))
```

---

## ⚡ 性能提示

### 1. 惰性計算

```python
# ❌ 立即計算所有結果
results = [process(x) for x in large_data]
first_result = results[0]

# ✅ 惰性計算
results = (process(x) for x in large_data)
first_result = next(results)  # 只計算第一個
```

### 2. 避免中間列表

```python
# ❌ 創建中間列表
data = range(1000000)
squared = [x ** 2 for x in data]
even = [x for x in squared if x % 2 == 0]
result = sum(even)

# ✅ 鏈式生成器
data = range(1000000)
result = sum(x ** 2 for x in data if x ** 2 % 2 == 0)
```

### 3. 使用內置函數

```python
# ❌ 手寫循環
result = []
for i in range(len(a)):
    result.append((a[i], b[i]))

# ✅ 使用 itertools
result = list(zip(a, b))
```

---

## 🐛 常見錯誤

### 錯誤 1: groupby 未排序

```python
# ❌ 錯誤
data = [('A', 1), ('B', 2), ('A', 3)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))
# A: [('A', 1)], B: [('B', 2)], A: [('A', 3)]

# ✅ 正確
data.sort(key=lambda x: x[0])
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))
# A: [('A', 1), ('A', 3)], B: [('B', 2)]
```

### 錯誤 2: 生成器耗盡

```python
# ❌ 錯誤
gen = (x for x in range(5))
list1 = list(gen)  # [0, 1, 2, 3, 4]
list2 = list(gen)  # [] - 已耗盡!

# ✅ 正確
gen = (x for x in range(5))
list1 = list(gen)
gen = (x for x in range(5))  # 重新創建
list2 = list(gen)
```

### 錯誤 3: tee 內存問題

```python
# ❌ 錯誤 - tee 會緩存所有數據
iters = itertools.tee(large_data, 10)
# 如果一個迭代器消耗很快，會占用大量內存

# ✅ 正確 - 盡快使用
iters = itertools.tee(data, 2)
for item in iters[0]:
    process(item)
for item in iters[1]:
    process(item)
```

---

## 📖 參考資源

- **官方文檔**: https://docs.python.org/3/library/itertools.html
- **itertools 食譜**: https://docs.python.org/3/library/itertools.html#itertools-recipes
- **更多食譜**: https://more-itertools.readthedocs.io/

---

**最後更新**: 2026-03-19
