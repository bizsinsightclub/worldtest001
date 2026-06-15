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

# 로어 요약(네짜 주입용) — 캐논 한국어를 결정적으로 추출. LLM·외부 의존 0, tonemanner 무관(원문 verbatim).
_LORE_SENT_END = re.compile(r"(?<=[다요죠음함])\.|(?<=[다요죠음함])\s*$|[。.](?=\s|$)")


def lore_summary(raw, limit=300):
    """로어 raw → 선두 문단 추출 요약(~limit자). 마크다운 헤딩/이미지/불릿 마커 정리,
    문장 경계에서 컷. 인물 dossier가 아닌 *로어 문서*만 대상 → 캐릭터 보이스 무관."""
    if not raw:
        return ""
    txt = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", raw)        # 이미지 md 제거
    lines = []
    for ln in txt.replace("\r", "").split("\n"):
        s = ln.strip()
        if not s:
            if lines and lines[-1] != "":
                lines.append("")
            continue
        s = re.sub(r"^#{1,6}\s*", "", s)                  # 헤딩 마커
        s = re.sub(r"^[-*•]\s*", "", s)                   # 불릿 마커
        s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)          # 굵게
        lines.append(s)
    body = " ".join(x for x in lines if x).strip()
    body = re.sub(r"\s{2,}", " ", body)
    if len(body) <= limit:
        return body
    cut = body[:limit]
    # 마지막 문장 종결("…다." 등) 또는 마침표에서 자른다
    m = list(re.finditer(r"[.。](?:\s|$)", cut))
    if m and m[-1].end() >= limit * 0.5:
        return cut[: m[-1].end()].strip()
    return cut.rstrip() + "…"


# 코어 로어(항상 주입·캐시 블록) 후보 — 마법소녀 '체계' 문서 우선.
_CORE_TITLE_PRIMARY = ("마법소녀",)
_CORE_TITLE_EXCLUDE = ("청", "목록", "공방", "가련", "사무소", "거부회")


def pick_core_lore(lore_pages):
    """세계 규칙의 근간이 되는 로어 1개 선정(없으면 None)."""
    cands = []
    for p in lore_pages:
        t = (p.get("title") or "")
        if any(k in t for k in _CORE_TITLE_PRIMARY) and not any(x in t for x in _CORE_TITLE_EXCLUDE):
            cands.append(p)
    if not cands:
        # 폴백: '마법소녀'를 키/제목에 포함하는 첫 문서
        for p in lore_pages:
            blob = (p.get("title") or "") + " " + " ".join(p.get("keys") or [])
            if "마법소녀" in blob:
                cands.append(p)
                break
    return cands[0]["id"] if cands else None


def annotate_lore(canon):
    """canon.lore[*]에 summary 부여 + canon.coreLoreId 선정 (play 전용, 원본 불변)."""
    for p in canon.get("lore", []):
        p["summary"] = lore_summary(p.get("raw", ""))
    canon["coreLoreId"] = pick_core_lore(canon.get("lore", []))
    return canon

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


def _has_batchim(w):
    """마지막 글자에 받침이 있는지(한글 음절이 아니면 False)."""
    if not w:
        return False
    code = ord(w[-1])
    if code < 0xAC00 or code > 0xD7A3:
        return False
    return (code - 0xAC00) % 28 != 0


def josa(w, batchim, plain):
    """한글 조사 자동 선택 — 받침 있으면 batchim, 없으면 plain. '김민석(이)가' 방지."""
    return (w or "") + (batchim if _has_batchim(w) else plain)


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
                    josa(c["title"], "은", "는") + " 평상복 차림이다. 일상적인 분위기로, 능력 노출을 자제한다."],
                    "state": [], "unlocks": []},
            })
        if im.get("m"):
            mods.append({
                "id": "outfit-%s-magical" % cid, "type": "outfit", "slot": "outfit",
                "title": "변신 의상", "ownedBy": cid, "imgKind": "m",
                "requires": [], "conflictsWith": ["outfit-%s-casual" % cid],
                "effects": {"narrative": [
                    josa(c["title"], "은", "는") + " 변신한 상태다. 전투 능력 사용이 허용되며, 평소보다 결연한 태도를 보인다."],
                    "state": [], "unlocks": []},
            })
        if c.get("staff"):
            staff = c["staff"]
            mods.append({
                "id": "weapon-%s-staff" % cid, "type": "equipment", "slot": "weapon",
                "title": weapon_label(staff), "ownedBy": cid,
                "requires": [],
                "effects": {"narrative": [
                    josa(c["title"], "은", "는") + " 고유 마법 지팡이 「" + staff + "」" + josa(staff, "을", "를") + " 들고 있다."],
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
    annotate_lore(canon)   # 로어 요약 + 코어 로어 선정 (네짜 주입용)

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
    _core = canon.get("coreLoreId")
    _coret = next((p.get("title") for p in canon.get("lore", []) if p.get("id") == _core), None)
    print("로어:", len(canon.get("lore", [])), "| 코어 로어:", _coret or "(없음)")
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
