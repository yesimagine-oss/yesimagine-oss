# Day 19 - 裝飾器進階與 functools 模塊

**日期**: 2026-03-19  
**學習時長**: 預計 2-3 小時  
**官方文檔**: https://docs.python.org/3/library/functools.html

---

## 📚 學習內容大綱

### 1. 裝飾器進階 (類裝飾器、參數化裝飾器)

### 2. functools 模塊深入

### 3. 上下文管理器深入

### 4. 實戰：裝飾器庫

---

## 1️⃣ 裝飾器進階

### 1.1 回顧：函數裝飾器基礎

```python
from functools import wraps

def simple_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"調用 {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@simple_decorator
def greet(name):
    """問候函數"""
    print(f"你好，{name}！")

greet("小明")
# 調用 greet
# 你好，小明！
```

### 1.2 參數化裝飾器

```python
from functools import wraps

def repeat(times):
    """參數化裝飾器 - 重複執行"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("Hello!")

say_hello()
# Hello!
# Hello!
# Hello!

# 裝飾器工廠
def logging_decorator(prefix=""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{prefix} 調用 {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@logging_decorator("[DEBUG]")
def process_data(data):
    print(f"處理：{data}")

process_data("test")
# [DEBUG] 調用 process_data
# 處理：test
```

### 1.3 類裝飾器

```python
class CountCalls:
    """類裝飾器 - 統計調用次數"""
    def __init__(self, func):
        wraps(func)(self)
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"第 {self.count} 次調用 {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    print(f"你好，{name}！")

greet("小明")  # 第 1 次調用 greet \n 你好，小明！
greet("小紅")  # 第 2 次調用 greet \n 你好，小紅！
print(f"總調用：{greet.count} 次")  # 總調用：2 次

# 類裝飾器帶參數
class Retry:
    """重試裝飾器"""
    def __init__(self, max_retries=3, delay=1):
        self.max_retries = max_retries
        self.delay = delay
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            for attempt in range(self.max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise
                    print(f"重試 {attempt + 1}/{self.max_retries}: {e}")
                    time.sleep(self.delay)
        return wrapper

@Retry(max_retries=3, delay=0.5)
def unstable_api():
    import random
    if random.random() < 0.7:
        raise ConnectionError("連接失敗")
    return "成功"

# 使用
try:
    result = unstable_api()
    print(result)
except Exception as e:
    print(f"最終失敗：{e}")
```

### 1.4 多重裝飾器

```python
from functools import wraps

def decorator1(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("裝飾器 1: 之前")
        result = func(*args, **kwargs)
        print("裝飾器 1: 之後")
        return result
    return wrapper

def decorator2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("裝飾器 2: 之前")
        result = func(*args, **kwargs)
        print("裝飾器 2: 之後")
        return result
    return wrapper

@decorator1
@decorator2
def say_hello():
    print("Hello!")

say_hello()
# 裝飾器 1: 之前
# 裝飾器 2: 之前
# Hello!
# 裝飾器 2: 之後
# 裝飾器 1: 之後
# 注意：裝飾順序從下到上
```

### 1.5 裝飾器類方法

```python
from functools import wraps

def method_logger(func):
    """裝飾類方法"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"調用 {self.__class__.__name__}.{func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper

class MyClass:
    @method_logger
    def greet(self, name):
        print(f"你好，{name}！")
    
    @method_logger
    def farewell(self, name):
        print(f"再見，{name}！")

obj = MyClass()
obj.greet("小明")
# 調用 MyClass.greet
# 你好，小明！

obj.farewell("小明")
# 調用 MyClass.farewell
# 再見，小明！
```

### 1.6 裝飾器統計性能

```python
from functools import wraps
import time

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 耗時：{end - start:.4f}秒")
        return result
    return wrapper

def memory_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import tracemalloc
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"{func.__name__} 內存：峰值 {peak / 1024:.2f} KB")
        return result
    return wrapper

@timing_decorator
@memory_decorator
def process_large_data():
    data = [i ** 2 for i in range(100000)]
    return sum(data)

result = process_large_data()
# process_large_data 內存：峰值 XXX KB
# process_large_data 耗時：X.XXXX 秒
```

---

## 2️⃣ functools 模塊深入

### 2.1 wraps 裝飾器

```python
from functools import wraps

# 不使用 wraps
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """問候函數"""
    print(f"你好，{name}！")

print(greet.__name__)  # wrapper - 錯誤！
print(greet.__doc__)   # None - 錯誤！

# 使用 wraps
def my_decorator_v2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator_v2
def greet_v2(name):
    """問候函數"""
    print(f"你好，{name}！")

print(greet_v2.__name__)  # greet_v2 - 正確！
print(greet_v2.__doc__)   # 問候函數 - 正確！
```

### 2.2 lru_cache - 最近最少使用緩存

```python
from functools import lru_cache

# 基礎用法
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 計算前 20 個斐波那契數
for i in range(20):
    print(fibonacci(i), end=" ")
# 0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181

# 查看緩存信息
print(f"\n緩存信息：{fibonacci.cache_info()}")
# CacheInfo(hits=18, misses=20, maxsize=128, currsize=20)

# 清除緩存
fibonacci.cache_clear()

# 實用示例：昂貴的函數調用
@lru_cache(maxsize=1000)
def expensive_computation(x, y):
    import time
    time.sleep(0.1)  # 模擬耗時
    return x ** y

# 第一次調用 (慢)
result1 = expensive_computation(2, 10)
# 第二次調用 (快，從緩存)
result2 = expensive_computation(2, 10)
```

### 2.3 partial - 偏函數

```python
from functools import partial

# 基礎用法
def power(base, exponent):
    return base ** exponent

# 創建平方函數
square = partial(power, exponent=2)
print(square(5))  # 25

# 創建立方函數
cube = partial(power, exponent=3)
print(cube(3))  # 27

# 實用示例：格式化輸出
def format_text(text, prefix="", suffix="", uppercase=False):
    if uppercase:
        text = text.upper()
    return f"{prefix}{text}{suffix}"

# 創建特定格式化函數
greet = partial(format_text, prefix="你好，", suffix="！", uppercase=True)
print(greet("小明"))  # 你好，小明！

farewell = partial(format_text, prefix="再見，", suffix="~")
print(farewell("小明"))  # 再見，小明~

# 實用示例：HTTP 請求
import requests

def http_request(method, url, **kwargs):
    response = requests.request(method, url, **kwargs)
    return response.json()

# 創建 GET 和 POST 函數
get = partial(http_request, "GET")
post = partial(http_request, "POST")

# 使用
# data = get("https://api.example.com/users")
# new_user = post("https://api.example.com/users", json={"name": "小明"})
```

### 2.4 partialmethod - 偏方法

```python
from functools import partialmethod

class MyClass:
    def greet(self, greeting, name):
        print(f"{greeting}, {name}!")
    
    # 創建特定問候方法
    say_hello = partialmethod(greet, "你好")
    say_goodbye = partialmethod(greet, "再見")

obj = MyClass()
obj.say_hello("小明")    # 你好，小明!
obj.say_goodbye("小明")  # 再見，小明!
```

### 2.5 singledispatch - 單分派泛函

```python
from functools import singledispatch

@singledispatch
def process_data(data):
    """默認處理"""
    print(f"處理未知類型：{type(data)}")
    return data

@process_data.register(str)
def _(data):
    print(f"處理字符串：{data.upper()}")
    return data.upper()

@process_data.register(int)
def _(data):
    print(f"處理數字：{data * 2}")
    return data * 2

@process_data.register(list)
def _(data):
    print(f"處理列表：{[x * 2 for x in data]}")
    return [x * 2 for x in data]

# 使用
process_data("hello")  # 處理字符串：HELLO
process_data(10)       # 處理數字：20
process_data([1, 2, 3]) # 處理列表：[2, 4, 6]
process_data({"a": 1})  # 處理未知類型：{'a': 1}

# 查看註冊的類型
print(process_data.registry)
```

### 2.6 total_ordering - 自动生成比較方法

```python
from functools import total_ordering

@total_ordering
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __eq__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return self.age == other.age
    
    def __lt__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return self.age < other.age
    
    def __repr__(self):
        return f"Person({self.name}, {self.age})"

# 使用
p1 = Person("小明", 18)
p2 = Person("小紅", 20)
p3 = Person("小剛", 18)

print(p1 < p2)   # True (自動生成)
print(p1 <= p2)  # True (自動生成)
print(p1 > p2)   # False (自動生成)
print(p1 >= p2)  # False (自動生成)
print(p1 == p3)  # True (我們定義的)
print(p1 != p3)  # False (自動生成)
```

### 2.7 reduce - 歸約函數

```python
from functools import reduce

# 基礎用法
numbers = [1, 2, 3, 4, 5]

# 求和
total = reduce(lambda x, y: x + y, numbers)
print(total)  # 15

# 求積
product = reduce(lambda x, y: x * y, numbers)
print(product)  # 120

# 帶初始值
total_with_init = reduce(lambda x, y: x + y, numbers, 100)
print(total_with_init)  # 115

# 實用示例：扁平化列表
nested = [[1, 2], [3, 4], [5, 6]]
flattened = reduce(lambda x, y: x + y, nested)
print(flattened)  # [1, 2, 3, 4, 5, 6]

# 實用示例：合併字典
dicts = [{"a": 1}, {"b": 2}, {"c": 3}]
merged = reduce(lambda x, y: {**x, **y}, dicts)
print(merged)  # {'a': 1, 'b': 2, 'c': 3}
```

---

## 3️⃣ 上下文管理器深入

### 3.1 contextmanager 裝飾器

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(name="操作"):
    """計時器上下文管理器"""
    start = time.time()
    print(f"開始 {name}")
    try:
        yield
    finally:
        end = time.time()
        elapsed = end - start
        print(f"結束 {name}, 耗時：{elapsed:.4f}秒")

# 使用
with timer("計算"):
    result = sum(range(1000000))
    print(f"結果：{result}")

@contextmanager
def managed_resource(name):
    """資源管理"""
    print(f"獲取資源：{name}")
    resource = {"name": name, "status": "active"}
    try:
        yield resource
    finally:
        print(f"釋放資源：{name}")
        resource["status"] = "released"

# 使用
with managed_resource("數據庫連接") as resource:
    print(f"使用資源：{resource}")
# 獲取資源：數據庫連接
# 使用資源：{'name': '數據庫連接', 'status': 'active'}
# 釋放資源：數據庫連接
```

### 3.2 ExitStack - 動態上下文管理器

```python
from contextlib import ExitStack

# 動態管理多個上下文
def process_multiple_files(filenames):
    with ExitStack() as stack:
        files = [stack.enter_context(open(f, 'r')) for f in filenames]
        # 現在所有文件都打開了
        for file in files:
            content = file.read()
            print(f"{file.name}: {len(content)} 字節")
        # 退出時自動關閉所有文件

# 使用
# process_multiple_files(['file1.txt', 'file2.txt', 'file3.txt'])

# 條件性使用上下文
def conditional_context(use_cache):
    with ExitStack() as stack:
        if use_cache:
            cache = stack.enter_context(get_cache())
            # 使用緩存
        else:
            cache = None
        
        # 處理邏輯
        process(cache)

# 手動管理
with ExitStack() as stack:
    file1 = stack.enter_context(open('file1.txt', 'r'))
    file2 = stack.enter_context(open('file2.txt', 'r'))
    
    # 可以在運行時決定是否添加更多上下文
    if some_condition:
        file3 = stack.enter_context(open('file3.txt', 'r'))
    
    # 處理文件
```

### 3.3 suppress - 忽略異常

```python
from contextlib import suppress
import os

# 基礎用法
with suppress(FileNotFoundError):
    os.remove('nonexistent_file.txt')
# 不會報錯，靜默忽略

# 忽略多個異常
with suppress(FileNotFoundError, PermissionError):
    os.remove('some_file.txt')

# 等價於
try:
    os.remove('nonexistent_file.txt')
except (FileNotFoundError, PermissionError):
    pass
```

### 3.4 redirect_stdout/stderr - 重定向輸出

```python
from contextlib import redirect_stdout, redirect_stderr
import io

# 重定向標準輸出
f = io.StringIO()
with redirect_stdout(f):
    print("這會被重定向")
output = f.getvalue()
print(f"捕獲的輸出：{output}")

# 重定向到文件
with open('output.txt', 'w') as file:
    with redirect_stdout(file):
        print("這會寫入文件")

# 重定向標準錯誤
f = io.StringIO()
with redirect_stderr(f):
    print("這是錯誤", file=__import__('sys').stderr)
errors = f.getvalue()
```

---

## 4️⃣ 實戰：裝飾器庫

### 4.1 常用裝飾器集合

```python
from functools import wraps, lru_cache
import time
import logging

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. 日誌裝飾器
def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"調用 {func.__name__}, 參數：{args}, {kwargs}")
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} 返回：{result}")
        return result
    return wrapper

# 2. 重試裝飾器
def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(f"重試 {attempt + 1}/{max_attempts}: {e}")
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

# 3. 超時裝飾器
def timeout(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError(f"{func.__name__} 超時 ({seconds}秒)")
            
            # 設置信號
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
        return wrapper
    return decorator

# 4. 緩存裝飾器
def cache(maxsize=128, ttl=None):
    def decorator(func):
        @lru_cache(maxsize=maxsize)
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 5. 驗證裝飾器
def validate_types(**expected_types):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            
            for param_name, expected_type in expected_types.items():
                if param_name in bound.arguments:
                    value = bound.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"{func.__name__}: {param_name} 必須是 {expected_type.__name__}, "
                            f"實際是 {type(value).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 使用示例
@log_calls
@retry(max_attempts=3, delay=0.5)
@validate_types(name=str, age=int)
def create_user(name, age):
    """創建用戶"""
    print(f"創建用戶：{name}, {age}歲")
    return {"name": name, "age": age}

# 測試
user = create_user("小明", 18)
# INFO:調用 create_user, 參數：('小明', 18), {}
# 創建用戶：小明，18 歲
# INFO:create_user 返回：{'name': '小明', 'age': 18}
```

### 4.2 性能監控裝飾器

```python
from functools import wraps
import time
from collections import defaultdict

class PerformanceMonitor:
    """性能監控器"""
    def __init__(self):
        self.stats = defaultdict(lambda: {"calls": 0, "total_time": 0})
    
    def monitor(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            
            elapsed = end - start
            self.stats[func.__name__]["calls"] += 1
            self.stats[func.__name__]["total_time"] += elapsed
            
            return result
        return wrapper
    
    def report(self):
        print("性能報告:")
        print(f"{'函數':<20} {'調用次數':>10} {'總耗時':>10} {'平均耗時':>10}")
        print("-" * 55)
        for func_name, stats in self.stats.items():
            avg_time = stats["total_time"] / stats["calls"]
            print(f"{func_name:<20} {stats['calls']:>10} {stats['total_time']:>10.4f} {avg_time:>10.4f}")

# 使用
monitor = PerformanceMonitor()

@monitor.monitor
def slow_function():
    time.sleep(0.1)
    return "done"

@monitor.monitor
def fast_function():
    return "done"

# 測試
for _ in range(5):
    slow_function()
    fast_function()

# 生成報告
monitor.report()
```

---

## 📝 今日練習

### 練習 1: 實現 memoize 裝飾器

```python
from functools import wraps

def memoize(func):
    """記憶化裝飾器"""
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(50))  # 快速計算
```

### 練習 2: 實現 async_retry 裝飾器

```python
from functools import wraps
import asyncio

def async_retry(max_attempts=3, delay=1):
    """異步重試裝飾器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    await asyncio.sleep(delay)
        return wrapper
    return decorator

@async_retry(max_attempts=3, delay=0.5)
async def fetch_data(url):
    # 模擬異步請求
    await asyncio.sleep(0.1)
    raise ConnectionError("連接失敗")

# 使用
# asyncio.run(fetch_data("https://api.example.com"))
```

### 練習 3: 實現 transaction 裝飾器

```python
from functools import wraps

def transaction(db_connection):
    """數據庫事務裝飾器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            conn = db_connection()
            try:
                conn.begin()
                result = func(conn, *args, **kwargs)
                conn.commit()
                return result
            except Exception as e:
                conn.rollback()
                raise
            finally:
                conn.close()
        return wrapper
    return decorator

# 使用示例
# @transaction(get_db_connection)
# def transfer_money(conn, from_account, to_account, amount):
#     conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_account))
#     conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_account))
```

---

## 🎯 明日計劃 (Day 20)

- [ ] 上下文管理器實戰
- [ ] with 語句深入
- [ ] 資源管理最佳實踐
- [ ] 實戰：文件處理工具庫

---

**學習筆記創建時間**: 2026-03-19 06:36 GMT+8
