#!/bin/bash
set -e

# 用法：./run_local.sh <杂志ID> [你的GITHUB_TOKEN] [日期]
MAG_ID=$1
TOKEN=$2
ISSUE_DATE=$3

# 1. 优先检测本地 .secrets 文件
if [ -f ".secrets" ]; then
    # 尝试读取 .secrets 中的 GITHUB_TOKEN=xxxx 这一行
    FILE_TOKEN=$(grep '^GITHUB_TOKEN=' .secrets | cut -d'=' -f2)
    [ -z "$TOKEN" ] && TOKEN=$FILE_TOKEN
fi

if [ -z "$MAG_ID" ] || [ -z "$TOKEN" ]; then
    echo "用法: ./run_local.sh <杂志ID> [GITHUB_TOKEN] [日期]"
    echo ""
    echo "✅ 建议配置方案：只需一次"
    echo "在当前目录下创建一个名为 .secrets 的文件，内容填写为："
    echo "GITHUB_TOKEN=你的_ghp_xxx_密钥"
    echo ""
    echo "这样以后只需直接运行: ./run_local.sh te"
    echo "抓取特定日期: ./run_local.sh te 你的TOKEN 2024-05-04"
    exit 1
fi

# 检查文件是否存在
if [ ! -f ".github/workflows/${MAG_ID}.yml" ]; then
    echo "错误：未发现对应的工作流文件 .github/workflows/${MAG_ID}.yml"
    exit 1
fi

# 调用 act 运行指定的工作流
if [ -n "$ISSUE_DATE" ]; then
    act workflow_dispatch -W ".github/workflows/${MAG_ID}.yml" \
      -s GITHUB_TOKEN="$TOKEN" \
      --input issue_date="$ISSUE_DATE"
else
    act workflow_dispatch -W ".github/workflows/${MAG_ID}.yml" \
      -s GITHUB_TOKEN="$TOKEN"
fi

echo "--- 抓取及同步流程已在容器内完成！ ---"
