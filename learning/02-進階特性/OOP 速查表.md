# Python OOP 速查表

**創建時間**: 2026-03-19  
**階段**: 第二階段 - Day 15  
**參考文檔**: https://docs.python.org/3/tutorial/classes.html

---

## 📋 核心概念速查

### 1. 類的定義

```python
class ClassName:
    """文檔字符串"""
    
    class_attr = "類屬性"  # 類屬性
    
    def __init__(self, param):
        self.instance_attr = param  # 實例屬性
    
    def instance_method(self):  # 實例方法
        return self.instance_attr
    
    @classmethod
    def class_method(cls):  # 類方法
        return cls.class_attr
    
    @staticmethod
    def static_method():  # 靜態方法
        return "無 cls/self"
```

### 2. 繼承

```python
class Child(Parent):
    def __init__(self):
        super().__init__()  # 調用父類構造函數
    
    def method(self):
        super().method()  # 調用父類方法
```

### 3. 特殊方法

| 方法 | 用途 | 示例 |
|------|------|------|
| `__init__` | 初始化 | `def __init__(self, x):` |
| `__str__` | 用戶友好字符串 | `print(obj)` |
| `__repr__` | 開發者字符串 | `repr(obj)` |
| `__len__` | 長度 | `len(obj)` |
| `__getitem__` | 索引訪問 | `obj[key]` |
| `__setitem__` | 索引設置 | `obj[key] = value` |
| `__delitem__` | 索引刪除 | `del obj[key]` |
| `__iter__` | 迭代器 | `for x in obj:` |
| `__next__` | 下一個元素 | `next(iterator)` |
| `__contains__` | in 運算 | `x in obj` |
| `__add__` | 加法 | `obj1 + obj2` |
| `__sub__` | 減法 | `obj1 - obj2` |
| `__mul__` | 乘法 | `obj * n` |
| `__eq__` | 等於 | `obj1 == obj2` |
| `__lt__` | 小於 | `obj1 < obj2` |
| `__le__` | 小於等於 | `obj1 <= obj2` |
| `__gt__` | 大於 | `obj1 > obj2` |
| `__ge__` | 大於等於 | `obj1 >= obj2` |
| `__enter__` | 進入上下文 | `with obj:` |
| `__exit__` | 退出上下文 | `with obj:` |

### 4. 屬性裝飾器

```python
class MyClass:
    def __init__(self):
        self._value = 0
    
    @property
    def value(self):
        """getter"""
        return self._value
    
    @value.setter
    def value(self, new_value):
        """setter"""
        self._value = new_value
    
    @value.deleter
    def value(self):
        """deleter"""
        del self._value
```

### 5. 抽象基類

```python
from abc import ABC, abstractmethod

class MyAbstract(ABC):
    @abstractmethod
    def my_method(self):
        pass
    
    @abstractmethod
    def my_other_method(self):
        pass
```

### 6. 數據類 (Python 3.7+)

```python
from dataclasses import dataclass, field

@dataclass
class DataClass:
    name: str
    value: int = 0
    items: list = field(default_factory=list)
```

---

## 🎯 最佳實踐

### ✅ 推薦做法

1. **使用 docstring** - 為類和方法添加文檔
2. **使用 property** - 控制屬性訪問
3. **優先組合而非繼承** - 避免過度繼承
4. **使用抽象基類** - 定義接口規範
5. **實現特殊方法** - 讓對象更 Pythonic

### ❌ 避免做法

1. **避免過度使用繼承** - 優先使用組合
2. **避免直接訪問私有屬性** - 使用公開接口
3. **避免濫用靜態方法** - 考慮是否應該是模塊函數
4. **避免複雜的多重繼承** - 容易導致 MRO 混亂

---

## 📚 常用設計模式

### 單例模式

```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 工廠模式

```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "汪汪"

class Cat(Animal):
    def speak(self):
        return "喵喵"

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        raise ValueError("未知動物類型")
```

### 觀察者模式

```python
class Subject:
    def __init__(self):
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self)

class Observer:
    def update(self, subject):
        pass
```

---

## 🔍 調試技巧

### 查看類信息

```python
obj = MyClass()

# 查看類型
type(obj)

# 查看 MRO (方法解析順序)
MyClass.__mro__

# 查看實例屬性
obj.__dict__

# 查看類屬性
MyClass.__dict__

# 查看方法
dir(obj)

# 查看文檔
help(MyClass)
```

### 檢查繼承關係

```python
isinstance(obj, MyClass)      # 是否是實例
issubclass(Child, Parent)     # 是否是子類
hasattr(obj, 'attr')          # 是否有屬性
getattr(obj, 'attr', default) # 獲取屬性
setattr(obj, 'attr', value)   # 設置屬性
delattr(obj, 'attr')          # 刪除屬性
```

---

## 📖 參考資源

- **官方教程**: https://docs.python.org/3/tutorial/classes.html
- **數據模型**: https://docs.python.org/3/reference/datamodel.html
- **abc 模塊**: https://docs.python.org/3/library/abc.html
- **dataclasses**: https://docs.python.org/3/library/dataclasses.html

---

**最後更新**: 2026-03-19
