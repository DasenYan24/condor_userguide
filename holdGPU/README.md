# 在特定机器上占用 GPU 的 HTCondor 示例

> **适用范围与权限要求**
>
> 集群默认只向用户开放指定节点的 SSH 登录权限，不开放所有计算节点的 SSH 登录权限。能够通过 HTCondor 提交作业，并不代表可以通过 SSH 登录作业所在的机器。
>
> 本教程采用“先通过 HTCondor 占用 GPU，再通过 SSH 登录对应机器使用 GPU”的方式，因此**通常不适用于默认权限的普通用户**。如有裸机调试等特殊需求，请先联系管理员，申请开通所需计算节点的 SSH 登录权限，获批后再使用本教程。

本例的 `holdgpu.sh` 由 HTCondor 传到临时工作目录运行；SSH 登录后的目录和环境不会自动与该作业相同。提交前需将 `initialdir` 改为自己的提交端项目目录，并在其中创建 `logs/`。目录和日志传输规则见[共享存储、文件传输与作业目录](../storage/README.md)。

## 注意事项

1. 占用 GPU 会影响其他用户的作业调度，请合理使用
2. 测试完成后记得及时释放资源：`condor_rm <jobid>`

## 使用方法

### 1. 修改提交文件

修改 `holdgpu.submit` 文件中的 `Arguments = 300` 为需要占用的时间，单位为秒。

编辑 `holdgpu.submit` 文件，指定要运行的机器：

```
Requirements = (TARGET.Machine=="taishan")
```

可选的机器包括：

- taishan
- huashan  
- hengshan
- shanshuimeng
- shuitianxu
- tianshuisong
- ditiantai

### 2. 提交作业

```bash
condor_submit holdgpu.submit
```

### 3. 查看作业状态和 GPU 分配

```bash
# 查看作业实时输出，可以查看作业占用的 GPU 信息
condor_tail <jobid>

# 查看作业 log
condor_q -l <jobid> | grep Log
```

```bash
# 查看作业状态
condor_q

# 在 taishan 上查看整个 pool 的所有任务，适合排查在 huashan 等机器提交的作业
condor_q -global -allusers

# 查看作业详细信息，包括分配的 GPU
condor_q -l <jobid> | grep GPU

# 查看作业分配的 GPU ID
condor_q -l <jobid> | grep AssignedGPUs
```

### 4. 查看输出

作业运行后，可以在 logs 目录下查看：

- `job_*.out` - 标准输出，包含 GPU 信息
- `job_*.err` - 错误输出
- `job_*.log` - HTCondor 日志

## 工具脚本说明

### holdgpu.sh

占用 GPU 并显示 GPU 映射信息的脚本。在 HTCondor 作业中运行：

```bash
./holdgpu.sh [sleep_time]  # 默认占用 300 秒
```

功能：

- 显示作业运行的机器和时间
- 显示 CUDA_VISIBLE_DEVICES 环境变量
- 自动检测 GPU 分配格式（UUID 或数字索引）
- 通过 condor_status 查询机器的 GPU 列表
- 显示程序 GPU 索引到物理 GPU 索引的映射
- 显示机器的所有 GPU 并标记当前作业使用的 GPU
- 占用 GPU 指定时间

输出示例：

```
GPU 映射信息:
--------------
程序 GPU 0 → 物理 GPU 1 (UUID: GPU-ddc03d24)

huashan 的所有 GPU:
  [0] GPU-d5c56962
  [1] GPU-ddc03d24 <- 分配给当前作业
  [2] GPU-81455554
  ...
```
