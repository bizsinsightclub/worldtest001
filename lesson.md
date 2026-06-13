# lesson.md — Lessons Learned

작업 중 얻은 교훈을 누적 기록한다. 새 교훈은 아래에 계속 추가.

## 로어북(RisuAI) 포맷

- 최상위 `{type:"risu", ver:1, data:[...]}`. `data`는 92개 엔트리.
- `mode:"folder"` 엔트리는 **카테고리 구분자**(content 없음). 키에 `folder:<uuid>`. 후속 엔트리가 그 폴더 소속 — 단, **순서 기반 귀속은 불완전**(괴이/시고쿠가 연습생 폴더 구간에 섞임). 폴더 위치만 믿지 말고 내용·NPC 태그라인으로 보정.
- 폴더 키에 보이지 않는 **``(U+F000) 프리픽스**가 붙는다 → 제거 후 사용.
- 프로필 필드는 **`-` 와 `*` 불릿 혼용**. 일부 캐릭터(타마모·치에리·치히로)는 `Name:` 대신 `Formal Name:`/`Self-Name:` 사용 → 대체 필드명 폴백 필요.
- `Personality`에 MBTI·에니어그램이 섞여 들어옴(예: `... ISTJ, 8w9`).

## 이미지 매칭

- 파일명 `{GivenName}_default.webp` / `{GivenName}_magical girl default.webp`. given-name = 영문 이름 토큰 중 하나.
- 매칭은 **이름 토큰을 `[\s/\-]`로 분리** 후 prefix와 대조. 하이픈 분리 안 하면 `Tamamo-no-Mae`가 `Tamamo` 이미지에 안 붙음.
- 일부 인물(스즈키 마호·모리카와 호시노 + 빌런 4종)은 **원본에 초상 없음** — 정상. 6개 카메오 이미지(Eden/Hanarin/Hayeul/Lucifer/Nori/Yeun)는 프로필 없음 → "게스트" 카드로.

## 파싱 버그 사례

- **월(月) 추정 부분일치**: `"may"`(영어 조동사)가 MONTHS에 매칭, `"1월"`이 `"11월"`의 부분문자열로 오인. → 본문 말고 **keys/제목에서만**, 그리고 **정규식 자릿수 경계**(`(?<!\d)(\d{1,2})\s*월`)로 해결.
- 관계 대상 해석은 영문 풀네임/한글 정식명/스테이지명 다중 룩업 + 부분매칭 폴백으로.

## 출력 · 검증 환경

- Windows 콘솔 cp949 → 유니코드 출력 시 `sys.stdout.reconfigure(encoding="utf-8")` 필수.
- **Playwright는 `file://` 차단** → `python -m http.server`로 서빙 후 검증.
- 단일 HTML에 이미지 base64 인라인 시 ~10.5MB. 브라우저에서 무리 없이 열리나, 데이터는 `separators=(",",":")`로 압축.

## v2 교훈

- **번역 서브에이전트 JSON 이스케이프**: 에이전트가 JSON을 직접 쓰게 하면 값 안의 한국어 대사 큰따옴표(`"재능,"`)를 이스케이프하지 않아 10개 중 5개 파일이 깨졌다. → `translate_lorebook.py`의 `tolerant_load`로 키 패턴(`"<digits>":`)을 앵커 삼아 bare-quote만 이스케이프해 복구. 다음엔 에이전트가 **plain .md 파일**을 쓰게 하고 파이썬이 JSON으로 묶는 편이 안전.
- **번역값 라벨 중복**: 한 배치가 `Species:` 값에 `종족: 인간`처럼 라벨을 덧붙임(44건). → 표시 단계 `strip_redundant_label` + 열거형은 영문 원본 기준 KR 매핑(`species_kr`)으로 회피.
- **파싱/표시 분리 원칙 유효**: 영문 원본으로 구조·이미지·관계를 해석하고 KO는 표시값만 머지하니 번역이 깨져도 구조가 안전. 번역 시 `- English Label:`·`#### Section` 헤더 유지가 핵심.
- **오프라인 실측 지도**: `dataofjapan/land` GeoJSON(47현)을 등각투영해 SVG path로 인라인(타일 불필요). 47현→17 가상구역 매핑 시 홋카이도는 단일 현이라 N/S를 한 지도구역으로 묶고 패널에서 둘 다 표시. 오키나와·오가사와라는 윈도 클리핑으로 제외.
- **CSS `color-mix`**로 팩션색 반투명 배경을 토큰 하나(`--c`)로 처리 — 모던 브라우저 전제(오프라인 로컬 용도 OK).
- **IntersectionObserver root**: 스크롤 컨테이너가 `#main`이라 observer `root`를 명시해야 연표 각인 리빌이 정확히 트리거. 뷰 전환(`show`) 시 재관찰 필요.
- 단일 HTML 용량 ~11.4MB(이미지 base64 + KO 데이터). 여전히 즉시 로드 가능.
