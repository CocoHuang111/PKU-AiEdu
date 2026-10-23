"""Check explicitly configured OSS with a unique temporary object, never user data.

Run on ECS: python -m scripts.check_oss_storage
Creates and deletes only _checks/<random UUID>.bin. No DB or evaluation models.
"""
from __future__ import annotations

import io
import json
import sys
import tempfile
import time
import uuid
from dataclasses import replace
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from backend.app.core.oss_storage import OSSConfig, OSSStorageBackend, OSSStorageError


def check():
    config = OSSConfig.from_env()
    key = "_checks/" + uuid.uuid4().hex + ".bin"
    payload = b"askedu-oss-storage-check\n" * 1024
    write_attempted = False
    began = time.monotonic()
    stage = "初始化缓存"
    # Record the harmless test key in case a failed deletion needs follow-up.
    print(json.dumps({"bucket": config.bucket, "region": config.region,
                      "role": config.role_name, "test_key": key}, ensure_ascii=False), flush=True)
    with tempfile.TemporaryDirectory(prefix="askedu-oss-check-") as tmp:
        storage = OSSStorageBackend(replace(config, cache_root=Path(tmp)))
        try:
            stage = "上传"
            write_attempted = True
            size = storage.save(key, io.BytesIO(payload))
            assert size == len(payload)
            stage = "读取缓存"
            path = storage.path_for(key)
            assert path.read_bytes() == payload
            storage.evict_cache(key)
            assert not path.exists()
            assert storage.path_for(key).read_bytes() == payload
            stage = "检查匿名访问"
            # Public unsigned GET must not expose this private teaching-data bucket.
            unsigned = f"https://{config.bucket}.oss-{config.region}.aliyuncs.com/{key}"
            try:
                with urlopen(unsigned, timeout=15) as response:
                    raise OSSStorageError(f"Bucket 匿名下载未被阻止（HTTP {response.status}），请检查私有权限")
            except HTTPError as error:
                if error.code != 403:
                    raise OSSStorageError(f"无法确认 Bucket 私有权限（HTTP {error.code}）") from None
            signed = storage.signed_download_url(key, 60)
            stage = "检查签名下载"
            try:
                with urlopen(signed, timeout=15) as response:
                    assert response.read(len(payload) + 1) == payload
            except (HTTPError, URLError):
                raise OSSStorageError("短期签名下载验证失败") from None
            print(json.dumps({"bytes": size, "internal": config.internal,
                              "read_write_cache": "passed", "unsigned_public_get": 403,
                              "signed_public_get": "passed",
                              "seconds": round(time.monotonic() - began, 2)}, ensure_ascii=False), flush=True)
        except Exception as error:
            # Only a fixed stage and exception type, never SDK details or signed URLs.
            print(f"失败环节：{stage}；异常类型：{type(error).__name__}", flush=True)
            if isinstance(error, OSSStorageError):
                print(str(error), flush=True)
            raise
        finally:
            if write_attempted:
                failed = sys.exc_info()[0] is not None
                try:
                    storage.delete(key)
                    print("本次 OSS 测试对象和本地缓存已清理；未操作用户文件。", flush=True)
                except OSSStorageError as error:
                    print("测试对象清理未确认：" + str(error), flush=True)
                    if not failed:
                        raise


if __name__ == "__main__":
    try:
        check()
    except OSSStorageError as error:
        raise SystemExit(str(error) + "。测试对象如未清理，请按上方唯一 test_key 处理。") from None
    except (ValueError, OSError, AssertionError):
        # Avoid propagating SDK exception details or signed URLs into logs.
        raise SystemExit("OSS 验证失败；请检查角色权限、网络、Bucket 设置或配置。测试对象如未清理，请按上方唯一 test_key 处理。") from None
