# -*- coding: utf-8 -*-
"""
build_play.py — 인터랙티브 플레이 플랫폼 빌드 (단일 HTML, 클라이언트 단독)
======================================================================
worldstate.md 설계를 실제로 굴리는 플레이 앱을 만든다.
  - build_wiki 의 캐논 파서/데이터(캐릭터·관계·이미지·고유 지팡이·복장)를 재사용
  - worldstate.md §8 시드 파이프라인으로 초기 WorldState 생성
  - 저작 자산(modules/flags/bands) 로드 + 복장/무기 모듈 자동 파생
  - play_template.page() 로 단일 HTML(lorebook-play.html) 생성

런타임은 클라이언트 단독(BYO 키) — 브라우저가 LLM API를 직접 호출한다.

사용:
  python build_play.py            # lorebook-play.html 생성
  python build_play.py --report   # 시드/모듈 통계만 출력
"""
import os
import re
import sys
import json
import argparse

sys.stdout.reconfigure(encoding="utf-8")

# 무기 유형 키워드 (긴 단어/특수형 우선 → '대검'이 '검'보다 먼저)
WEAPON_TYPES = [
    "카타나", "레이피어", "하나후다", "커틀러스", "지팡이", "단검", "대검", "고헤이",
    "쿠나이", "권총", "글러브", "완드", "랜턴", "바이올린", "팔레트", "주사기", "컨트롤러",
    "태블릿", "부적", "천칭", "부채", "발톱", "채찍", "주걱", "오브", "구슬", "반지",
    "활", "창", "봉", "붓", "펜", "검", "창",
]


def weapon_label(staff):
    """고유 지팡이 산문 → '이름(원어) - 유형' 형태의 간결한 아이템 라벨.
    예: "'적월(Red moon)'이라 불리는 붉은 카타나" → "적월(Red moon) - 카타나".
    고유명 없으면 짧은 명사구 그대로(끝 마침표 제거)."""
    if not staff:
        return staff
    s = staff.strip().rstrip(" .。")
    m = re.search(r"['‘’\"「『]([^'‘’\"」』]+)['‘’\"」』]", s)
    typ = next((t for t in WEAPON_TYPES if t in s), None)
    if m and typ:
        return "%s - %s" % (m.group(1).strip(), typ)
    if m:
        return m.group(1).strip()
    return s

import build_wiki
import play_template

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_HTML = os.path.join(HERE, "lorebook-play.html")

# 16개 지구 + 시고쿠 (홋카이도는 단일 통합)
DISTRICTS = [
    "Tokyo", "Osaka", "Kyoto", "Northern Kyushu", "Southern Kyushu",
    "Eastern Chugoku", "Western Chugoku", "Northern Kinki", "Southern Kinki",
    "Eastern Chubu", "Western Chubu", "Eastern Kanto", "Western Kanto",
    "Northern Tohoku", "Southern Tohoku", "Hokkaido", "Shikoku",
]


def load_json(name, default):
    p = os.path.join(HERE, name)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return default


def derive_modules(canon):
    """캐논에서 복장(default/magical)·무기(고유 지팡이) 모듈을 자동 파생."""
    mods = []
    for c in canon["characters"]:
        cid = c["id"]
        im = canon["images"].get(c.get("imgPrefix") or "", {})
        if im.get("d"):
            mods.append({
                "id": "outfit-%s-casual" % cid, "type": "outfit", "slot": "outfit",
                "title": "평상복", "ownedBy": cid, "imgKind": "d",
                "requires": [], "conflictsWith": ["outfit-%s-magical" % cid],
                "effects": {"narrative": [
                    "%s은(는) 평상복 차림이다. 일상적인 분위기로, 능력 노출을 자제한다." % c["title"]],
                    "state": [], "unlocks": []},
            })
        if im.get("m"):
            mods.append({
                "id": "outfit-%s-magical" % cid, "type": "outfit", "slot": "outfit",
                "title": "변신 의상", "ownedBy": cid, "imgKind": "m",
                "requires": [], "conflictsWith": ["outfit-%s-casual" % cid],
                "effects": {"narrative": [
                    "%s은(는) 변신한 상태다. 전투 능력 사용이 허용되며, 평소보다 결연한 태도를 보인다." % c["title"]],
                    "state": [], "unlocks": []},
            })
        if c.get("staff"):
            staff = c["staff"]
            mods.append({
                "id": "weapon-%s-staff" % cid, "type": "equipment", "slot": "weapon",
                "title": weapon_label(staff), "ownedBy": cid,
                "requires": [],
                "effects": {"narrative": [
                    "%s은(는) 고유 마법 지팡이 「%s」을(를) 들고 있다." % (c["title"], staff)],
                    "state": [], "unlocks": []},
            })
    return mods


def seed_world(canon, flag_catalog):
    """캐논에서 초기 WorldState 생성 (worldstate.md §8)."""
    rep_by_district = {}
    for c in canon["characters"]:
        d = c.get("districtNorm")
        if d and c.get("faction") == "rep" and d not in rep_by_district:
            rep_by_district[d] = c["id"]
    territory = {}
    for d in DISTRICTS:
        territory[d] = {
            "controller": rep_by_district.get(d),
            "stability": 0 if d == "Shikoku" else 80,
            "sealed": d == "Shikoku",
        }
    flags = {}
    for f in flag_catalog.get("flags", []):
        flags[f["key"]] = f.get("default")
    return {
        "meta": {"saveId": None, "schema": "worldstate/1", "turn": 0,
                 "ngPlusCount": 0, "protagonist": None, "companions": []},
        "flags": flags,
        "territory": territory,
        "affinity": {},
        "inventory": {"owned": [], "equipped": {"outfit": None, "weapon": None, "accessory": None}},
        "modules": {"equipped": [], "unlocked": []},
        "memory": [],
        "log": [],
    }


def build(report_only=False):
    ds = build_wiki.build_dataset()
    canon = build_wiki.build_js_data(ds)

    bands = load_json("affinity_bands.json", {})
    flag_catalog = load_json("flag_catalog.json", {})
    authored = load_json("modules.json", [])
    derived = derive_modules(canon)
    modules = derived + authored
    world = seed_world(canon, flag_catalog)

    assets = {
        "bands": bands.get("bands", []),
        "axes": bands.get("axes", []),
        "seedByRelType": bands.get("seedByRelType", {}),
        "flags": flag_catalog.get("flags", []),
        "issue": flag_catalog.get("issue", []),
        "modules": modules,
        "districts": [{"key": d, "kr": build_wiki.DISTRICT_KR.get(d, d)} for d in DISTRICTS],
    }

    seeded = sum(1 for t in world["territory"].values() if t["controller"])
    print("=" * 56)
    print("플레이 빌드 시드 통계")
    print("=" * 56)
    print("캐릭터:", len(canon["characters"]), "| 게스트:", len(canon["guests"]))
    print("모듈: %d (복장/무기 파생 %d + 저작 %d)" % (len(modules), len(derived), len(authored)))
    print("플래그:", len(assets["flags"]), "| 밴드:", len(assets["bands"]))
    print("지구:", len(DISTRICTS), "| 지역대표 통제 지구:", seeded)
    if report_only:
        return

    canon_json = json.dumps(canon, ensure_ascii=False, separators=(",", ":"))
    world_json = json.dumps(world, ensure_ascii=False, separators=(",", ":"))
    assets_json = json.dumps(assets, ensure_ascii=False, separators=(",", ":"))

    # ----- 위키 임베드(iframe srcdoc): 같은 ds로 위키 HTML 생성, 이미지는 부모 공유로 중복 제거 -----
    import wiki_template
    mappos_json = json.dumps(build_wiki.MAP_POS, ensure_ascii=False)
    try:
        import geo_japan
        mapgeo = geo_japan.build_map()
        if mapgeo:
            mapgeo["kr"] = dict(build_wiki.DISTRICT_KR, Hokkaido="홋카이도")
    except Exception as e:
        print("!! 지도 생성 실패, 폴백 사용:", e)
        mapgeo = None
    mapgeo_json = json.dumps(mapgeo, ensure_ascii=False, separators=(",", ":"))
    wiki_data = dict(canon, images={})  # 이미지는 부모(CANON)에서 가져옴 → 중복 제거
    wiki_data_json = json.dumps(wiki_data, ensure_ascii=False, separators=(",", ":"))
    wiki_html = wiki_template.page(wiki_data_json, mappos_json, mapgeo_json,
                                   extra_css=play_template.WIKI_THEME_CSS)
    wikidoc_json = json.dumps(wiki_html, ensure_ascii=False)
    print("위키 임베드: %.2f MB (이미지 부모 공유)" % (len(wiki_html) / 1024 / 1024))

    html = play_template.page(canon_json, world_json, assets_json, wikidoc_json)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print("\n생성 완료: %s  (%.1f MB)" % (OUT_HTML, os.path.getsize(OUT_HTML) / 1024 / 1024))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    build(report_only=args.report)
