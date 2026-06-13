# 마법소녀 세계관 위키 · Magical Girl Lorebook Wiki

인터랙티브 AI 판타지 소설(현대 일본 배경 **마법소녀** 세계관)의 로어북을 분석해
만든 **단일 HTML 위키/시각화 툴**입니다. 빌드·설치 없이 브라우저에서 바로 열립니다.

🔗 **GitHub Pages**: 저장소 `Settings → Pages → Branch: main / root` 활성화 후
`https://bizsinsightclub.github.io/worldtest001/` 로 접속.

## 5개 뷰

- **캐릭터 도감** — 62명 프로필(이미지·랭크·스탯·관계), 일상↔변신 토글, 진영 필터
- **세계 설정** — 마법소녀 체계·괴이·마법소녀청·시고쿠의 비극 등 위키 문서
- **관계도** — 팩션 클러스터 + 클릭 포커스, 관계 유형별 색상 엣지
- **지구 지도** — 일본 17개 지구 실측 벡터 지도(시고쿠 봉인)
- **연표 / 캘린더** — 현재→과거 세로 연표(각인 연출)와 사계 이벤트

## 빌드 (선택)

산출물 `lorebook-wiki.html` 은 자가완결형이라 그대로 열면 됩니다. 재생성하려면:

```bash
python translate_lorebook.py --merge   # 번역 캐시(lorebook_ko.json) 병합
python build_wiki.py                    # lorebook-wiki.html 생성
```

빌드·디자인·번역 규약은 [CLAUDE.md](CLAUDE.md) · [design.md](design.md) ·
[tonemanner.md](tonemanner.md) · [lesson.md](lesson.md) 참고.

> 한국어 primary. 캐릭터 일러스트는 HTML에 base64로 인라인되어 있습니다.
