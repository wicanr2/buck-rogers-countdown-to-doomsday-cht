#!/usr/bin/env python3
"""驗證第四頁 READY glyph identity 與繁中候選。"""
from __future__ import annotations
import csv, hashlib, re, sys, unicodedata
from pathlib import Path

from halfwidth import half_units  # 規格 039 §3.4：準確半形單位（U+0020–U+007E、U+2022 為 1，其餘 2）

EVENT_HEADER = ["event_key","sequence","original_length","original_sha256","caller","glyph_guard","background","foreground","row","column","entry_step","post_call_step","evidence_level","catalog_status"]
TRANSLATION_HEADER = ["key","translation","source"]
EXPECTED = [
 ("story.page4.line.001",34,"70dcbd264497c53d685f4261bf3bff0b8e4a3110b43b918105be9753048d95bf",17,301110011,302556029),
 ("story.page4.line.002",37,"b2005b94a3d6fb0fe926ff3c77bbb2f6d2c6a43169affb4cd10ee6b2641b6247",18,302599801,304177273),
 ("story.page4.line.003",33,"41248df16995d7ec129c735e250e4cbae84411a7b9da14bc67efe0594293cda7",19,304221261,305623148),
 ("story.page4.line.004",31,"35b59e99604cbd7264ad1218ae3ad20760dfc7a0d21ca04afaadeebe87a00eda",20,305667022,306981257),
 ("story.page4.line.005",33,"c83d64d5bcfeae8f41fc4fc899637fa45af2826b62d33e9ee9042331e91b561b",21,307025461,308427356),
 ("story.page4.line.006",24,"ab0a680e1bd4ba6ed62ac7438633c6559b22412508953561e0034d7440b65066",22,308471572,309478931),
]

def rows(path, header):
    raw=path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw: raise ValueError(f"{path}: BOM/CR")
    raw.decode("utf-8")
    with path.open(encoding="utf-8", newline="") as f:
        r=csv.DictReader(f, delimiter="\t")
        if r.fieldnames != header: raise ValueError(f"{path}: header")
        out=list(r)
    if any(None in x or any(v is None for v in x.values()) for x in out): raise ValueError(f"{path}: columns")
    return out


def validate(events_path: Path, translations_path: Path):
    ev=rows(events_path, EVENT_HEADER); tr=rows(translations_path, TRANSLATION_HEADER)
    if len(ev)!=len(EXPECTED) or len(tr)!=len(EXPECTED): raise ValueError("第四頁 DRAFT 必須恰有六筆")
    for i,(row, want) in enumerate(zip(ev, EXPECTED),1):
        key,length,digest,logical_row,entry,post=want
        if (row["event_key"],int(row["sequence"]),int(row["original_length"]),row["original_sha256"],int(row["row"]),int(row["entry_step"]),int(row["post_call_step"])) != (key,i,length,digest,logical_row,entry,post): raise ValueError(f"identity: {key}")
        if not re.fullmatch(r"[0-9a-f]{64}", digest): raise ValueError(f"hash: {key}")
        if (row["caller"],row["glyph_guard"],row["background"],row["foreground"],row["column"],row["evidence_level"],row["catalog_status"]) != ("0763:04FF","0763:026B","0","10","1","confirmed","READY"): raise ValueError(f"READY metadata: {key}")
    keys=[x["event_key"] for x in ev]
    if [x["key"] for x in tr] != keys: raise ValueError("translation coverage")
    for x in tr:
        if not x["translation"] or x["source"] != "runtime-editorial" or x["translation"] != unicodedata.normalize("NFC",x["translation"]): raise ValueError(f"translation: {x['key']}")
        if half_units(x["translation"]) > 78: raise ValueError(f"capacity: {x['key']}")

if __name__ == "__main__":
    if len(sys.argv)!=3: raise SystemExit("usage: story_page4_catalog.py EVENTS TRANSLATIONS")
    validate(Path(sys.argv[1]),Path(sys.argv[2])); print("story page4 READY OK")
