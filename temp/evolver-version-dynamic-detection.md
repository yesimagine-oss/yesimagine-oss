# Evolver 版本号动态检测学习记录

**学习日期**: 2026-04-03 07:17  
**主题**: 禁止硬编码版本号，使用动态检测  
**级别**: ⭐⭐⭐⭐⭐ 核心技能

---

## 📚 学习背景

### 问题现象

```
❌ "已检测到 evolver 环境，但未能获取版本号。请更新 evolver 至最新版本 (>= 1.26.0)"
```

### 根因分析

**错误代码** (`lib/gep_a2a_client.py:183`):

```python
# ❌ 硬编码版本号
if not evolver_version:
    evolver_version = '1.39.0'  # 问题：升级后仍使用旧版本号
```

**问题本质**:
1. 软件升级后，代码中的硬编码版本号未同步更新
2. Hub 检测到旧版本号，提示升级
3. 用户困惑：明明已升级，为什么还提示旧版本？

---

## 💡 解决方案

### 核心原则

**永远不要硬编码版本号**

```
❌ 错误：version = '1.39.0'
✅ 正确：version = read_version_from_package()
```

---

### 动态检测三层策略

```python
def get_evolver_version():
    """
    动态获取 evolver 版本号
    优先级：本地 node_modules → 项目 package.json → 全局 npm list → 'unknown'
    """
    
    # 方法 1: 从本地 node_modules 读取（最准确）
    own_pkg_path = Path(__file__).parent.parent / 'node_modules' / '@evomap' / 'evolver' / 'package.json'
    try:
        if own_pkg_path.exists():
            pkg = json.loads(own_pkg_path.read_text())
            return pkg.get('version')
    except:
        pass
    
    # 方法 2: 从项目根目录 package.json 读取
    try:
        repo_pkg = Path(__file__).parent.parent / 'package.json'
        if repo_pkg.exists():
            pkg = json.loads(repo_pkg.read_text())
            return pkg.get('version')
    except:
        pass
    
    # 方法 3: 从全局 npm list 读取（兜底）
    try:
        import subprocess
        result = subprocess.run(
            ['npm', 'list', '-g', '@evomap/evolver'],
            capture_output=True,
            text=True,
            timeout=10
        )
        for line in result.stdout.split('\n'):
            if '@evomap/evolver@' in line:
                return line.split('@evomap/evolver@')[1].strip()
    except:
        pass
    
    # 最终降级（不硬编码具体版本号）
    return 'unknown'
```

---

## 🎯 关键学习点

### 1. 为什么不能硬编码版本号？

| 硬编码 | 动态读取 |
|--------|---------|
| ❌ 升级后需要修改代码 | ✅ 升级后自动生效 |
| ❌ 容易忘记更新 | ✅ 始终反映真实版本 |
| ❌ 多环境版本不一致 | ✅ 每个环境独立读取 |
| ❌ 维护成本高 | ✅ 零维护成本 |

---

### 2. 版本号读取优先级

```
1. 本地 node_modules/@evomap/evolver/package.json  ← 最准确
   ↓ (失败)
2. 项目根目录 package.json
   ↓ (失败)
3. 全局 npm list -g @evomap/evolver  ← 兜底
   ↓ (失败)
4. 返回 'unknown'（不硬编码具体版本号）
```

**原理**: 
- 本地安装优先（项目依赖）
- 全局安装兜底（系统环境）
- 降级为 'unknown'（避免误导）

---

### 3. 环境指纹正确结构

```python
# ✅ 正确：版本号在 env_fingerprint 内部
env_fingerprint = {
    'evolver_version': version,      # ← 正确位置
    'client_version': version,       # ← 正确位置
    'client': 'evolver',
    'device_id': 'xxx',
    # ...
}

# ❌ 错误：版本号平铺在 payload 外层
payload = {
    'evolver_version': version,      # ← Hub 读不到
    'env_fingerprint': {...},
}
```

---

## 📖 相关知识点

### npm 版本管理

```bash
# 查看全局版本
npm list -g @evomap/evolver

# 查看本地版本
npm list @evomap/evolver

# 升级全局版本
sudo npm install -g @evomap/evolver@latest

# 升级本地版本
npm install @evomap/evolver@latest
```

---

### 权限问题处理

**问题**: `npm install -g` 权限不足

```
npm error EACCES: permission denied, rename '/usr/lib/node_modules/...'
```

**解决方案**:

```bash
# 方案 1: 使用 sudo（简单直接）
sudo npm install -g <package>

# 方案 2: 修改 npm 默认目录（推荐）
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH

# 方案 3: 使用 nvm（Node 版本管理）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install node
```

---

## 🔧 实战应用

### 场景 1: Python 项目读取 Node.js 包版本

```python
import subprocess
import json
from pathlib import Path

def get_package_version(package_name):
    """通用包版本读取函数"""
    
    # 方法 1: 读取 package.json
    pkg_json = Path('node_modules') / package_name / 'package.json'
    if pkg_json.exists():
        return json.loads(pkg_json.read_text()).get('version')
    
    # 方法 2: npm list
    try:
        result = subprocess.run(
            ['npm', 'list', '-g', package_name],
            capture_output=True,
            text=True
        )
        for line in result.stdout.split('\n'):
            if f'{package_name}@' in line:
                return line.split(f'{package_name}@')[1].strip()
    except:
        pass
    
    return 'unknown'

# 使用
version = get_package_version('@evomap/evolver')
print(f"Evolver 版本：{version}")
```

---

### 场景 2: 多语言项目版本同步

```python
# Python 版本
PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

# Node.js 版本
NODE_VERSION = subprocess.check_output(['node', '--version']).decode().strip()

# Evolver 版本
EVOLVER_VERSION = get_package_version('@evomap/evolver')

# 环境指纹
env_fingerprint = {
    'python_version': PYTHON_VERSION,
    'node_version': NODE_VERSION,
    'evolver_version': EVOLVER_VERSION,
    'platform': platform.system(),
    'arch': platform.machine(),
}
```

---

## ⚠️ 常见错误

### 错误 1: 硬编码版本号

```python
# ❌ 错误
VERSION = '1.39.0'

# ✅ 正确
VERSION = get_package_version('@evomap/evolver')
```

---

### 错误 2: 忽略异常处理

```python
# ❌ 错误（可能崩溃）
version = subprocess.check_output(['npm', 'list', '-g', 'pkg']).decode()

# ✅ 正确（安全降级）
try:
    version = subprocess.check_output(['npm', 'list', '-g', 'pkg'], timeout=10).decode()
except:
    version = 'unknown'
```

---

### 错误 3: 版本号位置错误

```python
# ❌ 错误（Hub 读不到）
payload = {
    'version': '1.39.0',  # 平铺在外层
    'env_fingerprint': {...}
}

# ✅ 正确（Hub 能读取）
payload = {
    'env_fingerprint': {
        'evolver_version': '1.39.0'  # 在 env_fingerprint 内部
    }
}
```

---

## 📝 检查清单

**代码审查时检查**:

- [ ] 是否有硬编码的版本号字符串？
- [ ] 版本号是否动态读取？
- [ ] 是否有异常处理（try/except）？
- [ ] 是否有降级策略（返回 'unknown'）？
- [ ] 版本号位置是否正确（env_fingerprint 内部）？

---

## 🎓 延伸学习

### 相关技能

1. **Python subprocess 模块** - 执行系统命令
2. **Node.js package.json 结构** - 读取包元数据
3. **语义化版本号 (SemVer)** - 版本号规范
4. **环境变量管理** - 配置与代码分离

### 推荐资源

- [Python subprocess 文档](https://docs.python.org/3/library/subprocess.html)
- [npm package.json 规范](https://docs.npmjs.com/cli/v10/configuring-npm/package-json)
- [语义化版本 2.0.0](https://semver.org/)

---

## 📅 复习计划

| 时间 | 内容 |
|------|------|
| **1 天后** | 回顾动态检测三层策略 |
| **1 周后** | 实践：为其他包添加动态版本检测 |
| **1 月后** | 检查是否有新的硬编码版本号 |

---

**学习总结**: 
> 版本号是动态信息，不是常量。永远从源头读取，不要硬编码。
> 这是软件工程中"单一事实来源"(Single Source of Truth)原则的体现。

**下次遇到类似问题**:
1. 搜索代码中的硬编码版本号
2. 替换为动态读取函数
3. 添加异常处理和降级策略
4. 验证版本号位置正确

---

**学习完成时间**: 2026-04-03 07:17  
**学习者**: RedOpenClaw
