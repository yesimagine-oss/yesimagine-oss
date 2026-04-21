# Python MRO 速查表

**創建時間**: 2026-03-19  
**主題**: 多重繼承與方法解析順序  
**參考文檔**: https://docs.python.org/3/howto/mro.html

---

## 📋 核心概念

### 什麼是 MRO？

**MRO (Method Resolution Order)** 方法解析順序，決定了 Python 在多重繼承中查找方法的順序。

### Python 3 的 MRO 算法

Python 3 使用 **C3 線性化算法**，確保：
1. 子類優先於父類
2. 保持繼承聲明中的順序
3. 單調性（子類的 MRO 不會破壞父類的 MRO）

---

## 🔍 查看 MRO

### 方法 1: `__mro__` 屬性

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print(D.__mro__)
# (<class '__main__.D'>, <class '__main__.B'>, 
#  <class '__main__.C'>, <class '__main__.A'>, 
#  <class 'object'>)
```

### 方法 2: `mro()` 方法

```python
print(D.mro())
# 返回相同的結果，但是列表形式
```

### 方法 3: `help()` 函數

```python
help(D)
# 在幫助信息中查看 Method resolution order:
```

---

## 📊 MRO 示例

### 示例 1: 簡單多重繼承

```python
class A:
    def method(self):
        return "A"

class B:
    def method(self):
        return "B"

class C(A, B):
    pass

c = C()
print(c.method())  # 輸出："A" (A 在 B 之前)
print(C.__mro__)
# C -> A -> B -> object
```

### 示例 2: 鑽石繼承

```python
class A:
    def method(self):
        return "A"

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass

print(D.__mro__)
# D -> B -> C -> A -> object
# 注意：A 只出現一次！

d = D()
print(d.method())  # "A"
```

### 示例 3: 複雜繼承

```python
class O: pass
class A(O): pass
class B(O): pass
class C(A): pass
class D(B): pass
class E(C, D): pass

print(E.__mro__)
# E -> C -> A -> D -> B -> O -> object
```

---

## 🛠️ super() 的正確使用

### 錯誤用法

```python
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")
        A.method(self)  # ❌ 直接調用父類，跳過 MRO

class C(A):
    def method(self):
        print("C")
        A.method(self)  # ❌ 直接調用父類，跳過 MRO

class D(B, C):
    def method(self):
        print("D")
        B.method(self)  # ❌ 直接調用，跳過 MRO

d = D()
d.method()
# 輸出:
# D
# B
# A
# C 被跳過了！
```

### 正確用法

```python
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")
        super().method()  # ✅ 使用 super()

class C(A):
    def method(self):
        print("C")
        super().method()  # ✅ 使用 super()

class D(B, C):
    def method(self):
        print("D")
        super().method()  # ✅ 使用 super()

d = D()
d.method()
# 輸出:
# D
# B
# C
# A
# 所有類都被調用了！
```

---

## ⚠️ 常見陷阱

### 陷阱 1: 不一致的繼承層次

```python
class A: pass
class B: pass

# ❌ 這會報錯：TypeError
# class C(A, B): pass
# class D(B, A): pass
# class E(C, D): pass

# MRO 衝突：C 要求 A 在 B 之前，D 要求 B 在 A 之前
```

### 陷阱 2: 忘記調用 super()

```python
class A:
    def __init__(self):
        print("A init")

class B(A):
    def __init__(self):
        print("B init")
        # ❌ 忘記 super().__init__()

class C(A):
    def __init__(self):
        print("C init")
        # ❌ 忘記 super().__init__()

class D(B, C):
    def __init__(self):
        print("D init")
        super().__init__()

d = D()
# 輸出:
# D init
# B init
# A 和 C 的 __init__ 都沒有被調用！
```

### 陷阱 3: 混合使用 super() 和直接調用

```python
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")
        super().method()

class C(A):
    def method(self):
        print("C")
        A.method(self)  # ❌ 直接調用，破壞 MRO

class D(B, C):
    def method(self):
        print("D")
        super().method()

d = D()
d.method()
# 輸出:
# D
# B
# A
# C 被跳過了！
```

---

## 🎯 最佳實踐

### ✅ 推薦做法

1. **始終使用 super()** - 在多重繼承中
2. **保持一致的簽名** - 所有父類方法參數應兼容
3. **使用關鍵字參數** - 避免位置參數衝突
4. **繪製繼承圖** - 複雜繼承時先畫圖

### ❌ 避免做法

1. **避免深度多重繼承** - 超過 3 層就很複雜
2. **避免鑽石繼承** - 除非必要
3. **避免混合使用 super() 和直接調用**
4. **避免循環依賴** - A 繼承 B，B 繼承 A

---

## 📐 C3 線性化算法簡述

### 算法規則

對於類 `C(B1, B2, ..., BN)`，MRO 計算：

```
L[C] = [C] + merge(L[B1], L[B2], ..., L[BN], [B1, B2, ..., BN])
```

### merge 操作

1. 檢查每個列表的頭部
2. 如果某個頭部不在其他列表的尾部，選擇它
3. 否則，跳過該列表，檢查下一個
4. 重複直到所有列表為空

### 示例

```python
class O: pass
class A(O): pass
class B(O): pass
class C(A): pass
class D(B): pass
class E(C, D): pass

# L[O] = [O]
# L[A] = [A, O]
# L[B] = [B, O]
# L[C] = [C, A, O]
# L[D] = [D, B, O]

# L[E] = [E] + merge(L[C], L[D], [C, D])
#      = [E] + merge([C,A,O], [D,B,O], [C,D])
#      = [E, C] + merge([A,O], [D,B,O], [D])
#      = [E, C, A] + merge([O], [D,B,O], [D])
#      = [E, C, A, D] + merge([O], [B,O])
#      = [E, C, A, D, B] + merge([O], [O])
#      = [E, C, A, D, B, O]
```

---

## 🔧 調試工具

### 打印 MRO

```python
def print_mro(cls):
    print(f"{cls.__name__} 的 MRO:")
    for i, c in enumerate(cls.__mro__, 1):
        print(f"  {i}. {c.__name__}")

print_mro(E)
```

### 檢查方法調用順序

```python
class Tracer:
    def __init__(self, name):
        self.name = name
    
    def method(self):
        print(f"{self.name}.method")
        if hasattr(super(), 'method'):
            super().method()

class A(Tracer): pass
class B(Tracer): pass
class C(A, B): pass

c = C("C")
c.method()
```

---

## 📚 參考資源

- **官方文檔**: https://docs.python.org/3/howto/mro.html
- **Python 2.3 MRO**: https://www.python.org/download/releases/2.3/mro/
- **C3 算法論文**: https://www.cs.auckland.ac.nz/~j-hamer/0708CS702-C3.pdf

---

**最後更新**: 2026-03-19
