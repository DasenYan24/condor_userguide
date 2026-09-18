# 共享存储、文件传输与作业目录

**推荐用法：传输代码，共享环境和大数据，结果直接保存到共享目录。** 两者可以同时使用，无需为了访问共享数据而关闭文件传输。

## 1. 先分清三种目录

| 目录 | 用途 |
| --- | --- |
| 提交目录 | 保存原始代码、提交文件、日志和回传结果 |
| 执行节点的临时目录（scratch） | 启用文件传输后，程序默认在这里运行代码副本 |
| 共享目录 | 多台节点直接访问同一份环境、数据或结果，如 `/mnt/cephfs/...` |

提交目录也可以放在共享存储上；即使代码已经共享，`should_transfer_files = YES` 仍会传输指定文件的副本。共享路径需要在目标执行节点挂载，且作业账号有访问权限，见[挂载范围](../servers/README.md#共享存储映射)。

## 2. 路径怎么写

以下按 `should_transfer_files = YES`、启动脚本没有执行 `cd` 的情况说明：

| 参数或写法 | 含义 |
| --- | --- |
| `initialdir` | 提交端输入、日志和回传结果的路径基准，**不是程序在执行节点的工作目录** |
| 相对路径的 `executable` | 相对于运行 `condor_submit` 时的目录，不随 `initialdir` 改变；建议写绝对路径 |
| `transfer_input_files` | 需要复制的代码和输入；其中相对路径按 `initialdir` 解释 |
| 程序中的相对路径 | 相对于当前工作目录，通常就是 scratch |
| 程序中的 `/mnt/cephfs/...` | 直接读写共享文件，不经过 HTCondor 复制 |
| `output`、`error`、`log` | 标准输出、标准错误和作业事件日志；不代表程序生成的全部结果 |

例如，传输 `data/input.txt` 后，默认在 scratch 中用 `input.txt` 读取。HTCondor 默认传输 `executable`，其他代码和输入需要列入 `transfer_input_files`，不会自动复制整个项目或 Python 环境。

[Python 教程](../Python/README.md)采用的就是这种方式：传输 `run.sh` 和 `test.py`，在执行节点加载共享的 `/mnt/cephfs/hot-small/dsyan/anaconda3` 环境。激活 Conda 不会改变工作目录。

## 3. 结果保存在哪里、何时可见

- **写入 scratch 的结果**：用 `transfer_output_files` 明确指定回传文件或目录；设置 `when_to_transfer_output = ON_EXIT` 后，程序自行退出时回传到提交端的 `initialdir`。不要假定所有子目录都会自动回传。
- **直接写入共享目录的结果**：写完并刷新后即可从共享路径读取，无需等待回传。可见不代表作业已经完成。
- **标准输出和错误**：本教程的 `YES` 示例默认在退出后回传；运行中可用 `condor_tail <作业号>` 查看。事件日志由提交端持续记录。
- **异常结束**：`ON_EXIT` 不保证被抢占或被删除的作业能保存临时结果；重要检查点建议直接写入共享目录。回传清单中的文件不存在会导致作业 Held。

多个作业应使用各自的结果目录，例如 `result_$(ClusterId).$(ProcId)`，避免覆盖。

## 4. 三种用法

| 示例 | 代码与输入 | 结果 | 传输设置 |
| --- | --- | --- | --- |
| [一：共享环境＋传输代码和小输入](examples/01-transfer/job.submit) | 代码、小输入复制到 scratch；Python 环境共享 | 退出后回传 | `YES` |
| [二：传输代码＋直接访问共享数据](examples/02-shared-data/job.submit)（推荐） | 只复制代码；环境、数据通过共享绝对路径访问 | 直接写共享目录 | `YES` |
| [三：全部共享](examples/03-shared-only/job.submit) | 代码、环境和数据都在共享目录 | 直接写共享目录 | `NO` |

例一明确设置 `transfer_output_files = result_$(ClusterId).$(ProcId)`；例二设置 `transfer_output_files = ""`，不再收集 scratch 结果，但仍回传标准输出和错误。

例三关闭传输后，程序从共享的 `initialdir` 启动。所有路径必须在执行节点可用，还需按目标节点公布的 `FileSystemDomain` 填写模板参数；这个属性不等于实际挂载检查。

**按步骤运行：[三个示例的准备、提交与结果查看](examples/README.md)。** 均为小型 CPU 求和任务，不占用 GPU。其他传输选项见 [HTCondor 官方文档](https://htcondor.readthedocs.io/en/24.x/users-manual/file-transfer.html)。
