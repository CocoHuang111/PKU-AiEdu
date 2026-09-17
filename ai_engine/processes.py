"""Isolate native inference allocations and keep cancellation responsive."""

from __future__ import annotations

import json
import selectors
import subprocess
import sys
import tempfile
import time


def run_json_worker(module: str, payload: dict, on_progress=None, timeout: float = 1800):
    """JSON-lines protocol; callbacks execute in the caller, never swallowed.

    Poll callbacks also check cancellation while a child is loading a model or
    doing native computation. Any exception terminates and reaps the child.
    """
    last_progress = None
    result = None
    deadline = time.monotonic() + timeout
    with tempfile.TemporaryFile(mode="w+b") as errors:
        process = subprocess.Popen(
            [sys.executable, "-u", "-m", module],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors,
            text=True, bufsize=1,
        )
        try:
            process.stdin.write(json.dumps(payload))
            process.stdin.close()
            with selectors.DefaultSelector() as selector:
                selector.register(process.stdout, selectors.EVENT_READ)
                while True:
                    if time.monotonic() > deadline:
                        raise TimeoutError(f"{module} 超过 {timeout:g} 秒，已停止子进程")
                    events = selector.select(timeout=1)
                    if not events:
                        if on_progress:
                            on_progress(last_progress)
                        continue
                    line = process.stdout.readline()
                    if not line:
                        break
                    try:
                        message = json.loads(line)
                    except ValueError:
                        continue
                    if message.get("type") == "progress":
                        last_progress = message["value"]
                        if on_progress:
                            on_progress(last_progress)
                    elif message.get("type") == "result":
                        result = message["value"]
            code = process.wait(timeout=max(1, deadline - time.monotonic()))
            if code != 0 or result is None:
                errors.seek(0, 2)
                errors.seek(max(0, errors.tell() - 4000))
                detail = errors.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"{module} 子进程退出（exit={code}）：{detail}")
            return result
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
            process.stdout.close()


def emit(kind: str, value) -> None:
    print(json.dumps({"type": kind, "value": value}, ensure_ascii=False, allow_nan=False), flush=True)
