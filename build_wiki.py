# -*- coding: utf-8 -*-
"""
build_wiki.py
=============
인터랙티브 판타지 소설(마법소녀 세계관) 로어북 -> 단일 HTML 위키/시각화 툴 생성기.

입력:
  - lorebook_export.json            (RisuAI 로어북 export)
  - collected_chars/*.webp          (캐릭터 기본/변신 이미지, 114장)

출력:
  - lorebook-wiki.html              (데이터 + 이미지 base64 + JS/CSS 인라인, 오프라인 자가완결)

사용:
  python build_wiki.py            # HTML 생성
  python build_wiki.py --report   # 파싱 통계만 출력 (HTML 미생성)
"""
import json
import re
import os
import sys
import base64
import argparse

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
LOREBOOK = os.path.join(HERE, "lorebook_export.json")
IMG_DIR = r"C:\Users\User\Documents\카카오톡 받은 파일\collected_chars"
OUT_HTML = os.path.join(HERE, "lorebook-wiki.html")

# ---------------------------------------------------------------------------
# 1. 로드 & 폴더 그룹핑
# ---------------------------------------------------------------------------

def load_items():
    with open(LOREBOOK, encoding="utf-8") as f:
        data = json.load(f)
    return data["data"]


def clean_key(k):
    # RisuAI 폴더 키에는  프리픽스가 붙는다
    return (k or "").replace("", "")


# ---------------------------------------------------------------------------
# 2. 필드/섹션 파서  (반정형 마크다운)
# ---------------------------------------------------------------------------

def get_field(content, *names):
    """'- Field: value' 또는 '* Field: value' 형태에서 값을 추출. 여러 후보명 지원."""
    for name in names:
        m = re.search(
            r"^\s*[-*]?\s*" + re.escape(name) + r"\s*:\s*(.+?)\s*$",
            content, re.M | re.I,
        )
        if m and m.group(1).strip():
            return m.group(1).strip()
    return None


def get_sections(content):
    """#### 또는 ### 헤더로 구분된 섹션들을 {title: body} 로 추출."""
    sections = {}
    # 헤더 위치 수집
    matches = list(re.finditer(r"^#{2,4}\s*(.+?)\s*$", content, re.M))
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        body = content[start:end].strip()
        if body:
            sections[title] = body
    return sections


SECTION_ALIASES = {
    "Personality Details": ["Personality Details"],
    "Public Image": ["Public Image"],
    "Combat Style": ["Combat Style", "Combat style", "Combat Characteristics"],
    "Relationships": ["Relationships", "Relationship", "Relationship Notes"],
    "Speech": ["Speech style and example", "Speech Style and Example",
               "Speech style and Example", "Speech Style"],
    "Awakening": ["Awakening", "Background and Awakening", "Background"],
    "Roleplaying Notes": ["Roleplaying Notes", "Roleplaying Role"],
    "Core Concept": ["Core Concept", "Overview"],
    "Weaknesses": ["Weaknesses and Limits", "Weaknesses"],
}


def pick_section(sections, key):
    for alias in SECTION_ALIASES.get(key, [key]):
        for title, body in sections.items():
            if title.lower() == alias.lower():
                return body
    return None


# ---------------------------------------------------------------------------
# 3. NPC List (master index) 파서 -> tagline 사전
# ---------------------------------------------------------------------------

def parse_npc_list(content):
    """'* Full Name / Stage: description' -> {full_name_lower: tagline}"""
    taglines = {}
    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("*"):
            continue
        line = line[1:].strip()
        # 'Name / Stage: desc' 또는 'Name: desc'
        m = re.match(r"^(.+?):\s*(.+)$", line)
        if not m:
            continue
        left, desc = m.group(1).strip(), m.group(2).strip()
        name = left.split("/")[0].strip()
        taglines[name.lower()] = {"name": name, "tagline": desc,
                                  "full_left": left}
    return taglines


# ---------------------------------------------------------------------------
# 4. 이미지 매핑
# ---------------------------------------------------------------------------

def scan_images():
    """{prefix: {'default': path, 'magical': path}}"""
    out = {}
    if not os.path.isdir(IMG_DIR):
        print("!! 이미지 폴더 없음:", IMG_DIR)
        return out
    for fn in os.listdir(IMG_DIR):
        if not fn.lower().endswith(".webp"):
            continue
        path = os.path.join(IMG_DIR, fn)
        if fn.endswith("_magical girl default.webp"):
            prefix = fn[: -len("_magical girl default.webp")]
            out.setdefault(prefix, {})["magical"] = path
        elif fn.endswith("_default.webp"):
            prefix = fn[: -len("_default.webp")]
            out.setdefault(prefix, {})["default"] = path
    return out


def match_image(name_en, images):
    """영문 이름의 토큰 중 이미지 prefix와 일치하는 것을 찾는다."""
    if not name_en:
        return None
    tokens = re.split(r"[\s/\-]+", name_en)
    # 정확 토큰 매칭
    for t in tokens:
        if t in images:
            return t
    # 하이픈/특수문자 제거 후 재시도 (Shuten-dōji 등)
    for t in tokens:
        for pfx in images:
            if pfx.lower() == t.lower():
                return pfx
    return None


def b64_uri(path):
    with open(path, "rb") as f:
        b = f.read()
    return "data:image/webp;base64," + base64.b64encode(b).decode("ascii")


# ---------------------------------------------------------------------------
# 5. 진영(faction) 분류
# ---------------------------------------------------------------------------

VILLAIN_NAMES = {  # 괴이/빌런 (개별 프로필)
    "Yamata no Orochi", "Shuten-dōji", "The Administrator", "Phantom",
    "Tamamo", "Tamamo-no-Mae", "Yeo Bongseon", "Kel'Thuzad", "Wushang", "Mizuchi",
}
SHIKOKU_NAMES = {"Taneda Hikari", "Tsugumi Kodaka", "Watanabe Shion", "Hino Chieri"}
REFUSAL_NAMES = {"Yorimitsu Ayame", "Renshu Matsuri", "Kino Tsubame",
                 "Minase Chihiro", "Igarashi Ichie"}

FACTION_LABEL = {
    "rep": "지역 대표",
    "bureau": "마법소녀청·협력",
    "trainee": "연습생",
    "shikoku": "시고쿠 (타마모)",
    "refusal": "졸업거부회",
    "villain": "괴이·빌런",
    "guest": "게스트",
    "other": "기타",
}


def classify_faction(name_en, folder, tagline):
    t = (tagline or "").lower()
    if name_en in VILLAIN_NAMES:
        return "villain"
    if name_en in SHIKOKU_NAMES:
        return "shikoku"
    if name_en in REFUSAL_NAMES:
        return "refusal"
    if "graduation refusal" in t:
        return "refusal"
    if "shikoku" in t or "tamamo" in t:
        return "shikoku"
    if folder and "지역 대표" in folder:
        return "rep"
    if "rep." in t:
        return "rep"
    if folder and "협력업체" in folder:
        return "bureau"
    if "bureau" in t or "workshop" in t or "mgb president" in t or "secretary" in t:
        return "bureau"
    if "trainee" in t or (folder and "연습생" in folder):
        return "trainee"
    return "other"


# ---------------------------------------------------------------------------
# 6. 캐릭터 / 로어 / 이벤트 빌드
# ---------------------------------------------------------------------------

def is_character(content):
    return bool(
        get_field(content, "Name", "Formal Name", "Self-Name")
        and get_field(content, "Rank", "Threat Class", "Former Rank",
                      "Current Status", "Role", "Species")
    )


def build_dataset(report_only=False):
    items = load_items()
    images = scan_images()
    npc_taglines = parse_npc_list(items[1].get("content", ""))
    ko = load_korean()
    # 한국어 NPC 인덱스(엔트리 1)에서 한국어 태그라인 (한글 정식명 -> tagline)
    ko_taglines = parse_npc_list(ko.get("1", "")) if ko else {}

    # 폴더 위치 -> 각 엔트리의 folder 이름 결정
    current_folder = None
    folder_of = {}
    for i, e in enumerate(items):
        if e.get("mode") == "folder":
            current_folder = e.get("comment")
            folder_of[i] = None
        else:
            folder_of[i] = current_folder

    characters = []
    lore_pages = []
    events = []

    used_prefixes = set()

    for i, e in enumerate(items):
        if e.get("mode") == "folder":
            continue
        content = e.get("content") or ""
        if not content:
            continue
        comment = e.get("comment", "")
        folder = folder_of.get(i)
        keys = clean_key(e.get("key", ""))

        if is_character(content):
            name_en = get_field(content, "Name", "Formal Name", "Self-Name") or comment
            stage = get_field(content, "Stage Name", "Former Stage Name", "Self-Name")
            tag = npc_taglines.get(name_en.lower(), {})
            faction = classify_faction(name_en, folder, tag.get("tagline"))
            sections = get_sections(content)

            pfx = match_image(name_en, images)
            if pfx:
                used_prefixes.add(pfx)
            imgset = images.get(pfx, {}) if pfx else {}

            # 관계 추출
            rel_body = pick_section(sections, "Relationships")
            relationships = parse_relationships(rel_body)

            rank_field = get_field(content, "Rank", "Former Rank")
            threat = get_field(content, "Threat Class")
            rank_label, stars, rank_kind = derive_rank(
                rank_field, tag.get("tagline"), threat)
            district = normalize_district(
                get_field(content, "Assigned District", "Current Territory"),
                tag.get("tagline"))

            char = {
                "id": "char-%d" % i,
                "title": comment,
                "nameEn": name_en,
                "rankLabel": rank_label,
                "stars": stars,
                "rankKind": rank_kind,
                "districtNorm": district,
                "nameJp": get_field(content, "Japanese Name"),
                "hiragana": get_field(content, "Hiragana"),
                "stage": stage,
                "rank": get_field(content, "Rank", "Former Rank", "Threat Class"),
                "age": get_field(content, "Age"),
                "office": get_field(content, "Management Office"),
                "generation": get_field(content, "Generation"),
                "district": get_field(content, "Assigned District",
                                      "Current Territory", "Former Position"),
                "species": get_field(content, "Species", "Type"),
                "height": get_field(content, "Height"),
                "staff": get_field(content, "Unique Magical Staff Form",
                                   "Unique magical staff form"),
                "personality": get_field(content, "Personality"),
                "role": get_field(content, "Role"),
                "status": get_field(content, "Current Status"),
                "tagline": tag.get("tagline"),
                "faction": faction,
                "factionLabel": FACTION_LABEL[faction],
                "sections": sections,
                "relationships": relationships,
                "rel_ko": [],
                "raw": content,
                "imgPrefix": pfx,
                "_imgset": imgset,  # 경로 (HTML 단계에서 base64)
            }

            # --- 한국어 표시값 오버레이 ---
            ko_content = ko.get(str(i))
            if ko_content:
                char["raw"] = ko_content  # 모달은 한국어 본문
                ko_sec = get_sections(ko_content)
                char["office"] = strip_redundant_label(
                    get_field(ko_content, "Management Office")) or char["office"]
                char["staff"] = strip_redundant_label(get_field(
                    ko_content, "Unique Magical Staff Form",
                    "Unique magical staff form")) or char["staff"]
                char["personality"] = get_field(ko_content, "Personality") \
                    or char["personality"]
                char["role"] = get_field(ko_content, "Role") or char["role"]
                char["rel_ko"] = parse_relationships(
                    pick_section(ko_sec, "Relationships"))
            # 열거형/지구 한국어화 (영문 값 기준 매핑)
            char["generation"] = gen_kr(char["generation"])
            char["species"] = species_kr(char["species"])
            char["rankLabel"] = rank_kr(char["rankLabel"])
            char["districtKr"] = DISTRICT_KR.get(district, district)
            # 한국어 태그라인 우선
            kt = ko_taglines.get(comment.lower(), {})
            if kt.get("tagline"):
                char["tagline"] = kt["tagline"]

            characters.append(char)
        elif folder == "고정 이벤트":
            events.append({
                "id": "event-%d" % i, "title": comment,
                "keys": keys, "raw": ko.get(str(i)) or content,
                "month": guess_month(keys, comment),
            })
        else:
            lore_pages.append({
                "id": "lore-%d" % i, "title": comment,
                "folder": folder, "keys": keys,
                "raw": ko.get(str(i)) or content,
            })

    # 매칭 안 된 이미지 -> 게스트 카드
    guests = []
    for pfx, imgset in images.items():
        if pfx in used_prefixes:
            continue
        guests.append({
            "id": "guest-%s" % re.sub(r"[^A-Za-z0-9]", "", pfx),
            "title": pfx, "nameEn": pfx, "faction": "guest",
            "factionLabel": FACTION_LABEL["guest"], "_imgset": imgset,
            "imgPrefix": pfx, "guest": True,
        })

    edges = resolve_edges(characters)

    return {
        "characters": characters,
        "guests": guests,
        "lore": lore_pages,
        "events": events,
        "images": images,
        "used_prefixes": used_prefixes,
        "edges": edges,
    }


def parse_relationships(body):
    if not body:
        return []
    rels = []
    for line in body.splitlines():
        line = line.strip()
        m = re.match(r"^[-*]\s*([^:]+?):\s*(.+)$", line)
        if m:
            target = m.group(1).strip()
            text = m.group(2).strip()
            rels.append({"target": target, "text": text})
    return rels


# --- 랭크 -> 별점 / 라벨 -------------------------------------------------

def derive_rank(rank, tagline, threat):
    """표시용 랭크 라벨과 별 개수(1~6) 산출."""
    src = " ".join(x for x in [rank, threat, tagline] if x)
    s = src.lower()
    # 괴이 위협등급
    if "arch" in s and "enemy" in s:
        return "아치 에너미", 6, "villain"
    if "main villain" in s:
        return "메인 빌런", 5, "villain"
    if "scene stealer" in s:
        return "씬 스틸러", 3, "villain"
    if re.search(r"\bextra\b", s):
        return "엑스트라", 1, "villain"
    # 마법소녀 등급
    if "special grade" in s:
        return "Special Grade", 6, "mg"
    m = re.search(r"grade\s*([1-9])", s)
    if m:
        g = int(m.group(1))
        stars = max(1, 6 - (g + 1) // 2)  # G1->5, G2->5, G3->4 ... G9->1
        stars = {1: 5, 2: 5, 3: 4, 4: 4, 5: 3, 6: 3, 7: 2, 8: 2, 9: 1}[g]
        return "Grade %d" % g, stars, "mg"
    return (rank or "—"), 2, "mg"


# --- 지구 정규화 ----------------------------------------------------------

DISTRICTS = [
    "Tokyo", "Osaka", "Kyoto", "Northern Kyushu", "Southern Kyushu",
    "Eastern Chugoku", "Western Chugoku", "Northern Kinki", "Southern Kinki",
    "Eastern Chubu", "Western Chubu", "Eastern Kanto", "Western Kanto",
    "Northern Tohoku", "Southern Tohoku", "Northern Hokkaido", "Southern Hokkaido",
    "Shikoku",
]


def normalize_district(field, tagline):
    src = " ".join(x for x in [field, tagline] if x) or ""
    s = src.lower().replace("kansai", "kinki")
    for d in DISTRICTS:
        if d.lower() in s:
            return d
    if "shikoku" in s:
        return "Shikoku"
    return None


DISTRICT_KR = {
    "Tokyo": "도쿄", "Osaka": "오사카", "Kyoto": "교토",
    "Northern Kyushu": "규슈 북부", "Southern Kyushu": "규슈 남부",
    "Eastern Chugoku": "주고쿠 동부", "Western Chugoku": "주고쿠 서부",
    "Northern Kinki": "긴키 북부", "Southern Kinki": "긴키 남부",
    "Eastern Chubu": "주부 동부", "Western Chubu": "주부 서부",
    "Eastern Kanto": "간토 동부", "Western Kanto": "간토 서부",
    "Northern Tohoku": "도호쿠 북부", "Southern Tohoku": "도호쿠 남부",
    "Northern Hokkaido": "홋카이도 북부", "Southern Hokkaido": "홋카이도 남부",
    "Shikoku": "시고쿠",
}


# --- 한국어 표시값 변환 -----------------------------------------------------

def gen_kr(v):
    if not v:
        return v
    m = re.search(r"(\d)(?:st|nd|rd|th)?\s*gen", v.lower())
    if m:
        return m.group(1) + "세대"
    return {"first generation": "1세대", "second generation": "2세대",
            "third generation": "3세대"}.get(v.lower().strip(), v)


def species_kr(v):
    if not v:
        return v
    s = v.lower()
    if "folklore" in s:
        return "민담류 괴이"
    if "urban legend" in s:
        return "도시전설류 괴이"
    if "anti-type" in s or "anti type" in s:
        return "안티류 괴이"
    if "media" in s:
        return "대중매체류 괴이"
    if "arch-enemy" in s or "arch enemy" in s:
        return "아치 에너미 (괴이)"
    if s.startswith("anomaly"):
        return "괴이"
    if "not ainu" in s:
        return "인간 (아이누 아님)"
    if "human" in s:
        return "인간"
    return v


def rank_kr(label):
    if not label:
        return label
    if label.lower() == "special grade":
        return "특급"
    m = re.match(r"grade\s*(\d)", label.lower())
    if m:
        return m.group(1) + "급"
    return label  # 괴이 등급(아치 에너미 등)·기타는 그대로


def strip_redundant_label(v):
    """KO 값 앞에 라벨이 중복된 경우 제거: '종족: 인간' -> '인간'."""
    if not v:
        return v
    m = re.match(r"^\s*[가-힣A-Za-z][가-힣A-Za-z ]{0,7}:\s*(\S.*)$", v)
    return m.group(1) if m else v


def load_korean():
    path = os.path.join(HERE, "lorebook_ko.json")
    if not os.path.exists(path):
        print("!! lorebook_ko.json 없음 — 영문으로 출력 (번역 파이프라인 먼저 실행)")
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# 관계 유형 분류 (영문 원문 키워드)
REL_TYPES = [
    ("family", ["family", "sister", "mother", "daughter", "sibling", "twin",
                "tamamo’s", "tamamo's", "adopted", "blood-related"]),
    ("mentor", ["trainee under", "mentor", "teaches", "instructor", "student",
                "master", "disciple", "coordinator", "looks after", "raised"]),
    ("rival", ["rival"]),
    ("former", ["former friend", "used to", "once ", "no longer", "ex-"]),
    ("enemy", ["enemy", "hates", "despises", "insane", "obstacle", "kill",
               "hostile", "distrust", "betray", "target", "revenge"]),
    ("love", ["in love", "crush", "romantic", "adore", "beloved", "lover"]),
    ("friend", ["friend", "childhood", "close ", "trust"]),
]


def classify_rel(text):
    s = (text or "").lower()
    for t, kws in REL_TYPES:
        if any(k in s for k in kws):
            return t
    return "colleague"


EN_MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11,
    "december": 12,
}


def guess_month(keys, title):
    """월은 keys/제목에서만 추정 (본문의 'may' 등 오탐 방지)."""
    hay = keys + " " + title
    low = hay.lower()
    # 'N월' (자릿수 경계로 11월이 1월로 오인되지 않게)
    m = re.search(r"(?<!\d)(\d{1,2})\s*월", hay)
    if m:
        return int(m.group(1))
    # 'N/D' 날짜 (5/1, 12/31)
    m = re.search(r"(?<!\d)(\d{1,2})/\d{1,2}", hay)
    if m:
        return int(m.group(1))
    # 영문 월 이름 (단어 경계)
    for name, v in EN_MONTHS.items():
        if re.search(r"\b" + name + r"\b", low):
            return v
    # 계절·명절 fallback
    if "golden week" in low or "골든 위크" in low:
        return 5
    if "halloween" in low or "할로윈" in low:
        return 10
    if "autumn" in low or "가을" in low:
        return 11
    if "summer" in low or "하계" in low:
        return 7
    return None


# ---------------------------------------------------------------------------
# 7. 리포트
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 8. 관계 엣지 해석 (target 문자열 -> 캐릭터 id)
# ---------------------------------------------------------------------------

def resolve_edges(characters):
    # 이름 -> id 룩업 테이블
    lookup = {}

    def add(key, cid):
        if key:
            lookup.setdefault(key.lower().strip(), cid)

    for c in characters:
        add(c["nameEn"], c["id"])
        add(c["title"], c["id"])
        if c.get("stage"):
            # 'Akakagerō (아카카게로우)' -> 'Akakagerō'
            st = re.sub(r"\(.*?\)", "", c["stage"]).strip()
            add(st, c["id"])
        # 성+이름 마지막 토큰
        toks = c["nameEn"].split()
        if len(toks) >= 2:
            add(" ".join(toks), c["id"])

    def resolve(tgt):
        tid = lookup.get(tgt.lower().strip())
        if not tid:
            for k, cid in lookup.items():
                if k and (k in tgt.lower() or tgt.lower() in k) and len(k) > 3:
                    return cid
        return tid

    edges = []
    seen = set()
    for c in characters:
        # 한국어 관계 목록 targetId 해석 (포커스 패널용)
        for rk in c.get("rel_ko", []):
            rk["targetId"] = resolve(rk["target"])
            rk["type"] = classify_rel(rk["text"])
        for rel in c["relationships"]:
            tid = resolve(rel["target"])
            rel["targetId"] = tid
            if tid and tid != c["id"]:
                pair = tuple(sorted([c["id"], tid]))
                if pair not in seen:
                    seen.add(pair)
                    edges.append({"source": c["id"], "target": tid,
                                  "text": rel["text"],
                                  "type": classify_rel(rel["text"])})
    return edges


# 하드코딩 역사 연표 (시고쿠 엔트리 기반)
HISTORY = [
    {"t": "30년 전", "title": "마나 오버플로우",
     "sub": "Mana Overflow",
     "desc": "최초의 마나 오버플로우 발생. 1세대 마법소녀들이 일제히 각성하고, "
             "스즈키 마호(키보오)가 그 중심에 선다. 현대 마법소녀 시대의 시작."},
    {"t": "30년 전 + 6개월", "title": "첫 백귀야행",
     "sub": "First Hyakki Yagyō",
     "desc": "시고쿠에서 최초의 백귀야행 발생. 민담류 아치 에너미 "
             "타마모노마에가 현현하여 요기(妖氣)를 퍼뜨리고, 수만 명의 민간인이 "
             "이성을 잃고 그녀의 권속이 된다."},
    {"t": "약 30년 전", "title": "1세대의 반격",
     "sub": "First-Generation Counterattack",
     "desc": "스즈키 마호가 이끄는 1세대가 타마모에게 중상을 입히지만, "
             "장기간의 요기 노출로 마법소녀들마저 위험에 처한다. 민간인과 "
             "타마모를 구분할 수 없어 결국 후퇴를 선택."},
    {"t": "약 30년 전", "title": "시고쿠 봉인",
     "sub": "The Sealing of Shikoku",
     "desc": "토벌 실패 후 시고쿠는 공식적으로 포기·봉인된다. 마법소녀청 "
             "비개입주의 정책의 근원이 된 최대의 실패."},
    {"t": "근래", "title": "치에리 납치 사건",
     "sub": "Abduction of Chieri",
     "desc": "히노 치에리가 시고쿠로 납치되어 세뇌당한다. 이 사건 이후 "
             "마법소녀청의 비개입·인프라 투자 정책이 한층 강화된다."},
    {"t": "현재", "title": "현재",
     "sub": "Present Day",
     "desc": "17개 지구에 마법소녀가 배치되어 괴이에 맞서는 한편, MGB 방송과 "
             "이벤트로 사회와 공존한다. 시고쿠는 여전히 봉인된 채 타마모의 영역으로 남아 있다."},
]


def report(ds):
    chars = ds["characters"]
    print("=" * 60)
    print("파싱 통계")
    print("=" * 60)
    print("캐릭터:", len(chars))
    print("게스트(이미지만):", len(ds["guests"]),
          "->", [g["nameEn"] for g in ds["guests"]])
    print("로어 페이지:", len(ds["lore"]))
    print("이벤트:", len(ds["events"]))
    total_edges = sum(len(c["relationships"]) for c in chars)
    print("관계 엣지(원시):", total_edges)
    print()
    # 진영 분포
    from collections import Counter
    fc = Counter(c["faction"] for c in chars)
    print("진영 분포:", dict(fc))
    print()
    no_img = [c["title"] for c in chars if not c["imgPrefix"]]
    print("이미지 매칭 실패 캐릭터(%d):" % len(no_img), no_img)
    print("이미지 매칭 성공: %d/%d" % (len(chars) - len(no_img), len(chars)))
    print()
    # 지구 매핑
    dist = [c["title"] for c in chars if c["districtNorm"]]
    print("지구 매핑된 캐릭터: %d" % len(dist))
    nodist_reps = [c["title"] for c in chars
                   if c["faction"] in ("rep", "trainee") and not c["districtNorm"]]
    print("지구 미매핑(대표/연습생):", nodist_reps)
    print()
    print("랭크 라벨 샘플:", [(c["title"], c["rankLabel"], c["stars"]) for c in chars[:6]])
    print()
    print("샘플 캐릭터:")
    for c in chars[:3]:
        print("  -", c["title"], "|", c["nameEn"], "| rank=", c["rank"],
              "| faction=", c["faction"], "| img=", c["imgPrefix"],
              "| rels=", len(c["relationships"]))


# ---------------------------------------------------------------------------
# 9. HTML 생성
# ---------------------------------------------------------------------------

# 지구 지도 좌표 (viewBox 720x920, 북=상단, 일본 형태를 스타일화) + 한글 라벨
MAP_POS = {
    "Northern Hokkaido": {"x": 540, "y": 80, "kr": "홋카이도 북부"},
    "Southern Hokkaido": {"x": 500, "y": 150, "kr": "홋카이도 남부"},
    "Northern Tohoku": {"x": 470, "y": 230, "kr": "도호쿠 북부"},
    "Southern Tohoku": {"x": 455, "y": 300, "kr": "도호쿠 남부"},
    "Eastern Kanto": {"x": 500, "y": 375, "kr": "간토 동부"},
    "Tokyo": {"x": 470, "y": 440, "kr": "도쿄"},
    "Western Kanto": {"x": 405, "y": 420, "kr": "간토 서부"},
    "Eastern Chubu": {"x": 385, "y": 350, "kr": "주부 동부"},
    "Western Chubu": {"x": 320, "y": 365, "kr": "주부 서부"},
    "Kyoto": {"x": 318, "y": 432, "kr": "교토"},
    "Northern Kinki": {"x": 262, "y": 400, "kr": "긴키 북부"},
    "Osaka": {"x": 285, "y": 470, "kr": "오사카"},
    "Southern Kinki": {"x": 330, "y": 505, "kr": "긴키 남부"},
    "Eastern Chugoku": {"x": 205, "y": 445, "kr": "주고쿠 동부"},
    "Western Chugoku": {"x": 130, "y": 470, "kr": "주고쿠 서부"},
    "Northern Kyushu": {"x": 95, "y": 555, "kr": "규슈 북부"},
    "Southern Kyushu": {"x": 110, "y": 640, "kr": "규슈 남부"},
    "Shikoku": {"x": 245, "y": 560, "kr": "시고쿠"},
}


def build_js_data(ds):
    """JS DATA 객체용 dict 구성 (base64 이미지 포함)."""
    # 이미지: prefix -> {d, m}  (사용된 것 + 게스트)
    images = {}
    for pfx, st in ds["images"].items():
        entry = {}
        if "default" in st:
            entry["d"] = b64_uri(st["default"])
        if "magical" in st:
            entry["m"] = b64_uri(st["magical"])
        if entry:
            images[pfx] = entry

    def char_out(c):
        return {
            "id": c["id"], "title": c["title"], "nameEn": c["nameEn"],
            "nameJp": c.get("nameJp"), "hiragana": c.get("hiragana"),
            "stage": c.get("stage"), "rankLabel": c["rankLabel"], "stars": c["stars"],
            "rankKind": c["rankKind"], "age": c.get("age"), "office": c.get("office"),
            "generation": c.get("generation"), "district": c.get("district"),
            "districtNorm": c.get("districtNorm"), "districtKr": c.get("districtKr"),
            "species": c.get("species"),
            "height": c.get("height"), "staff": c.get("staff"),
            "personality": c.get("personality"), "role": c.get("role"),
            "status": c.get("status"), "tagline": c.get("tagline"),
            "faction": c["faction"], "factionLabel": c["factionLabel"],
            "imgPrefix": c.get("imgPrefix"), "raw": c["raw"],
            "relationships": [{"target": r["target"], "text": r["text"],
                               "targetId": r.get("targetId"),
                               "type": r.get("type")}
                              for r in c.get("rel_ko") or c["relationships"]],
        }

    guests = [{"id": g["id"], "title": g["title"], "nameEn": g["nameEn"],
               "faction": "guest", "factionLabel": g["factionLabel"],
               "imgPrefix": g["imgPrefix"], "guest": True,
               "stars": 0, "rankLabel": "게스트"} for g in ds["guests"]]

    return {
        "characters": [char_out(c) for c in ds["characters"]],
        "guests": guests,
        "lore": ds["lore"],
        "events": ds["events"],
        "edges": ds["edges"],
        "history": HISTORY,
        "images": images,
    }


def generate_html(ds):
    import wiki_template
    data = build_js_data(ds)
    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    mappos_json = json.dumps(MAP_POS, ensure_ascii=False)
    # 실측 벡터 지도 데이터
    try:
        import geo_japan
        mapgeo = geo_japan.build_map()
        if mapgeo:
            mapgeo["kr"] = dict(DISTRICT_KR, Hokkaido="홋카이도")
    except Exception as e:
        print("!! 지도 생성 실패, 폴백 사용:", e)
        mapgeo = None
    mapgeo_json = json.dumps(mapgeo, ensure_ascii=False, separators=(",", ":"))
    html = wiki_template.page(data_json, mappos_json, mapgeo_json)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    size_mb = os.path.getsize(OUT_HTML) / 1024 / 1024
    print("\n생성 완료: %s  (%.1f MB)" % (OUT_HTML, size_mb))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    ds = build_dataset(report_only=args.report)
    report(ds)
    if not args.report:
        generate_html(ds)
