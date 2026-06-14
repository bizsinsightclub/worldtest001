# -*- coding: utf-8 -*-
"""
battles.py — 전투 사례 머지
===========================
`_battle_work/scene_*.md` (헤더 + 본문) 를 파싱해 참여자 이름을 캐릭터 id로 해석,
`battle_scenes.json` = [{id,title,type,participants:[{name,id}],blurb,scene}] 생성.

scene 파일 형식:
  TITLE: ...
  TYPE: ...
  PARTICIPANTS: 이름, 이름
  BLURB: ...
  ---
  (본문)
"""
import os
import sys
import glob
import json
import re

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "_battle_work")
OUT = os.path.join(HERE, "battle_scenes.json")


def parse_scene(path):
    raw = open(path, encoding="utf-8").read().replace("\r", "")
    if "---" not in raw:
        return None
    head, body = raw.split("---", 1)
    meta = {}
    for line in head.splitlines():
        m = re.match(r"^([A-Z]+)\s*:\s*(.+)$", line.strip())
        if m:
            meta[m.group(1).upper()] = m.group(2).strip()
    return {
        "title": meta.get("TITLE", os.path.basename(path)),
        "type": meta.get("TYPE", ""),
        "participants_raw": meta.get("PARTICIPANTS", ""),
        "blurb": meta.get("BLURB", ""),
        "scene": body.strip(),
    }


def merge():
    import build_wiki as b
    ds = b.build_dataset()
    by_title = {c["title"]: c for c in ds["characters"]}

    scenes = []
    for p in sorted(glob.glob(os.path.join(WORK, "scene_*.md"))):
        s = parse_scene(p)
        if not s:
            continue
        n = re.search(r"scene_(\d+)", os.path.basename(p)).group(1)
        parts = []
        for nm in [x.strip() for x in s["participants_raw"].split(",") if x.strip()]:
            base = re.sub(r"\s*[(（].*", "", nm).strip()  # '이름(스테이지)' -> '이름'
            c = by_title.get(nm) or by_title.get(base)
            parts.append({"name": base if c else nm,
                          "id": c["id"] if c else None,
                          "img": c.get("imgPrefix") if c else None})
        scenes.append({
            "id": "battle-%s" % n, "title": s["title"], "type": s["type"],
            "participants": parts, "blurb": s["blurb"], "scene": s["scene"],
            "chars": len(s["scene"].replace(" ", "").replace("\n", "")),
        })
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(scenes, f, ensure_ascii=False, indent=1)
    print("merge: %d scenes -> %s" % (len(scenes), OUT))
    for s in scenes:
        unres = [p["name"] for p in s["participants"] if not p["id"]]
        print("  %-10s %-22s chars=%d  참여=%s%s" % (
            s["id"], s["type"], s["chars"],
            ",".join(p["name"] for p in s["participants"]),
            ("  미해결:" + ",".join(unres)) if unres else ""))


if __name__ == "__main__":
    merge()
