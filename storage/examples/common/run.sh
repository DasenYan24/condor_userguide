#!/bin/bash
set -euo pipefail

# 第一个参数必须是已在目标节点验证可用的共享 Python 绝对路径。
python_executable="$1"
shift
if [[ "$python_executable" != /* || ! -x "$python_executable" ]]; then
    echo "共享 Python 路径不是绝对路径或不可执行：$python_executable" >&2
    exit 1
fi

export PYTHONNOUSERSITE=1
echo "执行节点：$(hostname)"
echo "启动目录：$PWD"
echo "Python：$python_executable"
# 保持 Condor 设置的工作目录；不执行 cd，不复制共享环境。
exec "$python_executable" -u "$@"
