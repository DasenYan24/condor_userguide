# 在 HTCondor 集群中运行 C/CUDA 程序

本目录包含在 HTCondor 集群中运行 C/CUDA 程序的示例和说明。

本例启用文件传输：可执行程序送到执行节点的临时工作目录运行，`initialdir` 指定提交端项目目录。提交前需在该目录创建 `logs/`；程序自己的结果文件与标准输出是不同的文件。路径解释、结果回传和共享数据用法见[共享存储、文件传输与作业目录](../storage/README.md)。

## 目录结构

- `test.cu` - CUDA 示例程序
- `Makefile` - 编译配置文件
- `job.submit` - HTCondor 作业提交文件

## 使用步骤

### 1. 准备程序

首先需要准备您的 C/CUDA 程序。示例程序 `test.cu` 展示了一个简单的 GPU 睡眠程序。

### 2. 编译程序

使用提供的 Makefile 编译程序：

```bash
make
```

这将生成可执行文件 `x.run`。

### 3. 创建提交文件

修改 `job.submit` 文件中的以下参数：

- `initialdir` - 修改为您的项目路径
- `request_GPUs` - 设置所需的 GPU 数量
- `requestMemory` - 设置所需的内存大小（MB）
- `Arguments` - 设置传递给程序的参数

### 4. 提交作业

```bash
csub job.submit
```

或

```bash
condor_submit job.submit
```

### 5. 监控作业

查看作业状态：

```bash
cq
```

查看作业详细信息：

```bash
cq -l <jobid>
```

## 注意事项

### GPU 使用规范

1. **测试阶段**：在 taishan 上测试时，必须使用 GPU 6、7、8 或 9：

   ```cuda
   cudaSetDevice(6);  // 或 7、8、9
   ```

2. **提交作业时**：必须将 GPU 设置改为 0，让 HTCondor 自动分配：

   ```cuda
   cudaSetDevice(0);
   ```

### 短作业优化

如果您的程序运行时间少于 30 分钟，可以在 `job.submit` 中启用短作业标志：

```
+SHORT_JOB=true
```

这样可以同时使用短作业集群和长作业集群的资源。

### 指定运行节点

如果需要在特定节点运行，可以在 `job.submit` 中设置：

```
Requirements = (TARGET.Machine=="taishan") || (TARGET.Machine=="huashan")
```

### CUDA 能力要求

如果程序需要特定的 CUDA 计算能力：

```
Requirements = CUDACapability > 6.0
```

## 故障排查

如果作业无法运行，使用以下命令分析原因：

```bash
cq -better-analyze <jobid>
```

查看运行日志：

- 标准输出：`logs/job_<ClusterId>.<ProcId>.out`
- 错误输出：`logs/job_<ClusterId>.<ProcId>.err`
- HTCondor 日志：`logs/job_<ClusterId>.log`
