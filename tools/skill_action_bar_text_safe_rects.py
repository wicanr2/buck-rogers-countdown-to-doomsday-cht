#!/usr/bin/env python3
"""驗證技能操作列 exact 事件、譯文與文字安全矩形。"""
from __future__ import annotations
import argparse, csv
from pathlib import Path

HEADER=["event_key","x","y","width","height","draw_x","draw_y","capacity_cells","line_count","overflow_policy"]

def read_rects(path: Path):
    with path.open(encoding="utf-8",newline="") as handle:
        reader=csv.DictReader(handle,delimiter="\t")
        if reader.fieldnames!=HEADER: raise ValueError("矩形欄位不符合固定 schema")
        return list(reader)

def validate(events: Path, translations: Path, rects: Path) -> int:
    with events.open(encoding="utf-8",newline="") as h: event_rows=list(csv.DictReader(h,delimiter="\t"))
    with translations.open(encoding="utf-8",newline="") as h: text_rows=list(csv.DictReader(h,delimiter="\t"))
    texts={r["key"]:r["translation"] for r in text_rows}; expected={}
    for event in event_rows:
        for variant in ("normal","focus"):
            key=f'{event["screen"]}.{event["key"]}.{variant}'
            expected[key]=(event["screen"],event["key"],int(event["x0"]),int(event["y0"]),int(event["x1"]),int(event["y1"]))
    data=read_rects(rects); found={r["event_key"]:r for r in data}
    if len(found)!=len(data) or set(found)!=set(expected): raise ValueError("矩形 key 重複、缺少或有孤兒")
    per_action={}
    for key,(screen,text_key,x0,y0,x1,y1) in expected.items():
        row=found[key]; nums={name:int(row[name]) for name in HEADER[1:9]}
        got=(nums["x"],nums["y"],nums["width"],nums["height"])
        if got!=(x0,y0,x1-x0,y1-y0): raise ValueError(f"{key}: exact 幾何漂移")
        if nums["draw_x"]!=x0 or nums["draw_y"]!=y0 or nums["capacity_cells"]!=(x1-x0)//8: raise ValueError(f"{key}: anchor 或容量漂移")
        if nums["line_count"]!=1 or row["overflow_policy"]!="single-line-reject": raise ValueError(f"{key}: 單列契約漂移")
        if text_key not in texts or len(texts[text_key])>nums["capacity_cells"]: raise ValueError(f"{key}: 譯文缺少或容量不足")
        base=key.rsplit(".",1)[0]; geom=got+(nums["draw_x"],nums["draw_y"],nums["capacity_cells"])
        if base in per_action and per_action[base]!=geom: raise ValueError(f"{base}: normal/focus 幾何不一致")
        per_action[base]=geom
    bases=list(per_action)
    for i,a in enumerate(bases):
        sa=expected[a+".normal"][0]; ax,ay,aw,ah,*_=per_action[a]
        for b in bases[i+1:]:
            if expected[b+".normal"][0]!=sa: continue
            bx,by,bw,bh,*_=per_action[b]
            if ax<bx+bw and bx<ax+aw and ay<by+bh and by<ay+ah: raise ValueError(f"{a}/{b}: 跨 action 重疊")
    return len(data)

def main():
    p=argparse.ArgumentParser(); p.add_argument("events",type=Path); p.add_argument("translations",type=Path); p.add_argument("rects",type=Path); a=p.parse_args()
    print(f"validated {validate(a.events,a.translations,a.rects)} skill action-bar rectangles")
if __name__=="__main__": main()
