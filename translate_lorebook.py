# -*- coding: utf-8 -*-
"""
translate_lorebook.py
=====================
로어북 영문 콘텐츠 -> 한국어 번역 파이프라인.

흐름:
  1) --export : 번역 대상 85개 엔트리(캐릭터·로어·이벤트) 원문 + 이름 매핑표를
                _ko_work/source.json 으로 추출. (번역 서브에이전트가 소비)
  2) (서브에이전트가 _ko_work/part_*.json = {idx: 한국어_content} 작성)
  3) --merge  : part_*.json 들을 lorebook_ko.json = {str(idx): content_ko} 로 병합.
  4) --status : 진행 상황(번역 완료/누락 인덱스) 점검.

번역 규칙은 tonemanner.md 를 따른다. 필드 라벨(`- Name:`)과 섹션 헤더(`#### ...`)는
영문 그대로 두고 값·산문만 한국어로 옮긴다.
"""
import json
import os
import sys
import glob
import argparse

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "_ko_work")
SOURCE = os.path.join(WORK, "source.json")
OUT = os.path.join(HERE, "lorebook_ko.json")


def content_indices(items):
    """폴더 아님 + content 있음 인 엔트리 인덱스."""
    idxs = []
    for i, e in enumerate(items):
        if e.get("mode") == "folder":
            continue
        if e.get("content"):
            idxs.append(i)
    return idxs


def export():
    import build_wiki as b
    items = b.load_items()
    ds = b.build_dataset()
    # 이름 매핑표: 영문명/스테이지 -> 한국어 정식명
    namemap = {}
    for c in ds["characters"]:
        kr = c["title"]
        if c.get("nameEn"):
            namemap[c["nameEn"]] = kr
        if c.get("stage"):
            namemap[c["stage"].split("(")[0].strip()] = kr
    entries = []
    for i in content_indices(items):
        e = items[i]
        entries.append({"idx": i, "comment": e.get("comment", ""),
                        "content": e.get("content", "")})
    os.makedirs(WORK, exist_ok=True)
    with open(SOURCE, "w", encoding="utf-8") as f:
        json.dump({"entries": entries, "namemap": namemap},
                  f, ensure_ascii=False, indent=1)
    print("export: %d entries -> %s" % (len(entries), SOURCE))
    # 배치 인덱스 안내
    idxs = [e["idx"] for e in entries]
    print("indices:", idxs)


import re


def tolerant_load(raw):
    """에이전트가 값 내부 큰따옴표를 이스케이프하지 않은 JSON 복구.
    구조: {"<digits>": "<value>", ...}. 키 패턴을 앵커로 값 구간을 잘라
    내부 bare-quote 를 이스케이프한 뒤 json 으로 디코드."""
    keys = list(re.finditer(r'"(\d+)"\s*:\s*"', raw))
    out = {}
    for i, m in enumerate(keys):
        idx = m.group(1)
        vstart = m.end()
        if i + 1 < len(keys):
            seg = raw[vstart:keys[i + 1].start()]
            seg = re.sub(r'"\s*,\s*$', "", seg)       # 끝의  ",  제거
        else:
            seg = raw[vstart:]
            seg = re.sub(r'"\s*}\s*$', "", seg)        # 끝의  "}  제거
        seg = re.sub(r'(?<!\\)"', r'\\"', seg)         # bare quote 이스케이프
        try:
            out[idx] = json.loads('"' + seg + '"')
        except Exception as e:
            print("  !! 복구 실패 idx", idx, e)
    return out


def merge():
    merged = {}
    parts = sorted(glob.glob(os.path.join(WORK, "part_*.json")))
    for p in parts:
        raw = open(p, encoding="utf-8").read()
        try:
            d = json.loads(raw)
        except json.JSONDecodeError:
            d = tolerant_load(raw)
            print("repaired:", os.path.basename(p), "->", len(d), "entries")
        for k, v in d.items():
            merged[str(k)] = v
    # 엔트리당 파일(e<idx>.txt)이 있으면 우선 적용 (정렬 버그 수정용)
    over = sorted(glob.glob(os.path.join(WORK, "e*.txt")))
    for p in over:
        base = os.path.basename(p)
        m = re.match(r"e(\d+)\.txt$", base)
        if not m:
            continue
        merged[m.group(1)] = open(p, encoding="utf-8").read().strip()
    if over:
        print("per-entry overrides:", len(over))
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=1)
    print("merge: %d parts -> %d entries -> %s" % (len(parts), len(merged), OUT))
    return merged


def status():
    """병합 결과 lorebook_ko.json 의 정렬을 원본과 대조."""
    import build_wiki as b
    items = b.load_items()
    if not os.path.exists(OUT):
        print("lorebook_ko.json 없음 — 먼저 --merge"); return
    ko = json.load(open(OUT, encoding="utf-8"))
    want = content_indices(items)
    missing = [i for i in want if str(i) not in ko]
    norm = lambda s: "".join((s or "").split())
    bad = []
    for i in want:
        e = items[i]; c = e.get("content") or ""
        if not b.is_character(c):
            continue
        koc = ko.get(str(i))
        if not koc:
            continue
        # 기대 이름 후보: 한글 정식명(comment/Korean Name Order) + 영문 Name
        cand = [b.get_field(c, "Korean Name Order"), e.get("comment", ""),
                b.get_field(c, "Name", "Formal Name", "Self-Name")]
        kon = (b.get_field(koc, "Korean Name Order") or b.get_field(koc, "Name")
               or b.get_field(koc, "Formal Name", "Self-Name") or "")
        ok = any(x and (norm(x) in norm(kon) or norm(kon) in norm(x)) for x in cand)
        if not ok:
            bad.append((i, e.get("comment"), kon[:16]))
    print("target=%d  translated=%d  missing=%d" % (len(want), len(ko), len(missing)))
    if missing:
        print("missing idx:", missing)
    print("misaligned=%d" % len(bad))
    for x in bad:
        print("  ", x)


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
