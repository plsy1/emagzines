#!/bin/bash
set -e

# 用法：./run_local.sh <杂志ID> [你的GITHUB_TOKEN]
MAG_ID=$1
TOKEN=$2

# 1. 优先检测本地 .secrets 文件
if [ -f ".secrets" ]; then
    # 尝试读取 .secrets 中的 GITHUB_TOKEN=xxxx 这一行
    # (有些 shell 下 source 可能报错，直接用 grep/sed 拿最稳)
    FILE_TOKEN=$(grep '^GITHUB_TOKEN=' .secrets | cut -d'=' -f2)
    [ -z "$TOKEN" ] && TOKEN=$FILE_TOKEN
fi

if [ -z "$MAG_ID" ] || [ -z "$TOKEN" ]; then
    echo "用法: ./run_local.sh <杂志ID> [GITHUB_TOKEN]"
    echo ""
    echo "✅ 建议配置方案：只需一次"
    echo "在当前目录下创建一个名为 .secrets 的文件，内容填写为："
    echo "GITHUB_TOKEN=你的_ghp_xxx_密钥"
    echo ""
    echo "这样以后只需直接运行: ./run_local.sh te"
    exit 1
fi

# 检查文件是否存在
if [ ! -f ".github/workflows/${MAG_ID}.yml" ]; then
    echo "错误：未发现对应的工作流文件 .github/workflows/${MAG_ID}.yml"
    exit 1
fi

echo "--- 正在通过 act 并在本地网络下抓取 $MAG_ID ---"

# 调用 act 运行指定的工作流，并传入关键的 TOKEN 用于最终推送
# 如果是 M 系列芯片，act 会自动处理对应的 arm64 环境
act workflow_dispatch -W ".github/workflows/${MAG_ID}.yml" \
  -s GITHUB_TOKEN="$TOKEN"

echo "--- 抓取及同步流程已在容器内完成！ ---"
