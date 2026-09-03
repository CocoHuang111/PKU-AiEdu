"""不依赖 openpyxl，用 zip+XML 读打分表第一张 sheet。"""

from __future__ import annotations

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def _colrow(cell_ref: str) -> tuple[int, int]:
    col, row = "", ""
    for c in cell_ref:
        if c.isalpha():
            col += c
        else:
            row += c
    n = 0
    for c in col:
        n = n * 26 + (ord(c) - 64)
    return n, int(row)


def _shared_strings(z: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    out = []
    for si in root.findall("m:si", NS):
        texts = [t.text or "" for t in si.findall(".//m:t", NS)]
        out.append("".join(texts))
    return out


def read_sheet_rows(
    path: str | Path, *, keep_blank_names: bool = False
) -> list[dict[str, str]]:
    """返回第一张表：表头为键的 dict 列表。单元格一律转成 str。

    inventory 默认忽略没有姓名的续行。专家规则长表需要保留这类行，再按原表
    顺序向下填充姓名，因此通过 ``keep_blank_names`` 显式开启，避免改变旧流程。
    """
    path = Path(path)
    with zipfile.ZipFile(path) as z:
        ss = _shared_strings(z)
        sheet_name = "xl/worksheets/sheet1.xml"
        if sheet_name not in z.namelist():
            raise FileNotFoundError(f"{path} 没有 sheet1")
        sheet = ET.fromstring(z.read(sheet_name))
        grid: dict[int, dict[int, str]] = {}
        for c in sheet.findall(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c"):
            ref = c.attrib.get("r")
            if not ref:
                continue
            col, row = _colrow(ref)
            t = c.attrib.get("t")
            v = c.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v")
            is_el = c.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}is")
            if t == "inlineStr" and is_el is not None:
                val = "".join(t.text or "" for t in is_el.findall(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"))
            elif t == "s" and v is not None and v.text is not None:
                val = ss[int(v.text)]
            elif v is not None and v.text is not None:
                val = v.text
            else:
                val = ""
            grid.setdefault(row, {})[col] = val

    if not grid:
        return []
    header_row = min(grid)
    for r in sorted(grid):
        vals = [str(v).strip() for v in grid[r].values()]
        if "姓名" in vals:
            header_row = r
            break
    headers = grid[header_row]
    max_col = max(headers)
    names = [headers.get(i, f"col{i}").strip() or f"col{i}" for i in range(1, max_col + 1)]
    records = []
    for r in sorted(grid):
        if r == header_row:
            continue
        cells = grid[r]
        rec = {names[i - 1]: str(cells.get(i, "")).strip() for i in range(1, len(names) + 1)}
        name = (rec.get("姓名") or "").strip()
        if name in {"姓名", "序号"} or (not keep_blank_names and not name):
            continue
        if any(rec.values()):
            records.append(rec)
    return records
