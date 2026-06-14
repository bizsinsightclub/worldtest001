# 마법소녀 세계관 위키 · Magical Girl Lorebook Wiki

인터랙티브 AI 판타지 소설(현대 일본 배경 **마법소녀** 세계관)의 로어북을 분석해
만든 **단일 HTML 위키/시각화 툴**입니다. 빌드·설치 없이 브라우저에서 바로 열립니다.

`lorebook-wiki.html` 을 더블클릭하면 오프라인으로 작동합니다.

## 6개 뷰

- **캐릭터 도감** — 62명 프로필(이미지·랭크·스탯·관계), 일상↔변신 토글, 진영 필터
- **세계 설정** — 마법소녀 체계·괴이·마법소녀청·시고쿠의 비극 등 위키 문서
- **관계도** — 팩션 클러스터 + 클릭 포커스, 관계 유형별 색상 엣지
- **지구 지도** — 일본 16개 지구 실측 벡터 지도(시고쿠 봉인)
- **연표 / 캘린더** — 현재→과거 세로 연표(각인 연출)와 사계 이벤트
- **전투 사례** — 세계관 작법을 따른 전투 묘사 예시 10종

## 편집(관리자) 모드

검색창 왼쪽 **🔑 편집** 버튼을 누르면 관리자 모드로 전환됩니다.

- **인라인 편집**: 점선으로 표시된 텍스트(이름·스탯·제목·태그 등)를 클릭해 바로 수정.
- **원문 편집**: 프로필·세계설정·전투·이벤트 본문은 **✎ 원문 편집**으로 전체 텍스트 수정.
- **저장**: 변경 사항은 브라우저 **localStorage**에 자동 저장됩니다(같은 브라우저에서 유지).
- **HTML 내보내기**: 편집을 반영한 새 `lorebook-wiki-edited.html` 을 내려받습니다(배포·이전용).
- **초기화**: 모든 편집을 지웁니다.

## 재빌드 (선택)

산출물은 자가완결형이라 그대로 써도 되지만, 데이터를 바꿔 재생성하려면:

```bash
python build_wiki.py            # lorebook-wiki.html 생성
python build_wiki.py --report   # 파싱·매칭 통계만 출력
```

캐릭터 이미지는 동봉된 **`images/`** 폴더(`{이름}_default.webp`,
`{이름}_magical girl default.webp`)에서 자동 인식됩니다. 번역·관계·전투 캐시
(`lorebook_ko.json`·`relation_types.json`·`battle_scenes.json`)는 그대로 재사용됩니다.

규약 문서: [CLAUDE.md](CLAUDE.md) · [design.md](design.md) ·
[tonemanner.md](tonemanner.md) · [lesson.md](lesson.md).

## 패키지

`python package.py` 로 소유권 이전용 ZIP(`lorebook-wiki-package.zip`)을 만듭니다
— 소스·데이터·문서·이미지·최종 HTML 포함, 재빌드 가능.

> 주 언어는 한국어. 고유명사는 한글 메인 + 일어/영문 병기. 원본 `lorebook_export.json` 은 읽기 전용.
