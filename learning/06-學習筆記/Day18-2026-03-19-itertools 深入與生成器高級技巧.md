# Day 18 - itertools 深入與生成器高級技巧

**日期**: 2026-03-19  
**學習時長**: 預計 2-3 小時  
**官方文檔**: https://docs.python.org/3/library/itertools.html

---

## 📚 學習內容大綱

### 1. itertools 模塊深入

### 2. 生成器高級技巧

### 3. 協程基礎 (Coroutines)

### 4. 實戰：高性能數據處理

---

## 1️⃣ itertools 模塊深入

### 1.1 高級鏈接技巧

```python
import itertools

# chain.from_iterable - 扁平化二維列表
nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flattened = itertools.chain.from_iterable(nested)
print(list(flattened))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 處理多個文件
def read_multiple_files(filenames):
    file_iterators = (open(f, 'r') for f in filenames)
    for line in itertools.chain.from_iterable(file_iterators):
        yield line.strip()

# 使用
# for line in read_multiple_files(['file1.txt', 'file2.txt', 'file3.txt']):
#     process(line)
```

### 1.2 高級切片

```python
import itertools

# islice - 高效切片大文件
def read_lines(filename, start=0, end=None):
    with open(filename, 'r') as f:
        for line in itertools.islice(f, start, end):
            yield line.strip()

# 讀取第 100-200 行
# for line in read_lines('large_file.txt', 100, 200):
#     print(line)

# 跳過表頭
def skip_header(filename, n=1):
    with open(filename, 'r') as f:
        for line in itertools.islice(f, n, None):
            yield line.strip()

# 分塊讀取
def read_in_chunks(filename, chunk_size=1000):
    with open(filename, 'r') as f:
        while True:
            chunk = list(itertools.islice(f, chunk_size))
            if not chunk:
                break
            yield chunk

# 使用
# for chunk in read_in_chunks('large_file.txt', 1000):
#     process_chunk(chunk)
```

### 1.3 分組高級應用

```python
import itertools

# groupby - 連續相同元素分組
data = [1, 1, 1, 2, 2, 3, 3, 3, 3, 2, 2, 1]
for key, group in itertools.groupby(data):
    print(f"{key}: {list(group)}")
# 1: [1, 1, 1]
# 2: [2, 2]
# 3: [3, 3, 3, 3]
# 2: [2, 2]
# 1: [1]

# 按長度分組單詞
words = ['a', 'bb', 'ccc', 'dd', 'eee', 'ffff']
words_sorted = sorted(words, key=len)  # 必須先排序！
for length, group in itertools.groupby(words_sorted, key=len):
    print(f"長度 {length}: {list(group)}")
# 長度 1: ['a']
# 長度 2: ['bb', 'dd']
# 長度 3: ['ccc', 'eee']
# 長度 4: ['ffff']

# 計算連續出現次數
def run_length_encode(data):
    return [(key, len(list(group))) for key, group in itertools.groupby(data)]

data = 'AAABBBAACCCDDDDAA'
encoded = run_length_encode(data)
print(encoded)  # [('A', 3), ('B', 3), ('A', 2), ('C', 3), ('D', 4), ('A', 2)]
```

### 1.4 排列組合實戰

```python
import itertools

# 生成密碼組合
def generate_passwords(chars, length):
    for combo in itertools.product(chars, repeat=length):
        yield ''.join(combo)

# 生成 3 位數字密碼
# for pwd in generate_passwords('0123456789', 3):
#     print(pwd)

# 比賽排名
teams = ['A', 'B', 'C', 'D']
print("前三名可能:")
for ranking in itertools.permutations(teams, 3):
    print(f"1.{ranking[0]} 2.{ranking[1]} 3.{ranking[2]}")

# 組合抽樣
import random
lottery_numbers = range(1, 50)
combinations = list(itertools.combinations(lottery_numbers, 6))
print(f"總組合數：{len(combinations)}")  # 15,890,700

# 隨機選一組
random_combo = random.choice(combinations)
print(f"幸運號碼：{random_combo}")
```

### 1.5 tee - 創建獨立迭代器

```python
import itertools

# tee - 從一個迭代器創建多個獨立迭代器
data = range(5)
iter1, iter2, iter3 = itertools.tee(data, 3)

print(f"iter1: {list(iter1)}")  # [0, 1, 2, 3, 4]
print(f"iter2: {list(iter2)}")  # [0, 1, 2, 3, 4]
print(f"iter3: {list(iter3)}")  # [0, 1, 2, 3, 4]

# 注意：tee 會緩存數據，如果一個迭代器消耗太多，會占用內存
# 最好立即使用創建的迭代器

# 實用示例：同時計算總和與平均值
def calculate_stats(numbers):
    iter1, iter2 = itertools.tee(numbers)
    total = sum(iter1)
    count = len(list(iter2))
    return total, total / count if count > 0 else 0

stats = calculate_stats([1, 2, 3, 4, 5])
print(f"總和：{stats[0]}, 平均值：{stats[1]}")
```

### 1.6 zip_longest - 處理不等長列表

```python
import itertools

# 普通 zip - 以最長的為準
list1 = [1, 2, 3, 4, 5]
list2 = ['a', 'b', 'c']

print(list(zip(list1, list2)))
# [(1, 'a'), (2, 'b'), (3, 'c')] - 丟失了 4 和 5

# zip_longest - 填充缺失值
print(list(itertools.zip_longest(list1, list2, fillvalue='?')))
# [(1, 'a'), (2, 'b'), (3, 'c'), (4, '?'), (5, '?')]

# 轉置矩陣（不等長行）
matrix = [
    [1, 2, 3, 4],
    [5, 6],
    [7, 8, 9]
]

transposed = list(itertools.zip_longest(*matrix, fillvalue=0))
print(transposed)
# [(1, 5, 7), (2, 6, 8), (3, 0, 9), (4, 0, 0)]
```

---

## 2️⃣ 生成器高級技巧

### 2.1 生成器委托 (yield from)

```python
# 嵌套循環的簡化
def nested_loop():
    for i in range(3):
        for j in range(3):
            yield (i, j)

# 使用 yield from 簡化
def nested_loop_v2():
    for i in range(3):
        yield from ((i, j) for j in range(3))

print(list(nested_loop_v2()))
# [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

# 委托給另一個生成器
def sub_generator():
    yield 1
    yield 2
    yield 3

def main_generator():
    yield 0
    yield from sub_generator()  # 委托
    yield 4

print(list(main_generator()))  # [0, 1, 2, 3, 4]

# 實戰：目錄樹遍歷
import os

def list_files(directory):
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            yield path
        elif os.path.isdir(path):
            yield from list_files(path)  # 遞歸委托

# 使用
# for file in list_files('/path/to/dir'):
#     print(file)
```

### 2.2 生成器管道

```python
# 鏈式生成器函數
def multiply(n):
    def generator(iterable):
        for item in iterable:
            yield item * n
    return generator

def add(n):
    def generator(iterable):
        for item in iterable:
            yield item + n
    return generator

def filter_even(iterable):
    for item in iterable:
        if item % 2 == 0:
            yield item

# 構建管道
data = range(10)
pipeline = data
pipeline = filter_even(pipeline)
pipeline = multiply(2)(pipeline)
pipeline = add(10)(pipeline)

print(list(pipeline))  # [10, 14, 18, 22, 26]

# 更優雅的管道構建
class Pipeline:
    def __init__(self, source):
        self.source = source
    
    def transform(self, func):
        self.source = func(self.source)
        return self
    
    def filter(self, predicate):
        def gen(iterable):
            for item in iterable:
                if predicate(item):
                    yield item
        return self.transform(gen)
    
    def map(self, func):
        def gen(iterable):
            for item in iterable:
                yield func(item)
        return self.transform(gen)
    
    def collect(self):
        return list(self.source)

# 使用
result = (Pipeline(range(10))
    .filter(lambda x: x % 2 == 0)
    .map(lambda x: x * 2)
    .map(lambda x: x + 10)
    .collect())

print(result)  # [10, 14, 18, 22, 26]
```

### 2.3 生成器與異常處理

```python
def safe_generator():
    try:
        for i in range(5):
            yield i
    except GeneratorExit:
        print("生成器被提前關閉")
    except Exception as e:
        print(f"發生錯誤：{e}")
        raise

gen = safe_generator()
print(next(gen))  # 0
print(next(gen))  # 1
gen.close()  # 生成器被提前關閉

# 在生成器中捕獲外部異常
def robust_processor():
    while True:
        try:
            value = yield
            result = 100 / value
            print(f"結果：{result}")
        except ZeroDivisionError:
            print("錯誤：除以零")
        except Exception as e:
            print(f"未知錯誤：{e}")

proc = robust_processor()
next(proc)
proc.send(10)   # 結果：10.0
proc.send(0)    # 錯誤：除以零
proc.send(20)   # 結果：5.0
```

### 2.4 生成器記憶化

```python
def memoize_generator(gen_func):
    """生成器記憶化裝飾器"""
    cache = []
    completed = False
    
    def wrapper(*args, **kwargs):
        nonlocal completed
        gen = gen_func(*args, **kwargs)
        
        index = 0
        while True:
            if index < len(cache):
                yield cache[index]
                index += 1
            elif completed:
                break
            else:
                try:
                    value = next(gen)
                    cache.append(value)
                    yield value
                    index += 1
                except StopIteration:
                    completed = True
                    break
    
    return wrapper

@memoize_generator
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
print([next(fib) for _ in range(5)])  # [0, 1, 1, 2, 3]
print([next(fib) for _ in range(5)])  # [5, 8, 13, 21, 34] - 從緩存讀取
```

---

## 3️⃣ 協程基礎 (Coroutines)

### 3.1 什麼是協程？

```python
# 協程是可以暫停和恢復的函數，支持雙向數據流

def simple_coroutine():
    print("協程啟動")
    x = yield
    print(f"接收到：{x}")
    y = yield
    print(f"接收到：{y}")

coro = simple_coroutine()
next(coro)      # 協程啟動
coro.send(10)   # 接收到：10
coro.send(20)   # 接收到：20
# coro.send(30)  # StopIteration
```

### 3.2 協程狀態機

```python
def status_machine():
    """狀態機協程"""
    state = "IDLE"
    while True:
        cmd = yield state
        if cmd == "START":
            state = "RUNNING"
        elif cmd == "PAUSE":
            state = "PAUSED"
        elif cmd == "RESUME":
            state = "RUNNING"
        elif cmd == "STOP":
            state = "IDLE"
        elif cmd == "STATUS":
            pass  # 返回當前狀態

machine = status_machine()
next(machine)  # 啟動
print(machine.send("STATUS"))  # IDLE
print(machine.send("START"))   # RUNNING
print(machine.send("PAUSE"))   # PAUSED
print(machine.send("RESUME"))  # RUNNING
print(machine.send("STOP"))    # IDLE
```

### 3.3 協程管道

```python
def producer(target):
    """生產者協程"""
    for i in range(5):
        target.send(i)
    target.close()

def filter_positive(target):
    """過濾器協程 - 只傳遞正數"""
    while True:
        value = yield
        if value > 0:
            target.send(value)

def square(target):
    """轉換器協程 - 平方"""
    while True:
        value = yield
        target.send(value ** 2)

def consumer():
    """消費者協程"""
    while True:
        value = yield
        print(f"收到：{value}")

# 構建管道
consumer_coro = consumer()
next(consumer_coro)

square_coro = square(consumer_coro)
next(square_coro)

filter_coro = filter_positive(square_coro)
next(filter_coro)

# 發送數據
data = [-2, -1, 0, 1, 2, 3]
for num in data:
    filter_coro.send(num)

filter_coro.close()
# 輸出:
# 收到：1
# 收到：4
# 收到：9
```

### 3.4 協程裝飾器

```python
from functools import wraps

def coroutine(func):
    """協程裝飾器 - 自動啟動"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return wrapper

@coroutine
def grep(pattern):
    """搜索包含模式的行"""
    while True:
        line = yield
        if pattern in line:
            print(f"匹配：{line}")

@coroutine
def printer():
    """打印接收到的值"""
    while True:
        value = yield
        print(f"打印：{value}")

# 使用
g = grep("Python")
g.send("I love Python")  # 匹配：I love Python
g.send("Java is good")   # 無輸出

p = printer()
p.send("Hello")  # 打印：Hello
p.send("World")  # 打印：World
```

### 3.5 協程聚合數據

```python
@coroutine
def averager():
    """計算平均值的協程"""
    total = 0.0
    count = 0
    average = None
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count

avg = averager()
print(avg.send(10))  # 10.0
print(avg.send(20))  # 15.0
print(avg.send(30))  # 20.0
print(avg.send(40))  # 25.0
```

---

## 4️⃣ 實戰：高性能數據處理

### 4.1 大文件日志分析

```python
import itertools
import re
from collections import defaultdict

def read_log(filename):
    """惰性讀取日志文件"""
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()

def parse_log_line(line):
    """解析日志行"""
    pattern = r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.+)'
    match = re.match(pattern, line)
    if match:
        return {
            'date': match.group(1),
            'time': match.group(2),
            'level': match.group(3),
            'message': match.group(4)
        }
    return None

def filter_by_level(level):
    """按級別過濾"""
    def filter_gen(records):
        for record in records:
            if record and record['level'] == level:
                yield record
    return filter_gen

def group_by_date(records):
    """按日期分組"""
    groups = defaultdict(list)
    for record in records:
        if record:
            groups[record['date']].append(record)
    return groups

def count_by_level(records):
    """統計各級別數量"""
    counts = defaultdict(int)
    for record in records:
        if record:
            counts[record['level']] += 1
    return counts

# 使用管道
def analyze_log(filename):
    lines = read_log(filename)
    parsed = (parse_log_line(line) for line in lines)
    
    # 統計
    parsed_list = list(parsed)
    counts = count_by_level(parsed_list)
    groups = group_by_date(parsed_list)
    
    print("日志統計:")
    for level, count in sorted(counts.items()):
        print(f"  {level}: {count}")
    
    print(f"\n按日期分組:")
    for date, records in sorted(groups.items()):
        print(f"  {date}: {len(records)} 條")

# 模擬日志
log_data = """
2026-03-19 10:00:00 INFO 系統啟動
2026-03-19 10:01:00 ERROR 數據庫連接失敗
2026-03-19 10:02:00 WARNING 內存使用率高
2026-03-19 10:03:00 ERROR 服務超時
2026-03-19 10:04:00 INFO 服務重啟
2026-03-20 09:00:00 INFO 系統啟動
2026-03-20 09:15:00 ERROR 磁盤空間不足
""".strip().split('\n')

with open('/tmp/test.log', 'w') as f:
    f.write('\n'.join(log_data))

analyze_log('/tmp/test.log')
```

### 4.2 批量 API 請求處理

```python
import itertools
import time

def rate_limiter(max_per_second):
    """限速器生成器"""
    interval = 1.0 / max_per_second
    last_call = 0
    while True:
        current = time.time()
        wait_time = max(0, last_call + interval - current)
        if wait_time > 0:
            time.sleep(wait_time)
        last_call = time.time()
        yield

def batch_processor(items, batch_size=10):
    """批量處理器"""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def process_with_retry(items, max_retries=3):
    """帶重試的處理"""
    for item in items:
        retries = 0
        while retries < max_retries:
            try:
                # 模擬處理
                result = f"處理：{item}"
                yield result
                break
            except Exception as e:
                retries += 1
                if retries >= max_retries:
                    yield f"失敗：{item} ({e})"
                else:
                    time.sleep(0.1 * retries)  # 指數退避

# 使用
urls = [f"https://api.example.com/data/{i}" for i in range(100)]

# 分批處理
batches = batch_processor(urls, batch_size=10)
for i, batch in enumerate(batches):
    print(f"批次 {i+1}: 處理 {len(batch)} 個請求")
    results = process_with_retry(batch)
    for result in results:
        print(f"  {result}")
```

### 4.3 實時數據流處理

```python
@coroutine
def data_filter(min_value=0):
    """數據過濾器"""
    while True:
        value = yield
        if value >= min_value:
            yield value

@coroutine
def data_transform(func):
    """數據轉換器"""
    while True:
        value = yield
        result = func(value)
        yield result

@coroutine
def data_aggregator(window_size=5):
    """數據聚合器 - 移動平均"""
    window = []
    while True:
        value = yield
        window.append(value)
        if len(window) > window_size:
            window.pop(0)
        average = sum(window) / len(window)
        yield average

@coroutine
def data_alert(threshold):
    """警報器"""
    while True:
        value = yield
        if value > threshold:
            print(f"⚠️ 警報：{value} 超過閾值 {threshold}")

# 構建處理管道
def create_pipeline():
    alert = data_alert(100)
    aggregator = data_aggregator(5)
    transform = data_transform(lambda x: x * 1.1)
    
    # 連接管道
    def pipeline():
        while True:
            value = yield
            transformed = transform.send(value)
            aggregated = aggregator.send(transformed)
            if aggregated:
                alert.send(aggregated)
    
    pipe = pipeline()
    next(pipe)
    return pipe

# 使用
pipeline = create_pipeline()
import random
for _ in range(20):
    value = random.randint(50, 150)
    print(f"輸入：{value}")
    pipeline.send(value)
```

---

## 📝 今日練習

### 練習 1: 實現 flatten 生成器

```python
def flatten(nested_list):
    """扁平化任意層級嵌套列表"""
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

# 測試
nested = [1, [2, 3], [4, [5, 6]], 7]
print(list(flatten(nested)))  # [1, 2, 3, 4, 5, 6, 7]
```

### 練習 2: 實現 interleave 生成器

```python
def interleave(*iterables):
    """交錯合併多個可迭代對象"""
    iterators = [iter(it) for it in iterables]
    while iterators:
        for i, it in enumerate(list(iterators)):
            try:
                yield next(it)
            except StopIteration:
                iterators.pop(i)

# 測試
print(list(interleave('ABC', '123', 'xyz')))
# ['A', '1', 'x', 'B', '2', 'y', 'C', '3', 'z']
```

### 練習 3: 實現 sliding_window 生成器

```python
from collections import deque
import itertools

def sliding_window(iterable, n=2):
    """滑動窗口"""
    window = deque(maxlen=n)
    it = iter(iterable)
    for _ in range(n):
        window.append(next(it))
    yield tuple(window)
    for item in it:
        window.append(item)
        yield tuple(window)

# 測試
print(list(sliding_window(range(5), 3)))
# [(0, 1, 2), (1, 2, 3), (2, 3, 4)]
```

---

## 🎯 明日計劃 (Day 19)

- [ ] 裝飾器進階 (類裝飾器、參數化裝飾器)
- [ ] 上下文管理器深入
- [ ] functools 模塊
- [ ] 實戰：裝飾器庫

---

**學習筆記創建時間**: 2026-03-19 06:18 GMT+8
