# 运行三个存储示例

先阅读[目录与传输规则](../README.md)。三个示例共用 [run.sh](common/run.sh) 和 [inspect_paths.py](common/inspect_paths.py)，计算 `1 + 2 + 3`，每个作业使用 1 CPU、128 MB 内存、20 MB 临时磁盘、0 GPU，无需安装额外 Python 包。

## 1. 准备目录

在获准登录的提交节点上，进入含有本章的 `condor_userguide` 仓库根目录执行。以下步骤使用同一终端，路径不含空格或逗号。

```bash
PYTHON_BIN=/mnt/cephfs/hot-small/dsyan/anaconda3/bin/python
EXECUTE_MACHINE=hengshan  # 改为已获准计算、可访问共享环境的在线节点

PERSONAL_ROOT="/mnt/cephfs/$(id -un)"
mkdir -p "$PERSONAL_ROOT"
DEMO_ROOT=$(mktemp -d "$PERSONAL_ROOT/storage-demo.XXXXXX")
cp -R storage/examples/. "$DEMO_ROOT/"
chmod +x "$DEMO_ROOT/common/run.sh"
for mode in 01-transfer 02-shared-data 03-shared-only; do
  mkdir -p "$DEMO_ROOT/$mode/logs" "$DEMO_ROOT/$mode/results"
done
cd "$DEMO_ROOT"
printf '本次示例目录：%s\n' "$DEMO_ROOT"
```

账号须有共享目录的读写权限；无法创建目录时联系管理员。示例直接调用共享 Python，自己的项目若需要 Conda 激活，可参考 [Python 教程](../../Python/README.md)。

## 2. 提交作业

**例一：传输代码和小输入，结果回传。**

```bash
condor_submit 01-transfer/job.submit \
  "demo_root=$DEMO_ROOT" "python_executable=$PYTHON_BIN" "execute_machine=$EXECUTE_MACHINE"
```

**例二：只传输代码，直接读写共享数据。**

```bash
condor_submit 02-shared-data/job.submit \
  "demo_root=$DEMO_ROOT" "python_executable=$PYTHON_BIN" "execute_machine=$EXECUTE_MACHINE"
```

**例三：全部共享。** 先跑通前两例，再查询所选节点的文件系统域，将实际值填入 `EXECUTE_FS_DOMAIN`：

```bash
condor_status -constraint "Machine == \"$EXECUTE_MACHINE\"" -af Name FileSystemDomain
EXECUTE_FS_DOMAIN=hengshan  # 按查询结果修改

condor_submit 03-shared-only/job.submit \
  "demo_root=$DEMO_ROOT" "python_executable=$PYTHON_BIN" \
  "execute_machine=$EXECUTE_MACHINE" "execute_filesystem_domain=$EXECUTE_FS_DOMAIN"
```

以上命令中的参数用于展开提交模板；不能省略参数直接提交。记下每次提交返回的作业号，例如 `123.0`。

## 3. 查看结果

将下面的示例目录和作业号替换为本次实际值：

```bash
MODE=01-transfer
JOB_ID=123.0
condor_q "$JOB_ID"
condor_history "$JOB_ID" -af JobStatus ExitCode
cat "$DEMO_ROOT/$MODE/logs/job_$JOB_ID.out"
cat "$DEMO_ROOT/$MODE/logs/job_$JOB_ID.err"
```

结束后应看到退出码 `0`，并在下表对应的 `summary.json` 中看到 `"sum": 6`。仍在队列且状态为 Held 时，用 `condor_q "$JOB_ID" -af HoldReason` 查看原因。

| 示例 | 结果路径（相对于 `$DEMO_ROOT`） | 程序运行时的 `cwd` |
| --- | --- | --- |
| 一 | `01-transfer/result_<作业号>/summary.json` | 执行节点的 scratch |
| 二 | `02-shared-data/results/result_<作业号>/summary.json` | 执行节点的 scratch |
| 三 | `03-shared-only/results/result_<作业号>/summary.json` | 共享的 `03-shared-only` 目录 |

JSON 中的路径记录执行时的位置，回传后不会改写。重复练习时新建示例目录；作业结束后可保存所需结果，再清理本次 `DEMO_ROOT`。
