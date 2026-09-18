#!/bin/bash
set -e

echo "run on $HOSTNAME"

# HTCondor 作业需要在脚本中加载 Conda 的 Shell 支持。
source /mnt/cephfs/hot-small/dsyan/anaconda3/etc/profile.d/conda.sh
# 本示例使用 CephFS 上已有的 base；个人环境请替换为自己的共享绝对路径。
conda activate /mnt/cephfs/hot-small/dsyan/anaconda3
export PYTHONNOUSERSITE=1

python -c 'import sys; print("Python executable:", sys.executable)'
python -m pip list
exec python test.py
