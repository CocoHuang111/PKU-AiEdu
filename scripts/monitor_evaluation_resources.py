"""Read-only host-side Docker/process sampling for a particular evaluation.

Requires root access to /proc and the Docker daemon. Does not restart jobs.
RSS samples are explicitly samples, not an exact combined-process high-water mark.
"""

import argparse
import json
import subprocess
import time
import uuid
from pathlib import Path


def command(*args):
    return subprocess.check_output(args, text=True, timeout=15).strip()


def sample(container):
    config = json.loads(command("docker", "inspect", container))[0]
    pid = config["State"]["Pid"]
    if not pid:
        return {"running": False, "restarts": config["RestartCount"]}
    groups = Path(f"/proc/{pid}/cgroup").read_text().splitlines()
    relative = next(line.split(":", 2)[2] for line in groups if line.startswith("0::"))
    root = Path("/sys/fs/cgroup") / relative.lstrip("/")
    stat = dict(line.split() for line in (root / "memory.stat").read_text().splitlines())
    processes = []
    for value in (root / "cgroup.procs").read_text().split():
        try:
            fields = dict(line.split(":", 1) for line in Path(f"/proc/{value}/status").read_text().splitlines() if ":" in line)
            processes.append({"pid": int(value), "rss_bytes": int(fields.get("VmRSS", "0 kB").split()[0]) * 1024,
                              "peak_rss_bytes": int(fields.get("VmHWM", "0 kB").split()[0]) * 1024})
        except (FileNotFoundError, ProcessLookupError):
            continue
    return {"running": True, "restarts": config["RestartCount"],
            "anon_bytes": int(stat["anon"]), "rss_bytes": sum(p["rss_bytes"] for p in processes),
            "processes": processes}


def main(task_id, output):
    task_id = str(uuid.UUID(task_id))
    output.mkdir(parents=True, exist_ok=True)
    started = time.time()
    maximum = 0
    with (output / "resources.jsonl").open("a", encoding="utf-8") as stream:
        while True:
            state = command("docker", "exec", "pku2-postgres-1", "psql", "-U", "pku2", "-d", "pku2", "-At", "-c",
                            f"SELECT status,progress,current_step FROM eval_tasks WHERE id='{task_id}';")
            if not state:
                raise RuntimeError("Task no longer exists; stopped sampling")
            status, progress, step = state.split("|")
            resource = sample("pku2-worker-1")
            maximum = max(maximum, resource.get("rss_bytes", 0))
            value = {"time": time.time(), "task_id": task_id, "status": status,
                     "progress": int(progress), "step": step, **resource}
            stream.write(json.dumps(value) + "\n")
            stream.flush()
            print(json.dumps(value), flush=True)
            if status in ("completed", "cancelled", "failed"):
                summary = {"task_id": task_id, "status": status, "sampled_peak_rss_bytes": maximum,
                           "sample_interval_sec": 5, "sampling_started_at": started,
                           "sampling_ended_at": time.time(), "restarts": resource["restarts"]}
                (output / "resources-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
                return
            time.sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("task_id")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    main(args.task_id, args.output)
