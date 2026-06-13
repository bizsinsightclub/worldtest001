# CLAUDE.md — 마법소녀 세계관 위키 프로젝트

/ 이 파일은 이 저장소에서 작업할 때의 기준 규약이다. 작업 전 [design.md](design.md)·[tonemanner.md](tonemanner.md)·[lesson.md](lesson.md)도 함께 참고할 것.

## 프로젝트란

`lorebook_export.json`(RisuAI 로어북, 현대 일본 배경 **마법소녀** 세계관, 92엔트리)을 분석해 **독자용 위키/시각화 툴**을 만든다. 산출물은 브라우저에서 더블클릭으로 열리는 **단일 HTML**(`lorebook-wiki.html`). 5개 뷰: 캐릭터 도감 · 세계 설정 · 관계도 · 지구 지도 · 연표 / 캘린더.

## 파일 맵

| 파일 | 역할 |
|---|---|
| `lorebook_export.json` | 원본 로어북 (영문, RisuAI export). **수정하지 않음** |
| `build_wiki.py` | 파서 + 데이터 조립 + HTML 생성기. 진입점 |
| `wiki_template.py` | HTML/CSS/JS 템플릿. `build_wiki.py`가 DATA를 주입 |
| `translate_lorebook.py` | 번역 파이프라인 (병렬 서브에이전트 → `lorebook_ko.json`) |
| `geo_japan.py` | 도도부현 GeoJSON → 17구역 투영 SVG 데이터 |
| `lorebook_ko.json` | 한국어 번역 캐시 (엔트리별). 재빌드 시 재사용 |
| `japan_pref.geojson` | 도도부현 경계 캐시 (1회 다운로드) |
| `lorebook-wiki.html` | **최종 산출물** (데이터·이미지 base64·JS·CSS 인라인) |
| 이미지 | `C:\Users\User\Documents\카카오톡 받은 파일\collected_chars` (`{GivenName}_default.webp`, `{GivenName}_magical girl default.webp`) |

## 빌드 · 검증

```bash
python build_wiki.py            # lorebook-wiki.html 생성
python build_wiki.py --report   # 파싱·매칭 통계만 출력 (HTML 미생성)
```

검증은 반드시 **HTTP 서빙 후 Playwright**로 한다 — Playwright는 `file://`을 차단한다:

```bash
python -m http.server 8765 --bind 127.0.0.1   # 백그라운드
# → http://127.0.0.1:8765/lorebook-wiki.html 를 Playwright로 로드, 5개 뷰 스크린샷 대조
```

실사용 시에는 HTML을 그냥 더블클릭하면 된다(오프라인 작동).

## 하드 제약

- **단일 HTML · 완전 오프라인** — 외부 CDN·타일·폰트 의존 금지. 라이브러리가 필요하면 인라인하거나 vanilla로 자체 구현.
- **표준 라이브러리 우선** — `build_wiki.py`는 가능한 한 파이썬 표준 라이브러리만 사용. 외부 패키지는 빌드 타임 한정(예: GeoJSON 다운로드)으로만, 없으면 폴백.
- **원본 불변** — `lorebook_export.json`은 읽기 전용. 파생물(ko/geojson)은 캐시 파일로 분리.
- **언어** — 위키 primary 언어는 **한국어**. 규칙은 [tonemanner.md](tonemanner.md).
- **디자인** — Reverse:1999 빈티지(세피아/골드) + 루비 표기. 규칙은 [design.md](design.md).

## 코드 컨벤션

- 파일 인코딩 UTF-8, 콘솔 출력은 `sys.stdout.reconfigure(encoding="utf-8")`(Windows cp949 회피).
- 파서는 **방어적으로**: `*`/`-` 불릿 혼용, `Name`/`Formal Name`/`Self-Name` 대체 필드, 매칭 실패 시 폴백을 둔다(→ [lesson.md](lesson.md)).
- 영문 원본은 **정규 키**(이미지 매칭·관계 해석)용으로 계속 파싱하고, **표시값만** 한국어 캐시에서 머지한다. 이 분리를 깨지 말 것.

## 작업 순서 (v2)

문서화(본 4종) → 번역 파이프라인 → 실측 지도 → 연표/캘린더 분리 → 팩션 칩/관계도. 자세한 계획은 플랜 파일 참조.
