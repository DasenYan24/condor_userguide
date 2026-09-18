# 服务器资源清单

本页记录与 HTCondor 集群相关的服务器资源。数据依据 2026-07-20 资产清单整理，核心数为物理核心数。

公开范围仅包含主机名、业务 IP、机房位置、硬件配置、序列号、磁盘和业务挂载关系；不收录带外管理地址、账号、凭据、责任人或部门信息。

## HTCondor 纳管节点

| 服务器 / 业务 IP | 位置 | 状态 | 配置 | 型号 / SN |
| ---------------- | ---- | ---- | ---- | --------- |
| taishan / `192.168.62.221` | 6C209C，柜 17，12U-15U | 已纳管 | Intel Xeon Gold 6226R / 32C / 252 GiB / 10 × RTX 3090 | 安擎 EG841G-G20 / EG2021061600015 |
| huashan / `192.168.62.191` | 6C209C，柜 17，2U-5U | 已纳管 | Intel Xeon Gold 6226R / 32C / 252 GiB / 10 × RTX 3090 | 安擎 EG841G-G20 / EG2021061600013 |
| hengshan / `192.168.62.192` | 6C209C，柜 17，7U-10U | 已纳管 | Intel Xeon Gold 6226R / 32C / 252 GiB / 10 × RTX 3090 | 安擎 EG841G-G20 / EG2021061600014 |
| tianshuisong / `192.168.62.187` | 6C209C，柜 16，9U-12U | 已纳管，设备离线 | Intel Xeon Gold 5122 / 8C / 125 GiB / 4 × RTX 3090 | 戴尔 T630 / 5LMFG13 |
| shuitianxu / `192.168.62.188` | 6C209C，柜 16，14U-17U | 已纳管 | Intel Xeon Gold 5122 / 8C / 125 GiB / 4 × RTX 4090 | 戴尔 T630 / 5LNJG13 |
| ditiantai / `192.168.62.189` | 6C209C，柜 16，19U-22U | 已纳管 | AMD EPYC 7513 / 64C / 378 GiB / 3 × RTX 4090 | 赋创 FG4812T-A3 / 80102086T25C021245 |
| shanshuimeng / `192.168.62.190` | 6C209C，柜 16，24U-27U | 已纳管 | Intel Xeon Silver 4214 / 24C / 126 GiB / 4 × RTX 3090 | 容天工控机 / YL2023120000101 |

### 磁盘与挂载

| 服务器 | 磁盘 | 挂载关系 |
| ------ | ---- | -------- |
| taishan | `sda: 893.3G`；`sdb: 9.1T`；`sdc: 32.7T` | `ubuntu-vg/ubuntu-lv → /`；`sda2 → /boot`；`sdb1 → /mnt/lab`；`sdc → /mnt/lab1`；`fengtianxiaoxu:/mnt/lab → /mnt/net1` |
| huashan | `sda: 893.3G`；`sdb: 9.1T`；`sdc: 32.7T` | `ubuntu-vg/ubuntu-lv → /`；`sda2 → /boot`；`sdb → /mnt/lab`；`sdc → /mnt/lab1` |
| hengshan | `sda: 893.3G`；`sdb: 9.1T`；`sdc: 32.7T` | `ubuntu-vg/ubuntu-lv → /`；`sda2 → /boot`；`sdb → /mnt/lab`；`sdc → /mnt/lab1`；`fengtianxiaoxu:/mnt/lab → /mnt/net1` |
| tianshuisong | `sda: 894.3G`；`sdb: 1.8T`；`sdc: 1.8T` | 未核实（设备离线） |
| shuitianxu | `sda: 894.3G`；`sdb: 1.8T`；`sdc: 1.8T` | `ubuntu-vg/ubuntu-lv → /`；`sda2 → /boot`；`sda1 → /boot/efi`；`sdb1 → /mnt/lab`；`sdc1 → /mnt/lab1`；`fengtianxiaoxu:/mnt/lab → /mnt/net1` |
| ditiantai | `sda: 893.8G`；`sdb: 1.7T` | `sda2 → /`；`sda1 → /boot/efi`；`sdb1 → /mnt/lab`；`fengtianxiaoxu:/mnt/lab → /mnt/net1` |
| shanshuimeng | `sda: 223.6G`；`sdb: 1.7T` | `ubuntu-vg/ubuntu-lv → /`；`sda2 → /boot`；`sda1 → /boot/efi`；`sdb1 → /mnt/lab`；`fengtianxiaoxu:/mnt/lab → /mnt/net1` |

## 相关但未纳管的服务器

以下设备出现在同一资产清单中，但当前未纳入 HTCondor。不要将其写入作业的 `Requirements`，除非纳管状态已经变更并得到确认。

| 服务器 / 业务 IP | 位置 | 用途 | 配置 | 型号 / SN |
| ---------------- | ---- | ---- | ---- | --------- |
| shanfenggu / `192.168.62.181` | 6C209C，柜 15，2U-7U | GPU 服务器 | AMD EPYC 9J14 / 192C / 503 GiB / 8 × NVIDIA H200 NVL | 赋创 FG5824S-A4 / TBS0CG00011B |
| fengdiguan / `192.168.62.182` | 6C209C，柜 15，9U-12U | 存储服务器 | AMD EPYC 9J14 / 96C / 188 GiB / 无 GPU | FS4160A-A4 / W5S0MD00014F |
| huoleishihe / `192.168.62.183` | 6C209C，柜 15，14U-17U | 存储服务器 | AMD EPYC 9J14 / 96C / 188 GiB / 无 GPU | FS4160A-A4 / W5S0MD00000Z |
| shanhuobi / `192.168.62.184` | 6C209C，柜 15，19U-22U | 存储服务器 | AMD EPYC 9J14 / 96C / 188 GiB / 无 GPU | FS4160A-A4 / W5S0MD00000U |
| fengtianxiaoxu / `192.168.62.185` | 6C209C，柜 15，24U-25U | 边缘存储服务器 | Intel Xeon Silver 4314 / 32C / 62 GiB / 1 × RTX 4090 | 五舟 S627G4 / W99012406002226 |
| dizelin / `192.168.62.186` | 6C209C，柜 16，2U-7U | GPU 服务器 | AMD EPYC 9J14 / 192C / 503 GiB / 8 × NVIDIA H200 NVL | 赋创 FG5824S-A4 / TBS0CG00011K |
| tiandipi / `192.168.62.194` | 6C209C，柜 18，3U-8U | GPU 服务器 | AMD EPYC 9J14 / 192C / 62 GiB / 2 × RTX 5090 | 赋创 FG5824S-A4 / 210235K0SD6265V20035 |
| tianhuotongren / `192.168.62.195` | 6C209C，柜 18，10U-15U | GPU 服务器 | AMD EPYC 9J14 / 192C / 62 GiB / 2 × RTX 5090 | 赋创 FG5824S-A4 / 210235K0SD6265V20034 |
| huotiandayou / `192.168.62.196` | 6C209C，柜 19，3U-8U | GPU 服务器 | AMD EPYC 9J14 / 192C / 62 GiB / 2 × RTX 5090 | 赋创 FG5824S-A4 / 210235K0SD6265V2001T |
| dishanqian / `192.168.62.197` | 6C209C，柜 19，10U-15U | GPU 服务器 | AMD EPYC 9J14 / 192C / 62 GiB / 2 × RTX 5090 | 赋创 FG5824S-A4 / 210235K0SD6265V20033 |
| leidiyu / `192.168.62.198` | 6C209C，柜 20，3U-8U | GPU 服务器 | AMD EPYC 9J14 / 192C / 62 GiB / 2 × RTX 5090 | 赋创 FG5824S-A4 / 210235K0SD6265V2001V |
| zeleisui / `192.168.62.199` | 6C209C，柜 20，10U-15U | GPU 服务器 | AMD EPYC 9J14 / 192C / 62 GiB / 2 × RTX 5090 | 赋创 FG5824S-A4 / 210235K0SD6265V2001S |

### 磁盘与挂载

| 服务器 | 磁盘 | 挂载关系 |
| ------ | ---- | -------- |
| shanfenggu、dizelin | `sda: 894.3G`；`nvme0n1: 3.5T` | `sda2 → /`；`sda1 → /boot/efi`；`nvme0n1` 当前未挂载 |
| fengdiguan、huoleishihe、shanhuobi | `sda`-`sdj: 各 23.6T`；`sdk: 894.3G`；`sdl: 0B`；`nvme0n1: 3.5T` | `sdk2 → /`；`sdk1 → /boot/efi`；其余磁盘当前未挂载 |
| fengtianxiaoxu | `sda`-`sdl: 各 14.6T`；`nvme0n1: 894.3G` | `ubuntu-vg/ubuntu-lv → /`；`nvme0n1p2 → /boot`；`nvme0n1p1 → /boot/efi`；`vg_data/lv_data → /mnt/lab` |
| tiandipi、tianhuotongren、huotiandayou、dishanqian、leidiyu、zeleisui | `sda: 894.3G` | `sda2 → /`；`sda1 → /boot/efi` |

## 共享存储映射

集群提供 CephFS 和 NFS 两套共享存储，内容不会自动同步。CephFS 挂载范围依据 2026-09-17 运维验收记录补充；NFS 保留 2026-07-20 资产清单已确认的范围。

| 类型 | 存储来源 | 节点访问路径 | 已确认挂载的 HTCondor 节点 |
| --- | --- | --- | --- |
| CephFS | fengdiguan、huoleishihe、shanhuobi 共同提供的 CephFS `/shared` | `/mnt/cephfs` | taishan、huashan、hengshan、shuitianxu、ditiantai、shanshuimeng |
| NFS | fengtianxiaoxu（`192.168.62.185`）的 `/mnt/lab` | `/mnt/net1` | taishan、hengshan、shuitianxu、ditiantai、shanshuimeng |

此外，shanfenggu、dizelin、fengtianxiaoxu、tiandipi、tianhuotongren、huotiandayou、dishanqian、leidiyu、zeleisui 也已挂载 `/mnt/cephfs`，合计 15 台客户端。三台 CephFS 存储服务器未配置该客户端挂载；tianshuisong 尚未完成挂载确认。

`/mnt/cephfs` 用于新项目的数据、代码和结果，`hot-small` 子目录适合运行环境和常用小文件；`/mnt/net1` 存放原有的共享数据和环境。文件存放建议见[首页共享存储说明](../readme.md#共享存储)。

`/mnt/net0` 的来源未在本次资产清单中确认。确认新的存储源之前，不应继续使用旧文档中的地址。

## 未在本次清单中确认的旧记录

qianweitian、kunweidi、shuileizhun、shuidibi、dishuishi、tianzelu 未出现在本次资产清单中。旧 IP 可能已经复用，因此本项目不再发布这些旧地址；如需恢复为当前资源，应先补齐新的业务 IP、位置和纳管状态。
