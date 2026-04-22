#!/bin/bash

# goToken-v2 测试运行脚本

echo "🧪 goToken-v2 测试套件"
echo "================================"

# 进入测试目录
cd "$(dirname "$0")"

# 检查 Go 是否安装
if ! command -v go &> /dev/null; then
    echo "❌ Go 未安装，请先安装 Go"
    exit 1
fi

# 编译测试
echo "📦 编译测试套件..."
go build -o test_runner test_suite.go

if [ $? -ne 0 ]; then
    echo "❌ 编译失败"
    exit 1
fi

echo "✅ 编译成功"
echo ""

# 运行测试
echo "🚀 运行测试..."
./test_runner

# 清理
rm -f test_runner

echo ""
echo "================================"
echo "✅ 测试完成"
