# -*- coding: utf-8 -*-
"""
classify_relations.py
=====================
캐릭터 간 방향성 관계를 원작자 의도에 맞는 유형으로 분류(LLM 패스)한다.

  1) --export : 방향성 관계(영문 원문 + src/tgt)를 _rel_work/edges.json 으로 추출.
  2) (서브에이전트가 _rel_work/cls_*.json = {"<srcId>|<tgtId>": "<type>"} 작성)
  3) --merge  : 합쳐 relation_types.json 생성.

유형(키, 영문): childhood, friend, rival, caretaker, mentor, family, enemy, love, colleague, former
"""
import os
import sys
import json
import glob
import argparse

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "_rel_work")
EDGES = os.path.join(WORK, "edges.json")
OUT = os.path.join(HERE, "relation_types.json")

TYPES = ["childhood", "friend", "rival", "caretaker", "mentor",
         "family", "enemy", "love", "colleague", "former"]


def export():
    import build_wiki as b
    ds = b.build_dataset()
    byid = {c["id"]: c for c in ds["characters"]}
    rels = []
    for c in ds["characters"]:
        for r in c.get("relationships", []):
            tid = r.get("targetId")
            if not tid or tid not in byid or tid == c["id"]:
                continue
            rels.append({
                "key": "%s|%s" % (c["id"], tid),
                "src": c["title"], "tgt": byid[tid]["title"],
                "text": (r.get("text") or "")[:400],
            })
    os.makedirs(WORK, exist_ok=True)
    with open(EDGES, "w", encoding="utf-8") as f:
        json.dump(rels, f, ensure_ascii=False, indent=1)
    print("export: %d directed relations -> %s" % (len(rels), EDGES))


def merge():
    out = {}
    for p in sorted(glob.glob(os.path.join(WORK, "cls_*.json"))):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            print("  skip", os.path.basename(p), e); continue
        for k, v in d.items():
            if v in TYPES:
                out[k] = v
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("merge: %d classified -> %s" % (len(out), OUT))


def status():
    if not os.path.exists(EDGES):
        print("edges.json 없음 — 먼저 --export"); return
    edges = json.load(open(EDGES, encoding="utf-8"))
    have = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    miss = [e["key"] for e in edges if e["key"] not in have]
    print("relations=%d classified=%d missing=%d" % (len(edges), len(have), len(miss)))
    import collections
    print("dist:", dict(collections.Counter(have.values())))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", action="store_true")
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    if a.export:
        export()
    if a.merge:
        merge()
    if a.status:
        status()
    if not (a.export or a.merge or a.status):
        ap.print_help()
