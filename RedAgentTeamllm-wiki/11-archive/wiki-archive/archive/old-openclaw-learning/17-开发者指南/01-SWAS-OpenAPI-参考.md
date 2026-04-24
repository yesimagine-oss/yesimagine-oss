---
category: llm
created_at: '2026-04-14'
tags:
- llm
- swas
- openapi
- 参考
- api
title: 01 Swas Openapi 参考
type: general
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
# SWAS OpenAPI 参考

**学习时间**: 2026-03-12 11:51
**难度**: ⭐⭐⭐⭐⭐ 开发者级
**预计时间**: 60 分钟

---

## 📚 概述

### 什么是 SWAS OpenAPI

SWAS OpenAPI 是阿里云轻量应用服务器的编程接口，允许通过 API 自动化管理服务器。

### 适用场景

- 自动化服务器创建与销毁
- 批量管理多台服务器
- 集成到 CI/CD 流程
- 开发服务器管理工具

---

## 🔑 API 基础

### API 端点

```
https://swas.aliyuncs.com
```

### 认证方式

```
Authorization: ACS <AccessKeyId>:<Signature>
```

### 公共参数

| 参数 | 说明 | 示例 |
|------|------|------|
| Action | 操作名称 | CreateInstance |
| Version | API 版本 | 2020-03-03 |
| AccessKeyId | 访问密钥 | LTAI5t... |
| Signature | 签名 | xxx |
| Timestamp | 时间戳 | 2026-03-12T03:00:00Z |
| SignatureMethod | 签名方式 | HMAC-SHA1 |
| SignatureVersion | 签名版本 | 1.0 |
| SignatureNonce | 签名随机数 | xxx |

---

## 🔧 常用 API

### 1. 创建实例

```http
POST /
Action=CreateInstance
&Version=2020-03-03
&PackageId=swas_s1.c2m4s60b30d3s
&ImageId=ubuntu_22_04_x64_20g_alibase_20230101.vhd
&RegionId=cn-hangzhou
&InstanceName=my-server
```

### 2. 查询实例列表

```http
POST /
Action=DescribeInstances
&Version=2020-03-03
&RegionId=cn-hangzhou
&PageNumber=1
&PageSize=10
```

### 3. 启动实例

```http
POST /
Action=StartInstance
&Version=2020-03-03
&InstanceId=swas-xxx
```

### 4. 停止实例

```http
POST /
Action=StopInstance
&Version=2020-03-03
&InstanceId=swas-xxx
```

### 5. 重启实例

```http
POST /
Action=RestartInstance
&Version=2020-03-03
&InstanceId=swas-xxx
```

### 6. 查询实例详情

```http
POST /
Action=DescribeInstanceDetail
&Version=2020-03-03
&InstanceId=swas-xxx
```

### 7. 创建快照

```http
POST /
Action=CreateSnapshot
&Version=2020-03-03
&InstanceId=swas-xxx
&SnapshotName=backup-20260312
```

### 8. 查询快照列表

```http
POST /
Action=DescribeSnapshots
&Version=2020-03-03
&InstanceId=swas-xxx
```

### 9. 重置实例密码

```http
POST /
Action=ResetInstancePassword
&Version=2020-03-03
&InstanceId=swas-xxx
&Password=NewPassword123
```

### 10. 删除实例

```http
POST /
Action=DeleteInstance
&Version=2020-03-03
&InstanceId=swas-xxx
```

---

## 💻 Python SDK 示例

### 安装 SDK

```bash
pip install aliyun-python-sdk-core
pip install aliyun-python-sdk-swas
```

### 创建实例

```python
from aliyunsdkcore.client import AcsClient
from aliyunsdkswas.request.v20200303.CreateInstanceRequest import CreateInstanceRequest

# 初始化客户端
client = AcsClient('<accessKeyId>', '<accessSecret>', 'cn-hangzhou')

# 创建请求
request = CreateInstanceRequest()
request.set_PackageId('swas_s1.c2m4s60b30d3s')
request.set_ImageId('ubuntu_22_04_x64_20g_alibase_20230101.vhd')
request.set_RegionId('cn-hangzhou')
request.set_InstanceName('my-server')

# 发送请求
response = client.do_action_with_exception(request)
print(response)
```

### 查询实例列表

```python
from aliyunsdkswas.request.v20200303.DescribeInstancesRequest import DescribeInstancesRequest

request = DescribeInstancesRequest()
request.set_PageNumber(1)
request.set_PageSize(10)
request.set_RegionId('cn-hangzhou')

response = client.do_action_with_exception(request)
print(response)
```

### 创建快照

```python
from aliyunsdkswas.request.v20200303.CreateSnapshotRequest import CreateSnapshotRequest

request = CreateSnapshotRequest()
request.set_InstanceId('swas-xxx')
request.set_SnapshotName('backup-' + datetime.now().strftime('%Y%m%d'))

response = client.do_action_with_exception(request)
print(response)
```

---

## 💻 Node.js SDK 示例

### 安装 SDK

```bash
npm install @alicloud/swas20200303
```

### 创建实例

```javascript
const Swas20200303 = require('@alicloud/swas20200303').default;
const OpenApi = require('@alicloud/openapi-client').default;

const config = new OpenApi.Config({
  accessKeyId: '<accessKeyId>',
  accessKeySecret: '<accessSecret>',
  endpoint: 'swas.aliyuncs.com'
});

const client = new Swas20200303.default(config);

const request = new Swas20200303.CreateInstanceRequest({
  packageId: 'swas_s1.c2m4s60b30d3s',
  imageId: 'ubuntu_22_04_x64_20g_alibase_20230101.vhd',
  regionId: 'cn-hangzhou',
  instanceName: 'my-server'
});

const response = await client.CreateInstance(request);
console.log(response);
```

---

## 🔒 签名机制

### 签名步骤

1. 获取所有请求参数
2. 按参数名排序
3. 构造待签名字符串
4. 使用 AccessKeySecret 进行 HMAC-SHA1 签名
5. 将签名添加到请求中

### 签名示例

```python
import hmac
import hashlib
import base64
import urllib.parse

def sign_string(string_to_sign, access_key_secret):
    h = hmac.new(
        (access_key_secret + '&').encode('utf-8'),
        string_to_sign.encode('utf-8'),
        hashlib.sha1
    )
    return base64.b64encode(h.digest()).decode('utf-8')

# 使用示例
signature = sign_string(string_to_sign, access_key_secret)
```

---

## ⚠️ 错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| InvalidParameter | 参数错误 | 检查参数格式 |
| InstanceNotFound | 实例不存在 | 检查实例 ID |
| InsufficientBalance | 余额不足 | 充值账户 |
| OperationDenied | 操作被拒绝 | 检查权限 |
| TooManyRequests | 请求过多 | 降低频率 |

---

## 📊 最佳实践

### 1. 错误重试

```python
from retry import retry

@retry(tries=3, delay=2)
def create_instance():
    response = client.do_action_with_exception(request)
    return response
```

### 2. 批量操作

```python
# 批量创建实例
instance_ids = []
for i in range(5):
    request.set_InstanceName(f'my-server-{i}')
    response = client.do_action_with_exception(request)
    instance_ids.append(response['InstanceId'])
```

### 3. 资源清理

```python
# 自动清理过期实例
def cleanup_old_instances():
    instances = client.describe_instances()
    for instance in instances:
        if is_expired(instance['CreationTime']):
            client.delete_instance(instance['InstanceId'])
```

---

## ✅ 验收清单

- [ ] 理解 API 基础
- [ ] 掌握常用 API
- [ ] 能够使用 SDK
- [ ] 了解签名机制
- [ ] 能够处理错误

---

**学习状态**: ✅ 已完成
**备注**: 开发者级内容，实际使用时查阅官方文档

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[01-openai-genes]]
- [[01-evomap_asset_structure_validate]]
- [[01-github-genes]]
