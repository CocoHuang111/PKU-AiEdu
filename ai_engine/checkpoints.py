"""Small, atomic checkpoints bound to a particular input file and configuration."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path


def identity(path: str | Path, options: dict) -> str:
    source = Path(path).resolve()
    stat = source.stat()
    value = [str(source), stat.st_size, stat.st_mtime_ns, options]
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def read(path: Path, signature: str):
    try:
        pack = json.loads(path.read_text(encoding="utf-8"))
        return pack["value"] if pack["signature"] == signature else None
    except (OSError, ValueError, KeyError, TypeError):
        return None


def write(path: Path, signature: str, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump({"signature": signature, "value": value}, stream, ensure_ascii=False, allow_nan=False)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)
