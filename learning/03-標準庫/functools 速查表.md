# Python functools 模塊速查表

**創建時間**: 2026-03-19  
**階段**: 第二階段 - Day 19  
**參考文檔**: https://docs.python.org/3/library/functools.html

---

## 📋 核心函數速查

### 1. wraps - 保留函數元數據

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """問候函數"""
    print(f"你好，{name}！")

print(greet.__name__)  # greet
print(greet.__doc__)   # 問候函數
```

### 2. lru_cache - 最近最少使用緩存

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 緩存信息
fibonacci.cache_info()

# 清除緩存
fibonacci.cache_clear()
```

### 3. partial - 偏函數

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
print(square(5))  # 25

cube = partial(power, exponent=3)
print(cube(3))  # 27
```

### 4. partialmethod - 偏方法

```python
from functools import partialmethod

class MyClass:
    def greet(self, greeting, name):
        print(f"{greeting}, {name}!")
    
    say_hello = partialmethod(greet, "你好")
    say_goodbye = partialmethod(greet, "再見")

obj = MyClass()
obj.say_hello("小明")    # 你好，小明!
obj.say_goodbye("小明")  # 再見，小明!
```

### 5. singledispatch - 單分派泛函

```python
from functools import singledispatch

@singledispatch
def process(data):
    return f"未知類型：{type(data)}"

@process.register(str)
def _(data):
    return f"字符串：{data.upper()}"

@process.register(int)
def _(data):
    return f"數字：{data * 2}"

print(process("hello"))  # 字符串：HELLO
print(process(10))       # 數字：20
print(process([1, 2]))   # 未知類型：<class 'list'>
```

### 6. total_ordering - 自动生成比較方法

```python
from functools import total_ordering

@total_ordering
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __eq__(self, other):
        return self.age == other.age
    
    def __lt__(self, other):
        return self.age < other.age

p1 = Person("小明", 18)
p2 = Person("小紅", 20)

print(p1 < p2)   # True (自動生成)
print(p1 <= p2)  # True (自動生成)
print(p1 > p2)   # False (自動生成)
print(p1 >= p2)  # False (自動生成)
print(p1 == p2)  # False (我們定義的)
print(p1 != p2)  # True (自動生成)
```

### 7. reduce - 歸約函數

```python
from functools import reduce

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
```

---

## 🎯 常用模式

### 模式 1: 緩存昂貴計算

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_computation(x, y):
    import time
    time.sleep(0.1)  # 模擬耗時
    return x ** y

# 第一次慢，後續快
result1 = expensive_computation(2, 10)
result2 = expensive_computation(2, 10)  # 從緩存
```

### 模式 2: 創建專用函數

```python
from functools import partial

def format_text(text, prefix="", suffix="", uppercase=False):
    if uppercase:
        text = text.upper()
    return f"{prefix}{text}{suffix}"

# 創建專用格式化函數
greet = partial(format_text, prefix="你好，", suffix="！", uppercase=True)
print(greet("小明"))  # 你好，小明！
```

### 模式 3: 類型分派

```python
from functools import singledispatch

@singledispatch
def serialize(obj):
    raise TypeError(f"不支持的類型：{type(obj)}")

@serialize.register(str)
def _(obj):
    return f'"{obj}"'

@serialize.register(int)
def _(obj):
    return str(obj)

@serialize.register(list)
def _(obj):
    return f"[{', '.join(serialize(item) for item in obj)}]"

print(serialize("hello"))     # "hello"
print(serialize(42))          # 42
print(serialize([1, 2, 3]))   # [1, 2, 3]
```

### 模式 4: 簡化比較運算

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch
    
    def __eq__(self, other):
        return (self.major, self.minor, self.patch) == \
               (other.major, other.minor, other.patch)
    
    def __lt__(self, other):
        return (self.major, self.minor, self.patch) < \
               (other.major, other.minor, other.patch)

v1 = Version(1, 0, 0)
v2 = Version(1, 2, 0)

print(v1 < v2)   # True
print(v1 <= v2)  # True
print(v1 > v2)   # False
print(v1 >= v2)  # False
```

---

## ⚡ 性能優化

### 1. 使用 lru_cache 優化遞歸

```python
# ❌ 沒有緩存 - 指數時間
def fibonacci_slow(n):
    if n < 2:
        return n
    return fibonacci_slow(n - 1) + fibonacci_slow(n - 2)

# ✅ 有緩存 - 線性時間
@lru_cache(maxsize=None)
def fibonacci_fast(n):
    if n < 2:
        return n
    return fibonacci_fast(n - 1) + fibonacci_fast(n - 2)

# 測試
import time
start = time.time()
fibonacci_fast(100)
end = time.time()
print(f"耗時：{end - start:.6f}秒")  # < 0.001 秒
```

### 2. 使用 partial 避免重複參數

```python
# ❌ 重複傳遞相同參數
def process_data(data, delimiter=",", strip=True, lowercase=False):
    # 處理邏輯
    pass

data_list = [data1, data2, data3]
for data in data_list:
    process_data(data, delimiter=",", strip=True, lowercase=False)

# ✅ 使用 partial
from functools import partial

process_csv = partial(process_data, delimiter=",", strip=True, lowercase=False)
for data in data_list:
    process_csv(data)
```

---

## 🐛 常見錯誤

### 錯誤 1: lru_cache 不能緩存可變參數

```python
# ❌ 錯誤
@lru_cache(maxsize=128)
def process_list(items):
    return sum(items)

process_list([1, 2, 3])  # TypeError: unhashable type: 'list'

# ✅ 正確 - 轉換為元組
@lru_cache(maxsize=128)
def process_list(items_tuple):
    return sum(items_tuple)

process_list(tuple([1, 2, 3]))  # ✅
```

### 錯誤 2: partial 參數順序

```python
def greet(greeting, name, punctuation="!"):
    return f"{greeting}, {name}{punctuation}"

# ❌ 錯誤 - 位置參數順序
hello = partial(greet, "小明")  # 第一個參數是 greeting，不是 name

# ✅ 正確 - 使用關鍵字參數
hello = partial(greet, name="小明")
print(hello("你好"))  # 你好，小明!
```

### 錯誤 3: singledispatch 註冊順序

```python
from functools import singledispatch

@singledispatch
def process(arg):
    return "默認"

# ✅ 正確 - 先註冊具體類型，再註冊抽象類型
@process.register(list)
def _(arg):
    return "列表"

@process.register(object)
def _(arg):
    return "對象"

# ❌ 錯誤 - 先註冊抽象類型會覆蓋具體類型
```

---

## 📖 參考資源

- **官方文檔**: https://docs.python.org/3/library/functools.html
- **PEP 3155 (lru_cache)**: https://www.python.org/dev/peps/pep-03155/
- **PEP 443 (singledispatch)**: https://www.python.org/dev/peps/pep-0443/

---

**最後更新**: 2026-03-19
