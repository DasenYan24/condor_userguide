"""用标准库计算 1 + 2 + 3，并记录代码、输入和结果真正所在的位置。"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("transfer", "shared-data", "shared-only"), required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pause-seconds", type=int, default=0)
    args = parser.parse_args()
    if not 0 <= args.pause_seconds <= 60:
        parser.error("--pause-seconds 必须在 0 到 60 之间")

    source = args.input.resolve(strict=True)
    numbers = [int(line) for line in source.read_text().splitlines() if line.strip()]
    # 每个作业使用独立结果目录；已有目录不覆盖，重跑练习请新建实验目录。
    destination = args.output.resolve()
    destination.mkdir(parents=True, exist_ok=False)
    result = {
        "mode": args.mode,
        "hostname": socket.gethostname(),
        "uid": os.getuid(),
        "groups": os.getgroups(),
        "cwd": str(Path.cwd()),
        "script_path": str(Path(__file__).resolve()),
        "python_executable": sys.executable,
        "python_prefix": sys.prefix,
        "scratch_dir": os.environ.get("_CONDOR_SCRATCH_DIR"),
        "input_path": str(source),
        "input_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "output_path": str(destination / "summary.json"),
        "count": len(numbers),
        "sum": sum(numbers),
        "pause_seconds": args.pause_seconds,
    }
    # 先完成临时文件，再改名发布结果，读者不会读到半份 JSON。
    temporary = destination / "summary.json.tmp"
    with temporary.open("x") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(destination / "summary.json")
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    if args.pause_seconds:
        print(f"结果已经写出，暂停 {args.pause_seconds} 秒以便观察回传时机。", flush=True)
        time.sleep(args.pause_seconds)
    print("计算完成；应同时检查 Condor 退出码和 summary.json 中的 sum=6。", flush=True)


if __name__ == "__main__":
    main()
