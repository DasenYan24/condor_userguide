# 在 HTCondor 集群中运行 Python 程序

本目录包含在 HTCondor 集群中运行 Python 程序的示例和说明。

## 目录结构

- `test.py` - Python 示例程序
- `run.sh` - 执行脚本
- `test.submit` - HTCondor 作业提交文件

## 环境配置

### 重要提示

**环境必须在目标执行节点可用，不能只在提交节点本地安装。** 本教程和 `run.sh` 统一使用 CephFS 上已有的 `/mnt/cephfs/hot-small/dsyan/anaconda3`。目标节点需要挂载 `/mnt/cephfs`，作业账号需要有环境的读取和执行权限。共享挂载并不自动保证运行库和依赖兼容，仍需通过实际作业验证；目录与文件传输的关系见[存储实践](../storage/README.md)。

### 使用共享 Conda 环境

集群已在 `/mnt/cephfs/hot-small/dsyan/anaconda3` 安装 Anaconda，**无需重复安装**。该安装由 `dsyan` 维护，其他已授权用户可读取和执行。其中 `base` 的路径就是该目录；本目录的小型示例默认使用这个已有环境。

在获准登录的提交节点上，显式加载这套 Conda 并确认实际 Python 路径，不要只凭终端中的 `(base)` 判断：

```bash
source /mnt/cephfs/hot-small/dsyan/anaconda3/etc/profile.d/conda.sh
conda activate /mnt/cephfs/hot-small/dsyan/anaconda3
python -c 'import sys; print(sys.executable)'
```

预期输出 `/mnt/cephfs/hot-small/dsyan/anaconda3/bin/python`。公共环境由维护者管理；自己的项目依赖应安装到下面创建的个人环境，不要直接修改公共 `base`。

### 查看可用环境

使用这套 Conda 查看当前用户已登记的环境及其路径：

```bash
/mnt/cephfs/hot-small/dsyan/anaconda3/bin/conda info -e
```

查看 base 环境的所有安装包：

```bash
/mnt/cephfs/hot-small/dsyan/anaconda3/bin/conda run -p /mnt/cephfs/hot-small/dsyan/anaconda3 python -m pip list
```

### 创建自己的环境

正式项目建议在 `hot-small` 下的个人目录创建环境。下面以 `myproject` 为例，可替换为自己的项目名；环境目录无需放入公共 Anaconda 安装目录：

```bash
ENV_PREFIX="/mnt/cephfs/hot-small/$(id -un)/envs/myproject"
mkdir -p "$(dirname "$ENV_PREFIX")"
/mnt/cephfs/hot-small/dsyan/anaconda3/bin/conda create -p "$ENV_PREFIX" python=3.12
```

如果个人目录无法创建或不可写，请联系管理员核对权限；不要修改公共目录的所有权或权限。以下步骤在同一终端继续执行，保留 `ENV_PREFIX`；新终端需重新设置为同一个实际路径。

### 安装 Python 包

1. 激活刚创建的个人环境，并确认解释器和用户包加载设置：

```bash
source /mnt/cephfs/hot-small/dsyan/anaconda3/etc/profile.d/conda.sh
conda activate "$ENV_PREFIX"
export PYTHONNOUSERSITE=1
python -c 'import sys; print(sys.executable); print(sys.prefix)'
python -m site
```

解释器应为 `$ENV_PREFIX/bin/python`，`sys.prefix` 应为个人环境目录。`ENABLE_USER_SITE: False` 表示不加载用户目录中的包；它本身不能证明安装目标正确，仍需核对解释器路径，含义见 [Python 官方说明](https://docs.python.org/3/library/site.html#site.ENABLE_USER_SITE)。

2. 在同一个个人环境中安装项目依赖。示例程序需要 NumPy：

```bash
python -m pip install numpy
python -c 'import numpy; print(numpy.__file__)'
```

**注意**：集群中有 3090 和 4090 不同型号的 GPU，安装的包可能对 GPU 型号有要求。

## 使用步骤

### 1. 编写 Python 程序

创建您的 Python 程序，例如 `test.py`。

### 2. 创建执行脚本

本目录的 `run.sh` 已采用 `conda activate` 方式，核心步骤为：

```bash
source /mnt/cephfs/hot-small/dsyan/anaconda3/etc/profile.d/conda.sh
conda activate /mnt/cephfs/hot-small/dsyan/anaconda3
export PYTHONNOUSERSITE=1
```

脚本默认使用 `hot-small` 上已有的共享 `base`，可直接用于本目录的小型示例。如果前面创建并安装了个人环境，请将 `run.sh` 中 `conda activate` 后面的路径改为该环境的完整路径，例如 `/mnt/cephfs/hot-small/<用户名>/envs/myproject`，把 `<用户名>` 替换为真实账号名。**创建环境、安装依赖和提交运行必须使用同一个环境**；不要假定提交端的 `ENV_PREFIX` 会自动传入作业。

HTCondor 作业需要在脚本中自行加载并激活 Conda，不能只依赖提交前在终端中执行过的激活操作。`PYTHONNOUSERSITE=1` 用于避免加载用户目录中的 Python 包；脚本中的 `set -e` 会在加载或激活环境失败时停止执行。脚本先打印实际解释器路径，再使用 `python -m pip list` 输出依赖清单，最后通过 `exec python test.py` 运行程序。

如果自行创建或复制脚本，记得设置执行权限：

```bash
chmod +x run.sh
```

### 3. 修改提交文件

修改 `test.submit` 文件中的参数：

- `initialdir` - 修改为提交节点上的项目路径；启用传输后，程序实际从执行节点的临时目录启动
- `request_GPUs` - 如需要 GPU，设置数量
- `request_CPUs` - 设置所需的 CPU 数量
- `transfer_input_files` - 列出所有需要传输的文件
- `arguments` - 设置传递给脚本的参数

### 4. 提交作业

先进入 `initialdir` 指定的项目目录，创建日志目录后再提交：

```bash
mkdir -p logs
csub test.submit
```

或

```bash
condor_submit test.submit
```

### 5. 查看结果

本例标准输出和标准错误默认在作业退出后回传到 `initialdir` 下的 `logs/`，事件日志则由提交节点记录：

- 标准输出：`logs/job_<ClusterId>.<ProcId>.out`
- 错误输出：`logs/job_<ClusterId>.<ProcId>.err`
- HTCondor 日志：`logs/job_<ClusterId>.log`

## 注意事项

### 验证环境

提交文件中的节点限制默认被注释。验证环境时，可先启用其中一条限制，把小型任务定向到一个已获准使用的在线节点，例如：

```
Requirements = (TARGET.Machine=="hengshan")
```

检查作业输出中的 `Python executable:` 是否指向期望的 `hot-small` 环境，以及是否输出 `python is ok!`。一次成功只验证该执行节点；计划运行的目标节点逐一验证后，再按需要放宽节点限制。

### 短作业优化

如果程序运行时间少于 30 分钟，启用短作业标志：

```
+SHORT_JOB=true
```

### 传输文件

本例采用 `should_transfer_files = YES`：`run.sh` 默认随 executable 传输，`test.py` 列在 `transfer_input_files` 中；程序在执行节点的临时目录运行。脚本加载的 `/mnt/cephfs/hot-small/dsyan/anaconda3` 环境通过共享绝对路径访问，不会自动复制到临时目录。

只把需要复制的其他代码、配置和小输入列入 `transfer_input_files`。共享数据使用绝对路径直接读取时，不必重复传输。程序在相对路径写结果与直接写 `/mnt/cephfs/...` 的保存方式不同；`output`、`error` 也不是模型结果目录。具体规则和三个完整实例见[共享存储、文件传输与作业目录](../storage/README.md)。

## 故障排查

1. 检查作业匹配情况：

```bash
cq -better-analyze <jobid>
```

2. 查看详细信息：

```bash
cq -l <jobid>
```

3. 查看实时输出：

```bash
condor_tail <jobid>
```

4. 检查 Python 路径是否正确：

   - 核对日志中的 `Python executable:`，应指向 `/mnt/cephfs/hot-small/dsyan/anaconda3/bin/python` 或自己的 `hot-small` 环境。
   - 通过 `sys.prefix`、`numpy.__file__` 等确认实际环境及依赖位置；`sys.path` 还可能包含作业代码目录，不能要求其中所有路径都位于环境目录。
   - 确认目标节点已挂载 CephFS、账号有访问权限，并避免加载仅存在于某台机器 Home 下的包。
