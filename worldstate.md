# worldstate.md — 월드 스테이트 & 모듈 설계 (엔진 비종속 스펙)

이 문서는 `lorebook_export.json`(마법소녀 세계관 캐논)을 babechat·zetta류 **인터랙티브 AI 소설 플랫폼**의 근간으로 쓰기 위한 **월드 스테이트(가변 세계 상태) + 모듈(장착형 서사 효과)** 설계 규약이다. 특정 엔진(RisuAI·자체 웹앱·기타 LLM 런타임)에 종속되지 않는 **데이터 계약**만 규정한다. 구현(코드·JSON 스키마 파일)은 다음 단계.

작성 기준 문서: [CLAUDE.md](CLAUDE.md)(프로젝트 규약) · [tonemanner.md](tonemanner.md)(한국어 어투·용어) · [design.md](design.md). 위키 데이터 모델(`build_wiki.py`의 `DATA`)을 캐논 소스로 참조한다.

---

## 0. 한눈에

- **캐논(불변)** 위에 **월드 스테이트(가변)** 를 오버레이한다. 원본은 절대 수정하지 않는다 — 위키의 `localStorage` 편집 오버레이와 같은 철학.
- 세계의 가변 상태는 다섯 갈래: **팩션 영역 / 캐릭터 호감도 / 인벤토리·복장 / 세계 플래그 / 세계의 기억**.
- **복장·장비·아이템·세계의 기억은 전부 하나의 추상 `Module`** 로 통일한다. 모듈은 "조건(`requires`)이 맞으면 서사·상태에 효과(`effects`)를 준다"는 선언이다.
- **"장착하면 스토리가 바뀐다"** 가 핵심: 모듈의 `effects.narrative`가 엔진 프롬프트에 지시문으로 주입된다.
- 엔진은 **세 가지 계약**만 구현하면 된다: ① 상태→프롬프트 **조립** ② 서사 결과→상태 **변이** ③ 단일 JSON **지속**.

---

## 1. 설계 원칙

1. **캐논 불변 / 상태 오버레이 분리.** `lorebook_export.json`·`lorebook_ko.json`·빌드 산출 `DATA`는 read-only 캐논이다. 플레이 중 변하는 것은 전부 별도의 `WorldState` 객체에만 기록한다. 캐논 엔티티는 `id`(예: `char-13`, 지구 키 `Tokyo`)로 참조한다.

2. **데이터 계약만 정의한다.** 이 문서는 상태의 *모양*과 엔진이 지켜야 할 *계약*만 정한다. "어떤 함수를 호출하라" 같은 API는 정하지 않는다. 그래야 RisuAI 로어북에도, 자체 백엔드에도, 다른 런타임에도 같은 세계를 얹을 수 있다.

3. **모듈 = 통합 추상.** 복장·장비·아이템·세계의 기억을 따로 만들지 않는다. 전부 `Module` 하나로 모델링하고 `type`으로만 구분한다. 새 장착물 종류가 생겨도 포맷은 그대로다.

4. **사람이 저작하고, 엔진은 평가만 한다.** 모듈 정의·플래그 카탈로그·호감도 밴드 임계값은 **저작 자산**(작가가 작성)이다. 런타임은 현재 상태에 대고 조건을 평가하고 효과를 적용할 뿐, 규칙을 발명하지 않는다.

5. **선언적 표현식.** 조건과 상태 변경은 코드가 아니라 데이터(`{path, op, value}`)로 적는다. 엔진은 이 작은 표현식 언어만 해석하면 된다(§6).

---

## 2. 계층 모델 — 캐논 vs 스테이트

```
┌──────────────────────────────────────────────┐
│  CANON  (read-only)                            │
│   characters[] · factions · districts ·        │  ← lorebook_export.json
│   relationships(edges) · items(고유 지팡이) ·   │     + lorebook_ko.json
│   lore · events · battles                      │     + build_wiki DATA
├──────────────────────────────────────────────┤
│  AUTHORED ASSETS  (read-only, 저작)             │
│   modules[] · flagCatalog · affinityBands ·    │  ← worldstate 자산
│   territorySeed · seedRules                     │
├──────────────────────────────────────────────┤
│  WORLD STATE  (mutable, 세이브)                 │
│   flags · territory · affinity · inventory ·   │  ← 1회차 = 1 세이브
│   modules.equipped · memory · log              │
└──────────────────────────────────────────────┘
```

- **CANON**: 세계의 사실. 인물·지구·관계·고유 아이템 등. 절대 안 바뀐다.
- **AUTHORED ASSETS**: 캐논 위에 게임성을 부여하는 정의들. 모듈 목록, 플래그 카탈로그, 호감도 밴드 임계, 영역 초기 시드 규칙. 작가가 만든다.
- **WORLD STATE**: 한 플레이어의 한 회차에서 실제로 변하는 값. 직렬화하면 세이브 파일 하나.

---

## 3. WorldState 스키마 (the save object)

런타임 1회차 = `WorldState` 객체 하나. JSON 단일 직렬화 가능(위키 export와 같은 발상).

```jsonc
{
  "meta": {
    "saveId": "run-7f3a",
    "schema": "worldstate/1",
    "turn": 42,                 // 진행한 서사 턴 수
    "ngPlusCount": 1,           // 몇 번째 회차인가 (0 = 첫 플레이)
    "protagonist": "char-13"    // 시점 인물(선택)
  },

  "flags": {                    // 세계 분기 (§4.4)
    "shikoku_sealed": true,
    "chieri_kidnapped": true,
    "gekko_karen_unlocked": false,
    "hyakki_yagyo_active": false,
    "exchange_win_streak": 1    // number 플래그도 허용
  },

  "territory": {                // 팩션 영역/세력 (§4.1)
    "Tokyo":   { "controller": "char-XX", "stability": 90, "sealed": false },
    "Kyoto":   { "controller": "char-13", "stability": 80, "sealed": false },
    "Shikoku": { "controller": null,      "stability": 0,  "sealed": true }
    // ... 17 districtKey
  },

  "affinity": {                 // 캐릭터 호감도 (§4.2)
    "char-13": { "value": 35, "band": "호의",
                 "axes": { "trust": 40, "respect": 60, "romance": 10 } }
    // 등장/상호작용한 캐릭터만 기록 (없으면 시드값으로 간주)
  },

  "inventory": {                // 인벤토리/복장 (§4.3)
    "owned": ["item-akane-katana", "outfit-akane-magical", "mod-memory-shikoku-truth"],
    "equipped": {
      "outfit": "outfit-akane-magical",
      "weapon": "item-akane-katana",
      "accessory": null
    }
  },

  "modules": {                  // 장착형 효과 (§5)
    "equipped": ["outfit-akane-magical", "mod-memory-shikoku-truth"],
    "unlocked": ["mod-memory-shikoku-truth", "mod-memory-true-ending-a"]
  },

  "memory": ["mod-memory-shikoku-truth"],  // 세계의 기억(획득형 모듈 id) — modules.unlocked의 부분집합

  "log": [                      // 변이 이력 (되감기·디버그)
    { "turn": 41, "path": "affinity.char-13.value", "op": "inc", "value": 5, "cause": "scene:42" }
  ]
}
```

설계 메모
- `flags`/`affinity`/`territory`는 **희소(sparse)** 로 저장한다. 키가 없으면 "시드 기본값"으로 간주(저장 용량·diff 최소화).
- `modules.equipped`는 복장·장비 같은 인벤토리 장착물과 세계의 기억을 **함께** 담는다. 인벤토리의 `equipped`는 그중 슬롯이 있는 것들의 뷰일 뿐(둘은 정합성 유지).
- `log`는 선택이지만 권장: 회차 종료 시 **세계의 기억 발급**(§4.4)과 디버깅의 근거가 된다.

---

## 4. 서브시스템

### 4.1 팩션 영역 / 세력 (territory)

캐논은 이미 일본을 **17지구 + 봉인된 시고쿠**로 나누고, 각 지구에 지역대표를 둔다. 그 위에 "지금 누가 어느 정도로 장악하고 있는가"를 얹는다.

| 필드 | 타입 | 의미 |
|---|---|---|
| `controller` | `factionId \| charId \| null` | 현재 실효 지배 세력/인물. 초기엔 지역대표. |
| `stability` | `0–100` | 안정도. 분쟁·괴이 출현으로 하락. |
| `sealed` | `bool` | 봉인 여부. 시고쿠 `true`. |

- **시드**: 캐논의 `character.districtNorm`(지역대표) → 해당 지구 `controller`. 시고쿠 `sealed:true, controller:null`.
- **서사 효과**: 한 장면이 어느 지구에서 벌어지는가에 따라 `controller`/`stability`가 톤·등장 가능 인물·이동 가능성에 반영된다. `stability`가 임계 이하로 떨어지면 `hyakki_yagyo_active` 플래그 트리거 조건이 될 수 있다(저작 규칙).
- **확장 슬롯**: 인접 지구 그래프, 침공/탈환 액션, 세력 자원. 이번 단계에선 상태 필드만 확정.

### 4.2 캐릭터 호감도 (affinity)

캐논의 관계는 산문 + 타입 엣지(소꿉친구·라이벌·사제·돌봄·가족·적대·연심·동료·옛 인연·친구)다. 여기에 **수치 + 밴드**를 얹어 동적으로 만든다.

| 필드 | 타입 | 의미 |
|---|---|---|
| `value` | `-100 ~ 100` | 주 호감도 축. |
| `band` | enum | `value`를 임계로 구간화한 라벨(아래). |
| `axes` | obj? | 다축 옵션: `trust` / `respect` / `romance` 등. |

**밴드(저작 임계, 예시)**

| 밴드 | value 범위 | 행동 지시(요약) |
|---|---|---|
| 적대 | −100 ~ −60 | 경계·적의. 협력 거부, 정보 은폐. |
| 냉담 | −59 ~ −20 | 사무적·거리감. |
| 중립 | −19 ~ 19 | 캐논 기본 태도. |
| 호의 | 20 ~ 49 | 호의적·협조적. |
| 신뢰 | 50 ~ 79 | 속내 공유, 위험 감수. |
| 헌신 | 80 ~ 100 | 자기희생적 충성. |

- **시드(관계 타입 → 시작 밴드)**: 가족·돌봄·소꿉친구 = 호의~신뢰에서 시작, 적대·옛 인연 = 냉담~적대, 라이벌 = 중립(존중은 높게: `axes.respect`↑). 캐논 엣지 `type`에서 자동 시드.
- **밴드가 행동을 토글한다**: 같은 인물도 밴드에 따라 다른 행동 지시문이 프롬프트에 들어간다(§7-①). 이는 **모듈 없이도** 작동하는 기본 상태 효과.
- **캐논 잠재 조건의 형식화**: 나츠메 유이의 "운명의 상대(Destined One)" — `axes.romance ≥ 80`이 되면 헌신·집착·질투형 행동 프로파일로 스왑된다. 이것은 affinity 임계가 행동을 바꾸는 대표 예다.

### 4.3 인벤토리 / 복장 모듈 (inventory + outfit)

아이템·복장은 **모듈의 물리적 표현**이다. 보유(`owned`)와 슬롯 장착(`equipped[slot]`)을 구분한다.

**슬롯(예시)**

| 슬롯 | 내용 | 캐논 시드 |
|---|---|---|
| `outfit` | 평상복 / 변신 의상 / 특수 의상 | 각 캐릭터 default·magical 2종 |
| `weapon` | 고유 마법 지팡이 | 적월(카타나)·리코(하나후다)·히요리(안경)·아야코(삼종신기 모조) 등 |
| `accessory` | 부가 장신구 | 캐논에 묘사된 소품(호시아이 마스코트 등) |
| `consumable` | 소모품 | 호시모리 공방 보급품, 게코카렌 마나 테라피 등 |

- **시드**: 캐논의 `Unique Magical Staff`·복장 2상태를 그대로 기본 아이템/슬롯으로 만든다(작법·이미지가 이미 존재).
- **장착이 서사를 바꾼다(핵심 요구)**: 장착물은 곧 모듈이므로 `effects.narrative`가 장면에 주입된다.
  - 변신 의상 장착 → 전투 가능 톤·능력 사용 허용.
  - 평상복 → 일상 톤, 능력 노출 자제.
  - 특정 유물(예: 시고쿠 관련 유물) 장착 → 분기 플래그 해금.
- **정합성**: `inventory.equipped`에 들어간 슬롯 장착물은 `modules.equipped`에도 반영되어야 한다(엔진이 동기화).

### 4.4 세계 플래그 / 분기 (flags) + 세계의 기억 (memory)

**플래그**는 세계의 분기 상태다. `bool` / `enum` / `number` 모두 허용.

**캐논 분기점 카탈로그(로어북에서 형식화, §9 부록과 연동)**

| 플래그 | 타입 | 의미 / 캐논 근거 |
|---|---|---|
| `shikoku_sealed` | bool | 시고쿠 봉인. 봉인이면 진입·등장 인물 제한. |
| `chieri_kidnapped` | bool | 치에리 납치 → 마법소녀청 비개입 정책 강화. |
| `gekko_karen_unlocked` | bool | 게코카렌 접근권. 해금 조건: 공식 교류전 2연승 등. |
| `hyakki_yagyo_active` | bool | 백귀야행 발생 중. 광역 위협 톤. |
| `hiyori_copy_charges` | number(0–2) | 히요리 능력 복사 슬롯(5분 관찰→1시간, 최대 2). |
| `exchange_win_streak` | number | 교류전 연승 수(해금 조건 계산용). |

**세계의 기억 (memory tokens)** — 메타 진행의 한 형태

- **정의**: 한 회차를 끝내며 특정 엔딩·플래그·업적을 달성하면 발급되는 **획득형 모듈**(`type:"memory"`). 다음 회차 시작 시 장착하면 `requires`가 충족되어 새 분기·서사 개입이 열린다(NewGame+).
- **저작 모듈과 동일 포맷**이다. 차이는 출처뿐: 저작 모듈은 작가가 배포, 세계의 기억은 플레이가 발급.
- **발급 규칙(저작)**: `{ when: <condition>, grants: <moduleId> }` 형태로 정의. 예) "시고쿠의 진실 엔딩 도달 → `mod-memory-shikoku-truth` 발급". 회차 종료 시 `log`/`flags`를 평가해 발급.
- **장착 효과**: 1회차에 몰랐던 사실을 '기억한' 상태로 다시 시작 → 특정 인물이 처음부터 다르게 반응하거나, 잠겨 있던 선택지가 열린다.

> 세계의 기억은 "모듈로 스토리를 바꾼다"의 **메타 진행 버전**일 뿐이다. 복장·장비도 같은 메커니즘으로 스토리를 바꾼다 — 그게 사용자가 강조한 핵심이다.

---

## 5. 모듈 통합 스펙

복장·장비·아이템·세계의 기억을 하나로 묶는 추상.

```jsonc
{
  "id": "outfit-akane-magical",
  "type": "outfit",               // outfit | equipment | item | memory
  "title": "변신 의상 · 적월",
  "slot": "outfit",               // 슬롯형이면 명시 (memory는 보통 슬롯 없음)
  "ownedBy": "char-13",           // 특정 캐릭터 귀속(선택)

  "requires": [                   // 모두 참이어야 효과 발동 (AND). 비면 항상.
    { "path": "flags.shikoku_sealed", "op": "eq", "value": true }
  ],

  "effects": {
    "narrative": [                // 엔진 프롬프트에 주입할 서사 지시문(한국어, tonemanner 준수)
      "아카네는 변신한 상태다. 전투 능력 사용이 허용되며, 말투는 평소보다 결연하다."
    ],
    "state": [                    // 장착/사용 시 상태 델타
      { "path": "affinity.char-14.axes.respect", "op": "inc", "value": 3 }
    ],
    "unlocks": ["gekko_karen_unlocked"]   // 플래그/모듈 해금
  },

  "conflictsWith": ["outfit-akane-casual"]  // 동시 장착 불가
}
```

필드 규약
- `type`: `outfit`·`equipment`·`item`·`memory`. UI·발급 출처가 다를 뿐 평가 방식은 동일.
- `requires`: `{path,op,value}` 조건 배열(§6). 모두 참일 때만 `effects` 적용. 세계의 기억은 보통 `{path:"meta.ngPlusCount", op:"gte", value:1}` 류를 갖는다.
- `effects.narrative`: **이 모듈이 켜졌을 때 LLM이 알아야 할 지시문**. 장면 생성 시 컨텍스트로 들어간다. 한국어·tonemanner 준수, 헤지·번역투 금지.
- `effects.state`: 장착(또는 사용) 시 적용할 상태 변경.
- `effects.unlocks`: 다른 플래그·모듈 해금.
- `conflictsWith`: 상호 배타(평상복 vs 변신 의상 등).

---

## 6. 표현식 — 조건과 상태 변경 (엔진 비종속)

조건(`requires`)과 변경(`effects.state`, 발급 규칙)은 작은 선언적 표현식으로만 쓴다. 엔진은 이 표만 해석하면 된다.

**경로(path)**: `WorldState`의 점 경로. 예) `flags.shikoku_sealed`, `affinity.char-13.value`, `territory.Kyoto.stability`, `inventory.equipped.outfit`, `meta.ngPlusCount`.

**조건 연산자(op, requires용)**

| op | 의미 |
|---|---|
| `eq` / `ne` | 같다 / 다르다 |
| `gt` / `gte` / `lt` / `lte` | 크다/이상/작다/이하(number) |
| `in` / `nin` | 값이 배열에 포함/미포함 |
| `has` | 배열 경로(owned/equipped/memory)에 value가 들어있다 |

**변경 연산자(op, state 델타용)**

| op | 의미 |
|---|---|
| `set` | 지정 값으로 설정 |
| `inc` / `dec` | 수치 증감(범위 클램프) |
| `push` / `pull` | 배열에 추가/제거 |
| `toggle` | bool 반전 |

규칙
- `requires`의 여러 조건은 **AND**. **OR**가 필요하면 모듈/규칙을 둘로 나눈다(단순성 유지).
- `inc`/`dec`는 해당 필드의 범위로 클램프(호감도 −100~100, 안정도 0~100).
- `set band`는 직접 쓰지 않는다 — `value` 변경 후 엔진이 밴드를 **파생**한다(§7-②).

---

## 7. 세 가지 엔진 계약

엔진이 이 셋만 구현하면 어떤 런타임이든 같은 세계가 돈다.

**① 컨텍스트 조립 (상태 → 프롬프트)**
현재 `WorldState`를 평가해 LLM 주입 블록을 만든다.
- 활성 모듈(장착 + `requires` 충족) 전체의 `effects.narrative`를 모은다.
- 각 등장 캐릭터의 호감도 `band`에 대응하는 행동 지시문을 붙인다.
- 현재 지구의 `controller`/`stability`/`sealed`와 관련 플래그를 요약한다.
- 이 블록을 엔진별 위치에 넣는다: RisuAI면 로어북/저자 노트 주입, 자체 엔진이면 system prompt. **위치만 다르고 내용 계약은 동일.**

**② 변이 (서사 결과 → 상태 델타)**
한 턴의 서사 결과에서 상태 변화를 뽑아 `WorldState`에 적용한다. 두 방식 모두 허용:
- (a) **구조화 출력**: 엔진이 서술과 함께 델타(JSON/tool 호출)를 방출 → 그대로 적용.
- (b) **선택지 매핑**: 사전 정의된 선택지/액션이 고정 델타를 들고 있어, 플레이어 선택이 곧 델타.
적용 후 영향받은 `affinity.*.value`의 `band`를 재계산하고, 해금/충돌·발급 규칙을 평가한다. 각 델타는 `log`에 적는다.

**③ 지속 / 직렬화**
`WorldState`는 단일 JSON 세이브. 저장·로드·공유 가능(위키 export와 동일 사고). 회차 종료 시 발급 규칙(`{when, grants}`)을 평가해 **세계의 기억**을 `modules.unlocked`/`memory`에 추가한다.

**런타임 루프(요약)**
```
로드 → [조립①] 프롬프트 구성 → LLM 서사 생성
     → 플레이어 입력/선택 → [변이②] 델타 적용·밴드 재계산·해금 평가
     → [지속③] 저장 → (반복)
회차 종료 → 발급 규칙 평가 → 세계의 기억 발급 → 다음 회차로 이월
```

---

## 8. 캐논과의 연결 (시드 파이프라인)

월드 스테이트의 초기값은 캐논에서 자동 생성한다(저작 시드 규칙).

- `territory[*].controller` ← 캐논 지역대표(`character.districtNorm`).
- `territory.Shikoku.sealed = true` ← 캐논(시고쿠 황폐·봉인).
- `affinity[*]` 시작 밴드 ← 캐논 관계 엣지 `type`(가족=신뢰, 적대=냉담 …).
- `inventory.owned` 기본 ← 캐논 고유 지팡이 + 복장 2상태.
- `flags` 초기값 ← 캐논 현재 시점(예: `shikoku_sealed:true`).

이렇게 하면 "빈 세계"가 아니라 **캐논과 일관된 세계**에서 1회차가 시작된다.

---

## 9. 부록 — 로어북 잠재 조건 → 형식화 매핑

캐논 프로즈에 이미 들어있는 조건/분기를 상태·모듈로 옮긴 표. (구현 단계에서 출처 엔트리 인용을 덧붙인다.)

| 캐논 프로즈(요지) | 형식화 |
|---|---|
| 시고쿠는 황폐해 마법소녀 미배치·봉인 | `flags.shikoku_sealed=true`, `territory.Shikoku.sealed=true` |
| 치에리가 시고쿠로 납치되면 청의 비개입 강화 | `flags.chieri_kidnapped` → 트리거로 관련 톤/정책 지시 |
| 게코카렌 접근권은 교류전 2연승·대형 괴이 격파 등으로 부여 | `flags.gekko_karen_unlocked`, 조건 `exchange_win_streak ≥ 2` |
| 마나 오버플로우 6개월 뒤 시고쿠서 첫 백귀야행·타마모노마에 현현 | `flags.hyakki_yagyo_active`, 영역 stability 연동 |
| 히요리: 5분 관찰 시 능력 복사 1시간, 최대 2 슬롯 | `flags.hiyori_copy_charges`(0–2) + 사용 모듈 |
| 나츠메: '운명의 상대'에게 헌신·집착·질투 | `affinity.<id>.axes.romance ≥ 80` → 행동 프로파일 스왑 |
| 호시아이: 마스코트 소실 시 거친 1인칭·가학 인격으로 전환 | `accessory` 모듈(마스코트) 해제 → 인격 스왑 directive |
| 각 캐릭터 고유 지팡이(적월·하나후다·안경 등) | `item`/`weapon` 모듈로 시드 |
| 평상복 / 변신 의상 2상태 | `outfit` 모듈 2종, `conflictsWith`로 배타 |
| 회차 종료 시 달성 엔딩 | `{when, grants}` → `type:"memory"` 모듈 발급(NewGame+) |

---

## 10. 범위와 다음 단계

**이번 문서의 범위**: 위 1~9의 *설계*. 코드·JSON 스키마 파일은 만들지 않는다.

**확장 슬롯(이번엔 상태 자리만 비워둠)**: 영역 인접 그래프·침공 액션·세력 자원, 호감도 다축 가중, 소모품 경제, 퀘스트/목표 트래커, 전투 규칙(현 `battle_scenes.json`은 예시 산문이지 규칙이 아님).

**구현 현황 (v6 — 클라이언트 단독 플레이 앱):** 본 설계는 `build_play.py` + `play_template.py`로 구현되어 **`lorebook-play.html`**(vanilla 단일 HTML, BYO 키)로 빌드된다.
- 저작 자산: `affinity_bands.json`(밴드 임계) · `flag_catalog.json`(캐논 분기 플래그 + 발급 규칙) · `modules.json`(세계의 기억·특수 모듈). 복장/무기 모듈은 `build_play.derive_modules()`가 캐논에서 자동 파생.
- 시드 생성기: `build_play.seed_world()`가 캐논 `DATA`(지역대표→영역 controller, 시고쿠 봉인, 관계 타입→호감도 시작값)에서 초기 `WorldState`를 만든다.
- 세 계약: `play_template.py` JS의 `assembleContext()`(조립) · `mutate()`+상태 델타 펜스 프로토콜(변이) · localStorage 세이브 슬롯(지속)으로 구현. 어댑터는 openai/anthropic/gemini/mock.

**남은 후속(선택):** `world_schema.json`(검증용 JSON Schema), RisuAI 로어북 주입 어댑터, 영역/퀘스트 등 확장 슬롯.
