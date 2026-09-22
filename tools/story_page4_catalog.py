#!/usr/bin/env python3
"""驗證第四頁 screenshot-derived DRAFT identity 與繁中候選。"""
from __future__ import annotations
import csv, hashlib, re, sys, unicodedata
from pathlib import Path

EVENT_HEADER = ["event_key","sequence","original_length","original_sha256","caller","glyph_guard","background","foreground","row","column","entry_step","post_call_step","evidence_level","catalog_status"]
TRANSLATION_HEADER = ["key","translation","source"]
EXPECTED = [
 ("story.page4.line.001",33,"faea4e715864605d192788c6331c6335b3a9bccc91fba21e72069a5336d64f12",17),
 ("story.page4.line.002",38,"59206579c9802e1d04cea0730e6fafcf81da28d9df31bc898c9a0cb11b61db56",18),
 ("story.page4.line.003",33,"9c8b8840aa76634ac107888c33017f57910b06e999d3199cb92810b8939759ea",19),
 ("story.page4.line.004",24,"58cbe528d3e70d3188fbd9033e2cf6f40ecbdadb4491e193b1a7c8539ae771f7",20),
 ("story.page4.line.005",35,"8e49dbd6d876f3772995c070f80036e0651d265abd9299cf12d07bd0af5d5ce0",21),
 ("story.page4.line.006",24,"ab0a680e1bd4ba6ed62ac7438633c6559b22412508953561e0034d7440b65066",22),
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

def cells(s):
    return sum(2 if unicodedata.east_asian_width(c) in {"W","F"} else 1 for c in s)

def validate(events_path: Path, translations_path: Path):
    ev=rows(events_path, EVENT_HEADER); tr=rows(translations_path, TRANSLATION_HEADER)
    if len(ev)!=len(EXPECTED) or len(tr)!=len(EXPECTED): raise ValueError("第四頁 DRAFT 必須恰有六筆")
    for i,(row, want) in enumerate(zip(ev, EXPECTED),1):
        key,length,digest,logical_row=want
        if (row["event_key"],int(row["sequence"]),int(row["original_length"]),row["original_sha256"],int(row["row"])) != (key,i,length,digest,logical_row): raise ValueError(f"identity: {key}")
        if not re.fullmatch(r"[0-9a-f]{64}", digest): raise ValueError(f"hash: {key}")
        if (row["caller"],row["glyph_guard"],row["background"],row["foreground"],row["column"],row["entry_step"],row["post_call_step"],row["evidence_level"],row["catalog_status"]) != ("unknown","unknown","0","10","1","0","0","visual-transcription","DRAFT"): raise ValueError(f"DRAFT metadata: {key}")
    keys=[x["event_key"] for x in ev]
    if [x["key"] for x in tr] != keys: raise ValueError("translation coverage")
    for x in tr:
        if not x["translation"] or x["source"] != "runtime-editorial" or x["translation"] != unicodedata.normalize("NFC",x["translation"]): raise ValueError(f"translation: {x['key']}")
        if cells(x["translation"]) > 39: raise ValueError(f"capacity: {x['key']}")

if __name__ == "__main__":
    if len(sys.argv)!=3: raise SystemExit("usage: story_page4_catalog.py EVENTS TRANSLATIONS")
    validate(Path(sys.argv[1]),Path(sys.argv[2])); print("story page4 DRAFT OK")
