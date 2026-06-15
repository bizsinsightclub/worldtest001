# -*- coding: utf-8 -*-
"""play_template.py — 인터랙티브 플레이 앱 HTML/CSS/JS 템플릿 (vanilla, 단일 파일).

build_play.py 가 캐논(CANON)·초기 월드(WORLD)·저작 자산(ASSETS)을 주입한다.
wiki_template 의 디자인 토큰·헬퍼 패턴을 차용하되, 플레이 전용 런타임을 담는다.
"""

# 종이 질감 노이즈 (wiki_template 와 동일)
NOISE = ("data:image/svg+xml;base64,"
         "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNjAiIGhl"
         "aWdodD0iMTYwIj48ZmlsdGVyIGlkPSJuIj48ZmVUdXJidWxlbmNlIHR5cGU9ImZyYWN0YWxO"
         "b2lzZSIgYmFzZUZyZXF1ZW5jeT0iMC44IiBudW1PY3RhdmVzPSIyIiBzdGl0Y2hUaWxlcz0i"
         "c3RpdGNoIi8+PC9maWx0ZXI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmls"
         "dGVyPSJ1cmwoI24pIiBvcGFjaXR5PSIwLjYiLz48L3N2Zz4=")

CSS = r"""
:root{
  /* Plum Violet 벨벳 (Pantone 20-0132 #2A0F38) */
  --bg:#160a22; --bg2:#1e0f30; --panel:#2a0f38; --panel2:#3a1a50;
  --ink:#ece2f6; --ink-dim:#bcaad6; --ink-faint:#8d7ab0;
  /* 주 액센트 = 자수정(보라). 변수명은 유지하되 보라로 재정의 */
  --gold:#b98cff; --gold-bright:#d9c4ff; --gold-deep:#6e4fa0;
  --shimmer:#cbb06a;            /* 금속 골드 시머(희소) */
  --line:#4a2f6b; --line-soft:#33214d;
  --rep:#d9b65f; --bureau:#7fb6ff; --trainee:#8fd0a8;
  --shikoku:#d98fc9; --refusal:#e87a8c; --villain:#b98cff; --guest:#a89ac0;
  --shadow:0 12px 40px rgba(8,2,18,.6);
}
*{box-sizing:border-box}
html,body{margin:0;height:100%}
body{
  background:
    radial-gradient(120% 85% at 50% -12%, #4a2168 0%, #2a0f38 42%, #160a22 72%, #0a0414 100%),
    radial-gradient(70% 50% at 85% 8%, rgba(150,110,220,.16), transparent 60%),
    radial-gradient(60% 45% at 12% 90%, rgba(110,79,160,.14), transparent 60%);
  background-attachment:fixed;
  color:var(--ink);
  font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',system-ui,sans-serif;
  font-size:15px; line-height:1.6; overflow:hidden;
}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:9999;
  background-image:url('__NOISE__');background-size:160px;opacity:.05;mix-blend-mode:overlay}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:9998;
  box-shadow:inset 0 0 220px 60px rgba(0,0,0,.65)}
h1,h2,h3,.serif{font-family:'Iowan Old Style','Palatino Linotype','Book Antiqua',Palatino,'Nanum Myeongjo',Georgia,serif}
::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-thumb{background:#4a2f6b;border-radius:6px;border:2px solid var(--bg)}
::-webkit-scrollbar-track{background:transparent}
ruby{ruby-position:over} rt{font-size:.5em;color:var(--gold);font-weight:600}

/* 레이아웃 */
/* iOS Safari: 100vh/100dvh는 하단 플로팅 툴바 '뒤'로 콘텐츠가 들어가 입력바가 가려짐.
   100svh(가장 작은 뷰포트=브라우저 UI 항상 표시 기준)로 하면 입력바가 늘 보임. 미지원 시 100vh 폴백. */
#app{display:grid;grid-template-columns:1fr;grid-template-rows:60px 1fr;height:100vh;height:100svh}
#topbar{display:flex;align-items:center;gap:14px;padding:0 20px;border-bottom:1px solid var(--line);
  background:linear-gradient(180deg,#2a153e,#1f0f2e);box-shadow:0 2px 18px rgba(0,0,0,.5);z-index:50}
.brand{font-size:18px;font-weight:700;color:var(--gold-bright);text-shadow:0 1px 0 #000;white-space:nowrap}
.brand small{display:block;font-size:9px;letter-spacing:.32em;color:var(--ink-faint);text-transform:uppercase}
#nav{display:flex;gap:6px;margin-left:18px}
.navbtn{background:transparent;border:1px solid transparent;color:var(--ink-dim);padding:7px 14px;
  border-radius:9px;cursor:pointer;font-size:13px;font-weight:600;font-family:inherit}
.navbtn:hover{color:var(--ink);background:#00000033}
.navbtn.active{color:var(--gold-bright);border-color:var(--gold-deep);background:#00000044}
.navbtn:disabled{opacity:.35;cursor:not-allowed}
#topspacer{margin-left:auto}
.tbtn{background:#18092a;border:1px solid var(--line);color:var(--ink-dim);padding:7px 13px;border-radius:9px;
  cursor:pointer;font-size:12px;font-weight:600;font-family:inherit}
.tbtn:hover{border-color:var(--gold-deep);color:var(--ink)}
#runtag{font-size:12px;color:var(--ink-faint);margin-right:4px}

main{position:relative;overflow:hidden}
.view{display:none;position:absolute;inset:0;overflow:auto}
.view.active{display:block}
/* 모바일: 햄버거 드로어 + 레일 시트 (기본은 데스크톱 — 토글/스크림 숨김) */
.navtoggle{display:none}
.railtoggle{display:none}
#scrim{display:none;position:fixed;inset:0;background:#0009;z-index:60}
body.nav-open #scrim,body.rail-open #scrim{display:block}
#view-wiki{padding:0;overflow:hidden}
#wikiFrame{width:100%;height:100%;border:0;display:block;background:var(--bg)}
.pad{max-width:1100px;margin:0 auto;padding:26px 30px 60px}
.kicker{font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:var(--gold-deep);margin-bottom:6px}
h2.title{font-size:26px;margin:.1em 0 .5em;color:var(--gold-bright)}
.center{text-align:center}
/* 메인 히어로 타이틀 */
.hero{text-align:center;margin:10px 0 28px}
.hero-kicker{font-size:11px;letter-spacing:.42em;text-transform:uppercase;color:var(--gold-deep);margin-bottom:12px}
.hero-title{font-family:'Iowan Old Style','Nanum Myeongjo',Palatino,Georgia,serif;font-size:48px;line-height:1.04;margin:0;
  color:var(--gold-bright);letter-spacing:.02em;text-shadow:0 2px 22px rgba(150,110,220,.5),0 1px 0 #000}
.hero-sub{font-family:'Iowan Old Style','Nanum Myeongjo',Palatino,Georgia,serif;font-size:21px;font-style:italic;color:var(--ink-dim);margin-top:8px}
.pick-card{padding:24px 24px 10px}
/* '당신' 모드 토글 + 페르소나 패널 + 시작 설정 */
.youmode{display:flex;gap:8px;justify-content:center;margin:0 0 16px}
.youmode button{font-family:inherit;cursor:pointer;background:#18092a;border:1px solid var(--line);color:var(--ink-dim);
  padding:8px 16px;border-radius:10px;font-size:13px;font-weight:600}
.youmode button.on{background:linear-gradient(180deg,#3a1a50,#2a0f38);border-color:var(--gold-deep);color:var(--gold-bright)}
.youmode-desc{text-align:center;font-size:12.5px;color:var(--ink-dim);margin:0 0 16px;line-height:1.55}
.youmode-desc b{color:var(--gold-bright);font-weight:700}
.persona-panel{margin:0 0 14px}
.persona-panel.hide{display:none}
.psn-chips{display:flex;gap:7px;flex-wrap:wrap;margin:0 0 12px}
.psn-chip{display:inline-flex;align-items:center;gap:7px;background:#18092a;border:1px solid var(--line);color:var(--ink-dim);
  padding:6px 11px;border-radius:18px;font-size:12.5px;cursor:pointer}
.psn-chip.on{border-color:var(--gold-deep);color:var(--gold-bright);background:#241138}
.psn-chip .del{color:var(--ink-faint);font-size:11px;border:0;background:none;cursor:pointer;padding:0 0 0 2px}
.psn-form{border:1px solid var(--line-soft);border-radius:12px;padding:14px;background:#1b0c2b}
.psn-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px}
.psn-grid .full{grid-column:1/-1}
.psn-form label{display:block;font-size:11.5px;color:var(--ink-faint);margin:0 0 4px;letter-spacing:.03em}
.psn-form .req{color:var(--refusal)}
.psn-form input,.psn-form textarea{width:100%;box-sizing:border-box;background:#120724;border:1px solid var(--line);color:var(--ink);
  border-radius:9px;padding:9px 11px;font-family:inherit;font-size:13.5px}
.psn-form textarea{min-height:84px;resize:vertical;line-height:1.55}
.psn-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:4px;justify-content:center}
.startset{display:flex;gap:14px;align-items:center;justify-content:center;flex-wrap:wrap;margin:18px 0 4px;
  border-top:1px solid var(--line-soft);padding-top:16px}
.startset .ss-lab{font-size:12px;color:var(--ink-faint)}
.startset select{background:#18092a;border:1px solid var(--line);color:var(--ink);border-radius:9px;padding:7px 10px;font-family:inherit;font-size:13px}
.tonebtns{display:inline-flex;gap:6px}
.tonebtns button{font-family:inherit;cursor:pointer;background:#18092a;border:1px solid var(--line);color:var(--ink-dim);padding:6px 12px;border-radius:8px;font-size:12.5px}
.tonebtns button.on{border-color:var(--gold-deep);color:var(--gold-bright);background:#241138}
/* 시작 상황 카드(플레이 로그 상단) */
.sitcard{max-width:760px;margin:0 auto 18px;border:1px solid var(--gold-deep);border-radius:12px;
  background:linear-gradient(180deg,#241138,#1b0c2b);padding:12px 16px}
.sc-h{color:var(--gold-bright);font-size:12px;letter-spacing:.08em;margin-bottom:8px}
.sc-chips{display:flex;gap:8px;flex-wrap:wrap}
.scchip{font-size:12px;color:var(--ink-dim);background:#160a26;border:1px solid var(--line-soft);border-radius:14px;padding:4px 10px}
.scchip b{color:var(--gold);font-weight:600;margin-right:4px}
/* 호버 툴팁(약어→실제 기술명) */
.tip{position:relative;cursor:help;border-bottom:1px dotted var(--gold-deep)}
.tip::after{content:attr(data-tip);position:absolute;left:0;bottom:142%;width:max-content;max-width:280px;white-space:normal;
  background:#160a26;border:1px solid var(--gold-deep);color:var(--ink);font-size:11px;font-weight:400;line-height:1.45;
  padding:6px 9px;border-radius:8px;opacity:0;pointer-events:none;transform:translateY(4px);transition:.15s;z-index:30;box-shadow:var(--shadow)}
.tip:hover::after{opacity:1;transform:none}
.muted{color:var(--ink-faint)}
.card2{background:linear-gradient(180deg,var(--panel),var(--panel2));border:1px solid var(--line);
  border-radius:14px;padding:18px 20px;box-shadow:var(--shadow);margin-bottom:18px}
.card2 h3{margin:.1em 0 .6em;color:var(--gold);font-size:16px}
label.fld{display:block;font-size:12px;color:var(--ink-dim);margin:10px 0 4px;font-weight:600}
input.tin,select.tin,textarea.tin{width:100%;background:#18092a;border:1px solid var(--line);color:var(--ink);
  padding:9px 12px;border-radius:9px;font-size:14px;font-family:inherit;outline:none}
input.tin:focus,select.tin:focus,textarea.tin:focus{border-color:var(--gold-deep);box-shadow:0 0 0 2px rgba(201,162,75,.15)}
.btn{background:linear-gradient(180deg,#4a2e6e,#3a2256);border:1px solid var(--gold-deep);color:var(--gold-bright);
  padding:10px 18px;border-radius:10px;cursor:pointer;font-size:14px;font-weight:700;font-family:inherit}
.btn:hover{background:linear-gradient(180deg,#5a3a82,#34164a)}
.btn.ghost{background:#18092a;border-color:var(--line);color:var(--ink-dim);font-weight:600}
.btn:disabled{opacity:.4;cursor:not-allowed}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.warn{font-size:12px;color:#e0a35c;background:#2a1d0c;border:1px solid #5a3f18;border-radius:8px;padding:9px 12px;margin-top:8px}

/* === 시작: 선택 슬롯 === */
.pickslots{display:flex;gap:16px;flex-wrap:wrap;justify-content:center}
.pslot{position:relative;width:134px;aspect-ratio:3/4;border-radius:12px;border:2px dashed var(--line);background:#120724;
  display:flex;align-items:center;justify-content:center;color:var(--ink-faint);font-size:12px;font-weight:700;
  overflow:hidden;transition:box-shadow .2s,border-color .2s}
.pslot .slab{letter-spacing:.06em}
.pslot.p .slab::before{content:"★ ";color:var(--gold)}
.pslot.filled{border-style:solid}
.pslot.filled img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:top center}
.pslot.filled .nm{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:6px 8px;font-size:11px;color:#fff;
  background:linear-gradient(0deg,#000e,#0000)}
.pslot.filled .x{position:absolute;top:4px;right:5px;z-index:3;cursor:pointer;width:21px;height:21px;border-radius:50%;
  background:#000b;color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px}
.pslot.p.filled{border-color:var(--gold-bright);box-shadow:0 0 0 1px var(--gold-deep),0 0 16px 2px rgba(201,162,75,.45)}
.pslot.c.filled{border-color:#7fb6ff;animation:glowpulse 2.1s ease-in-out infinite}
@keyframes glowpulse{
  0%,100%{box-shadow:0 0 0 2px rgba(127,182,255,.5),0 0 14px 3px rgba(96,156,255,.4)}
  50%{box-shadow:0 0 0 2px rgba(170,210,255,.8),0 0 26px 7px rgba(120,175,255,.68)}}

/* === 시작: 팩션 탭 === */
.ftabs{display:flex;gap:7px;flex-wrap:wrap;margin:18px 0 0;justify-content:center}
.ftab{background:#18092a;border:1px solid var(--line);color:var(--ink-dim);padding:7px 13px;border-radius:9px;
  cursor:pointer;font-size:12px;font-weight:700;font-family:inherit}
.ftab:hover{color:var(--ink);border-color:var(--gold-deep)}
.ftab.on{color:var(--gold-bright);border-color:var(--gold-bright);background:#3a2256}
.ftab .ct{opacity:.55;font-weight:400;margin-left:5px}

/* === 시작: 부채꼴 핸드 + 좌우 화살표 === */
.handnav{display:flex;align-items:center;gap:8px}
.harrow{flex:none;width:44px;height:170px;border:1px solid var(--line);background:#18092a;color:var(--gold-bright);
  border-radius:10px;cursor:pointer;font-family:serif;font-size:26px;line-height:1;transition:background .15s,opacity .15s}
.harrow:hover{background:#3a2256;border-color:var(--gold-deep)}
.harrow:disabled{opacity:.22;cursor:default;background:#18092a}
.harrow.hide{visibility:hidden}
.handwrap{position:relative;flex:1;min-width:0;overflow-x:auto;overflow-y:hidden;padding:22px 8px 16px;scroll-behavior:smooth;scrollbar-width:none}
.handwrap::-webkit-scrollbar{display:none}
.hand{display:flex;justify-content:safe center;align-items:flex-end;gap:12px;min-width:min-content}
.fcard{flex:0 0 auto;width:140px;aspect-ratio:3/4;border-radius:12px;overflow:hidden;position:relative;
  cursor:pointer;background:#1f0f2e;border:2px solid transparent;transform-origin:bottom center;
  transition:transform .18s cubic-bezier(.2,.7,.2,1),box-shadow .2s,border-color .2s;
  box-shadow:0 6px 16px rgba(0,0,0,.5);animation:fanin .4s ease backwards}
.fcard img{width:100%;height:100%;object-fit:cover;object-position:top center;display:block}
.fcard .noimg{width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-family:serif;font-size:34px;color:#6e5a8e;background:radial-gradient(circle at 50% 35%,#2a1640,#160a26)}
.fcard .cap{position:absolute;left:0;right:0;bottom:0;padding:5px 7px;font-size:11px;font-weight:700;color:#fff;background:linear-gradient(0deg,#000e,#0000)}
.fcard::after{content:"";position:absolute;inset:0;opacity:0;transition:opacity .2s;
  background:linear-gradient(120deg,transparent 30%,rgba(160,205,255,.25) 50%,transparent 70%)}
.fcard:hover{transform:translateY(-10px) scale(1.05);z-index:30;border-color:#7fb6ff;
  box-shadow:0 14px 30px rgba(0,0,0,.6),0 0 16px 2px rgba(120,175,255,.5)}
.fcard:hover::after{opacity:1}
.fcard.taken{filter:grayscale(.55) brightness(.55)}
.fcard .chk{position:absolute;top:6px;left:6px;z-index:3;width:22px;height:22px;border-radius:50%;background:#7fb6ff;
  color:#0d1518;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:900}
@keyframes fanin{0%{opacity:0;transform:translateY(14px) scale(.9)}100%{opacity:1}}
@media (prefers-reduced-motion:reduce){.fcard{animation:none}.pslot.c.filled{animation:none;box-shadow:0 0 0 2px #7fb6ff}}

/* 모듈 칩 */
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:6px}
.chip{border:1px solid var(--line);background:#18092a;color:var(--ink-dim);padding:7px 12px;border-radius:20px;
  cursor:pointer;font-size:12px;font-weight:600}
.chip:hover{border-color:var(--gold-deep);color:var(--ink)}
.chip.on{background:#4a2e6e;border-color:var(--gold-bright);color:var(--gold-bright)}
.chip.mem{cursor:pointer}
/* 잠긴 세계의 기억 — 사슬·자물쇠 */
.chip.locked{cursor:not-allowed;color:var(--ink-faint);border-style:dashed;border-color:#5a4a72;
  background:repeating-linear-gradient(135deg, rgba(150,140,170,.16) 0 5px, rgba(30,20,45,.16) 5px 11px), #160a26}
.chip.locked .lk{margin-right:6px}
.chip.locked .lt{opacity:.7;text-shadow:0 0 5px rgba(0,0,0,.6)}
.chip.locked:hover{border-color:#5a4a72;color:var(--ink-faint)}

/* 플레이 */
#view-play.active{display:grid;grid-template-columns:1fr 300px;gap:0}
#playmain{display:flex;flex-direction:column;height:100%;min-width:0}
#log{flex:1;overflow:auto;padding:24px 30px;max-width:820px;margin:0 auto;width:100%}
.msg{margin:0 0 18px;animation:fade .4s ease}
@keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.msg.u{text-align:right}
.msg.u .bub{display:inline-block;background:#34194c;border:1px solid var(--line);border-radius:14px 14px 4px 14px;
  padding:9px 14px;color:var(--ink);max-width:78%;text-align:left}
.msg.a .bub{font-family:'Iowan Old Style',Palatino,'Nanum Myeongjo',Georgia,serif;font-size:16px;line-height:1.85;color:#ece2f6}
.msg.a .bub h2,.msg.a .bub h3{font-size:17px;color:var(--gold)}
.msg.a .bub p{margin:.5em 0}
.msg.sys{text-align:center;color:var(--gold-deep);font-size:12px;letter-spacing:.1em}
.msg.chg{text-align:center;color:var(--gold-bright);font-size:12px;letter-spacing:.04em;margin:-6px 0 16px}
.msg.chg::before,.msg.chg::after{content:"";display:inline-block;width:24px;height:1px;background:var(--gold-deep);vertical-align:middle;margin:0 8px;opacity:.6}
/* 하단 패딩에 safe-area-inset-bottom 합산 → 아이폰 홈 인디케이터가 입력바를 가리지 않게 */
#composer{border-top:1px solid var(--line);padding:14px 30px calc(14px + env(safe-area-inset-bottom,0px));background:#1f0f2e}
#composer .inwrap{max-width:820px;margin:0 auto;display:flex;gap:10px;align-items:flex-end}
#userInput{flex:1;resize:none;min-height:46px;max-height:160px}
#choices{max-width:820px;margin:0 auto 8px;display:flex;gap:8px;flex-wrap:wrap}
.choice{background:#18092a;border:1px solid var(--gold-deep);color:var(--gold-bright);padding:8px 14px;border-radius:9px;
  cursor:pointer;font-size:13px;font-family:inherit}
.choice:hover{background:#3a2256}
/* 입력바 액션 (모델 칩 + 빠른 액션) */
#composer .actbar{max-width:820px;margin:0 auto 8px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.mchip{display:inline-flex;align-items:center;gap:7px;font-family:inherit;cursor:pointer;
  background:linear-gradient(180deg,#7a4fb8,#5a338f);border:1px solid var(--gold-deep);color:#f3ecff;
  padding:7px 12px;border-radius:999px;font-size:13px;font-weight:600;box-shadow:var(--shadow)}
.mchip:hover{filter:brightness(1.12)}
.mchip .mchip-ic{display:inline-grid;place-items:center;width:18px;height:18px;border-radius:50%;
  background:#2a0f38;color:var(--gold-bright);font-size:11px}
.mchip .mchip-cv{opacity:.7;font-size:11px}
.qbtn{font-family:inherit;cursor:pointer;background:#18092a;border:1px solid var(--line);color:var(--ink-dim);
  padding:7px 12px;border-radius:999px;font-size:12.5px}
.qbtn:hover{border-color:var(--gold-deep);color:var(--gold-bright);background:#23123a}
/* 모델 카드 리스트 */
.mlist{max-height:300px;overflow:auto;border:1px solid var(--line-soft);border-radius:12px;background:#1b0c2b;margin:2px 0 6px}
.mcard{display:flex;align-items:center;gap:10px;padding:11px 14px;cursor:pointer;border-bottom:1px solid var(--line-soft)}
.mcard:last-child{border-bottom:0}
.mcard:hover{background:#26133c}
.mcard.sel{background:#2c1746}
.mcard .mc-main{flex:1;min-width:0}
.mcard .mc-top{display:flex;align-items:center;gap:8px}
.mcard .mc-top b{color:var(--ink);font-size:14.5px}
.mcard .mc-rec{font-size:10.5px;color:#160a22;background:var(--gold-bright);border-radius:5px;padding:1px 6px;font-weight:700}
.mcard .mc-tag{color:var(--gold);font-size:11.5px;font-weight:600;margin-top:1px}
.mcard .mc-desc{color:var(--ink-faint);font-size:12px;margin-top:3px;line-height:1.4}
.mcard .mc-check{color:var(--gold-bright);font-size:18px;width:20px;text-align:center}
/* 고급(직접 입력) */
.adv{margin:8px 0 4px;border:1px solid var(--line-soft);border-radius:10px;padding:6px 12px;background:#1b0c2b}
.adv>summary{cursor:pointer;color:var(--ink-dim);font-size:13px;padding:4px 0;list-style:none}
.adv>summary::-webkit-details-marker{display:none}
.adv>summary::before{content:'▸ ';color:var(--gold-deep)}
.adv[open]>summary::before{content:'▾ '}

/* 벨벳 패널 광택 */
.card2,.scard,.sdetail,.recap,.mbox,.portrait{box-shadow:var(--shadow),inset 0 1px 0 rgba(222,202,255,.07)}

/* 마법진 로더 + 본문 일괄 표출 */
.loader{display:flex;flex-direction:column;align-items:center;gap:13px;padding:20px 0 10px}
.mcircle{width:112px;height:112px;filter:drop-shadow(0 0 7px rgba(185,140,255,.7))}
.mcircle circle,.mcircle polygon,.mcircle rect{fill:none;stroke:var(--gold-bright);vector-effect:non-scaling-stroke}
.mcircle .r1{transform-origin:50% 50%;animation:spin 9s linear infinite}
.mcircle .r2{transform-origin:50% 50%;animation:spin 13s linear infinite reverse}
.mcircle .pulse{transform-origin:50% 50%;animation:mpulse 2.3s ease-in-out infinite}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes mpulse{0%,100%{opacity:.45}50%{opacity:1}}
.lcap{font-size:11px;letter-spacing:.22em;color:var(--gold-bright);opacity:.85;text-transform:uppercase}
.reveal{animation:reveal .5s ease}
@keyframes reveal{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){.mcircle .r1,.mcircle .r2,.mcircle .pulse{animation:none}.reveal{animation:none}}

/* 우측 미니 스테이터스 */
#rail{border-left:1px solid var(--line);background:#1f0f2e;overflow:auto;padding:16px 14px}
#rail h4{margin:0 0 10px;color:var(--gold);font-size:13px;letter-spacing:.05em}
.mini{display:flex;align-items:center;gap:9px;margin-bottom:10px}
.mini img,.mini .av{width:38px;height:38px;border-radius:8px;object-fit:cover;object-position:top center;flex:none;background:#2a1640}
.mini .av{display:flex;align-items:center;justify-content:center;font-family:serif;color:#6e5a8e}
.mini .nm{font-size:12px;font-weight:700}
.bar{height:7px;border-radius:5px;background:#120724;overflow:hidden;margin-top:3px;border:1px solid #00000055}
.bar i{display:block;height:100%}
.bandtag{font-size:10px;font-weight:700;padding:1px 6px;border-radius:5px;margin-left:6px}

/* 스테이터스 뷰 — 최근 전개 + 마스터-디테일 */
.recap{background:linear-gradient(180deg,var(--panel),var(--panel2));border:1px solid var(--line);border-radius:12px;
  padding:14px 18px;margin-bottom:16px}
.recap h4{margin:0 0 8px;color:var(--gold);font-size:13px;letter-spacing:.06em}
.recap ul{margin:0;padding-left:18px}
.recap li{margin:4px 0;color:var(--ink-dim);font-size:13px;line-height:1.5}
.recap .muted{font-size:12px}
.status-wrap{display:grid;grid-template-columns:268px 1fr;gap:18px;align-items:start}
.slist{display:flex;flex-direction:column;gap:6px;max-height:calc(100vh - 210px);overflow:auto;
  border:1px solid var(--line-soft);border-radius:12px;padding:8px;background:#120724}
.srow{display:flex;align-items:center;gap:10px;padding:7px 8px;border-radius:9px;cursor:pointer;border:1px solid transparent}
.srow:hover{background:#00000040}
.srow.on{background:#3a2256;border-color:var(--gold-deep)}
.srow img,.srow .av{width:40px;height:40px;border-radius:8px;object-fit:cover;object-position:top center;flex:none;background:#2a1640}
.srow .av{display:flex;align-items:center;justify-content:center;font-family:serif;color:#6e5a8e}
.srow .sm{flex:1;min-width:0}
.srow .snm{font-size:13px;font-weight:700;display:flex;align-items:center;gap:6px}
.srow .dot{width:8px;height:8px;border-radius:50%;flex:none}
.sdetail{background:linear-gradient(180deg,var(--panel),var(--panel2));border:1px solid var(--line);border-radius:14px;
  padding:18px;display:flex;gap:18px;min-height:220px}
.sdetail .sp{width:150px;flex:none}
.sdetail .sp img{width:150px;border-radius:12px;object-fit:cover;object-position:top center;background:#2a1640}
.sdetail .sp .av{width:150px;aspect-ratio:3/4;border-radius:12px;display:flex;align-items:center;justify-content:center;font-family:serif;font-size:40px;color:#6e5a8e;background:#2a1640}
.sdetail .sbody{flex:1;min-width:0}
.sdetail h3{margin:0;color:var(--gold-bright);font-size:20px}
.sdetail .en{font-size:12px;color:var(--ink-faint);margin:2px 0 12px}
.relnote{margin-top:12px;font-size:13px;color:var(--ink-dim);border-left:2px solid var(--gold-deep);padding:2px 0 2px 10px}
@media(max-width:760px){.status-wrap{grid-template-columns:1fr}.sdetail{flex-direction:column}}
@media(max-width:640px){
  #topbar{padding:0 12px;gap:8px}
  .navtoggle{display:inline-flex;font-size:17px;line-height:1;padding:6px 11px}
  .brand{font-size:15px}.brand small{display:none}
  #runtag{display:none}
  #btnSettings{font-size:0;padding:7px 10px}
  #btnSettings::before{content:"⚙";font-size:15px}
  /* nav → 좌측 드로어 */
  #nav{position:fixed;top:0;left:0;bottom:0;width:230px;margin:0;flex-direction:column;gap:4px;
    background:linear-gradient(180deg,#2a153e,#1a0c28);border-right:1px solid var(--line);
    padding:64px 12px 16px;transform:translateX(-100%);transition:transform .22s ease;z-index:70;overflow:auto}
  body.nav-open #nav{transform:none}
  #nav .navbtn{width:100%;text-align:left;font-size:15px;padding:11px 14px}
  /* 플레이: 단일 컬럼 + 레일 우측 시트 */
  #view-play.active{grid-template-columns:1fr}
  #log{padding:16px 16px;max-width:none}
  #composer{padding:10px 14px calc(10px + env(safe-area-inset-bottom,0px))}
  #composer .inwrap,#composer .actbar,#choices{max-width:none}
  body.on-play .railtoggle{display:inline-flex;position:fixed;right:14px;bottom:calc(88px + env(safe-area-inset-bottom,0px));z-index:55;
    align-items:center;background:linear-gradient(180deg,#3a1a50,#2a0f38);border:1px solid var(--gold-deep);
    color:var(--gold-bright);border-radius:22px;padding:9px 15px;font-family:inherit;font-size:13px;font-weight:600;cursor:pointer;box-shadow:var(--shadow)}
  #rail{position:fixed;top:0;right:0;bottom:0;width:280px;max-width:84vw;transform:translateX(100%);
    transition:transform .22s ease;z-index:70}
  body.rail-open #rail{transform:none}
  /* 시작 화면 */
  .pad{padding:18px 14px}
  .hero-title{font-size:44px}
  .pslot{width:46%}
  .psn-grid{grid-template-columns:1fr}
  .startset{gap:10px}
  .sitcard{margin:0 0 14px}
  /* 모달 */
  #modal,#impModal,#qlipModal{padding:12px}
  .mbox{padding:18px 16px}
  .qlip-head{flex-wrap:wrap;justify-content:center;text-align:center}
}
.axes{margin-top:10px}
.axline{font-size:11px;color:var(--ink-dim);margin-bottom:7px}
.axline .axhd{display:flex;justify-content:space-between;margin-bottom:2px}
.axline .axn{font-weight:600}
.axline .axv{font-variant-numeric:tabular-nums;color:var(--ink)}
.affnum{font-variant-numeric:tabular-nums;font-size:12px;color:var(--ink-dim);margin-left:auto}
.nmrow{display:flex;align-items:center;gap:8px}

/* 장비 뷰 */
.equip-wrap{display:grid;grid-template-columns:300px 1fr;gap:24px;align-items:start}
.portrait{position:relative;border:1px solid var(--line);border-radius:16px;overflow:hidden;
  background:linear-gradient(180deg,#2a153e,#160a24);box-shadow:var(--shadow)}
.portrait img{width:100%;display:block}
.portrait::after{content:"";position:absolute;left:0;right:0;bottom:0;height:42%;pointer-events:none;
  background:linear-gradient(180deg,transparent 0%,rgba(20,15,9,.55) 55%,#160a24 100%)}
.portrait .av{width:100%;aspect-ratio:3/4;display:flex;align-items:center;justify-content:center;font-family:serif;font-size:54px;color:#6e5a8e}
.pname{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:14px 16px 13px;
  font-family:'Iowan Old Style',Palatino,'Nanum Myeongjo',Georgia,serif;font-size:18px;font-weight:700;color:var(--gold-bright)}
.pname span{display:block;font-size:11px;font-weight:400;color:var(--ink-faint);letter-spacing:.04em;font-style:italic;margin-top:1px}
.inv-tools{display:flex;justify-content:flex-end;margin-bottom:10px}
.it-th{width:36px;height:36px;border-radius:8px;object-fit:cover;object-position:top center;flex:none;background:#2a1640}
.slot{margin-bottom:14px}
.slot .lab{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-deep);margin-bottom:6px}
.item{display:flex;justify-content:space-between;align-items:center;border:1px solid var(--line);border-radius:9px;
  padding:9px 12px;margin-bottom:6px;background:#18092a;cursor:pointer}
.item:hover{border-color:var(--gold-deep)}
.item.on{border-color:var(--gold-bright);background:#34194c}
.item .it-t{font-size:13px;font-weight:600}
.item .it-s{font-size:11px;color:var(--ink-faint)}
.item .eqb{font-size:11px;font-weight:700;color:var(--gold-bright)}

/* 설정 모달 */
#modal,#impModal,#qlipModal{position:fixed;inset:0;background:#000a;display:none;align-items:center;justify-content:center;z-index:200;padding:20px}
#modal.on,#impModal.on,#qlipModal.on{display:flex}
textarea.tin{resize:vertical}
.mbox{background:linear-gradient(180deg,#2a0f38,#20102e);border:1px solid var(--gold-deep);border-radius:16px;
  max-width:480px;width:100%;padding:22px 24px;box-shadow:var(--shadow);max-height:88vh;overflow:auto}
#qlipModal .mbox{max-width:560px}
.mbox h3{margin:0 0 12px;color:var(--gold-bright)}
.close{float:right;cursor:pointer;color:var(--ink-faint);font-size:20px;line-height:1}
/* 토큰 비용 HUD */
.hud{max-width:820px;margin:0 auto 8px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:12px;color:var(--ink-dim)}
.hud .hud-i b{color:var(--gold-bright);font-weight:700}
.hud .hud-sep{color:var(--gold-deep)}
.hud .hud-btn{margin-left:auto;font-size:11.5px;padding:5px 11px}
/* 세피로트 모달 */
.qlip-head{display:flex;gap:16px;align-items:center;margin-bottom:14px}
.donut{width:120px;height:120px;border-radius:50%;flex:none;display:grid;place-items:center;position:relative}
.donut::after{content:"";position:absolute;width:72px;height:72px;border-radius:50%;background:#20102e}
.donut-h{position:relative;z-index:1;text-align:center;line-height:1.15;max-width:66px;overflow:hidden}
.donut-h b{display:block;color:var(--gold-bright);font-size:15px;white-space:nowrap}
.donut-h span{font-size:9.5px;color:var(--ink-faint)}
.qlip-cap{font-size:14px;color:var(--ink)}
.qlist{display:flex;flex-direction:column;gap:10px}
.qrow{display:flex;gap:9px;align-items:flex-start}
.qrow .swatch{width:12px;height:12px;border-radius:3px;flex:none;margin-top:4px}
.qrow .qmain{flex:1;min-width:0;border-bottom:1px solid var(--line-soft);padding-bottom:8px}
.qtop{display:flex;align-items:baseline;gap:6px}
.qtop b{color:var(--ink);font-size:14px}
.qtop .qsub{font-size:11px;color:var(--ink-faint)}
.qtop .qnum{margin-left:auto;color:var(--gold-bright);font-size:13px;font-weight:700}
.qtop .qpct{color:var(--ink-faint);font-size:11px;font-weight:400}
.qsrc{font-size:12px;color:var(--gold);margin-top:2px}
.qwhy{font-size:11.5px;color:var(--ink-faint);margin-top:2px;line-height:1.45}
"""

# ------- JS -------
JS = r"""
'use strict';
const CANON  = JSON.parse(document.getElementById('canon').textContent);
const ASSETS = JSON.parse(document.getElementById('assets').textContent);
const SEED   = JSON.parse(document.getElementById('world').textContent);
window.CANON = CANON;  // 임베드 위키(iframe)가 window.parent.CANON.images 로 이미지 공유

const byId = {}; CANON.characters.forEach(c=>byId[c.id]=c); (CANON.guests||[]).forEach(g=>byId[g.id]=g);
const modById = {}; ASSETS.modules.forEach(m=>modById[m.id]=m);
const bands = ASSETS.bands || [];
const districtKr = {}; (ASSETS.districts||[]).forEach(d=>districtKr[d.key]=d.kr);
const playable = CANON.characters.filter(c=>!c.guest);
const AXIS_KR = {trust:'신뢰', respect:'존중', romance:'연심', bond:'유대', fear:'경계'};
const TYPE_KR = {outfit:'복장', equipment:'장비', item:'아이템', memory:'세계의 기억', accessory:'장신구'};
const SLOT_KR = {outfit:'복장', weapon:'무기', accessory:'장신구'};

// 가져온 모듈(이미지·메타데이터 포함) 영속 — localStorage 'playMods'
function loadExtraMods(){ try{return JSON.parse(localStorage.getItem('playMods')||'[]');}catch(e){return [];} }
function registerMod(m){ modById[m.id]=m; if(!ASSETS.modules.find(x=>x.id===m.id)) ASSETS.modules.push(m); }
loadExtraMods().forEach(registerMod);

/* ============ 토큰·비용 ('클리포트 억지력' = 토큰 1:1) ============ */
// 오프라인 휴리스틱 토큰 추정(한글·CJK ≈ 0.6 tok/char, 그 외 ≈ 0.27). 비율 산출 + usage 폴백용.
function estTokens(s){
  if(!s) return 0; let cjk=0, oth=0;
  for(const ch of String(s)){ const c=ch.codePointAt(0);
    if((c>=0x1100&&c<=0x11FF)||(c>=0x3000&&c<=0x9FFF)||(c>=0xAC00&&c<=0xD7A3)||(c>=0xF900&&c<=0xFAFF)||(c>=0x3040&&c<=0x30FF)) cjk++; else oth++; }
  return Math.max(1, Math.round(cjk*0.6 + oth*0.27));
}
// 모델 단가 (USD / 1M 토큰, 입력/출력 — 2026-06 기준 근사치)
// 주: Gemini 3.x Pro는 >200k 컨텍스트에서 $4/$18 고단가 티어, GPT-5.x는 >272k에서 2×/1.5× 티어가
//     있으나 플레이 규모는 그 미만이라 미적용. flash-lite 키는 flash보다 먼저 둬 접두 오매칭 방지.
const PRICES = {
  'claude-opus-4-8':[5,25], 'claude-sonnet-4-6':[3,15], 'claude-haiku-4-5':[1,5],
  'gemini-3.1-pro':[2,12], 'gemini-3-pro':[2,12],
  'gemini-3.5-flash':[1.5,9], 'gemini-3-flash':[1.5,9],
  'gemini-2.5-pro':[1.25,10], 'gemini-2.5-flash-lite':[0.10,0.40], 'gemini-2.5-flash':[0.30,2.5],
  'gpt-5.5':[5,30], 'gpt-5.4':[2.5,15], 'gpt-5-nano':[0.05,0.40], 'gpt-5-mini':[0.25,2], 'gpt-5':[1.25,10],
  'gpt-4o':[2.5,10], 'gpt-4o-mini':[0.15,0.6], 'mock':[0,0], '_default':[3,15]
};
// 모델 ID는 자유 입력이라 변종(gemini-3.1-pro-preview 등)이 들어옴 → 접두/패밀리 폴백으로 견고화.
function priceOf(model){
  if(!model) return PRICES['_default'];
  if(PRICES[model]) return PRICES[model];
  const m=String(model).toLowerCase();
  for(const k in PRICES){ if(k!=='_default' && m.indexOf(k)===0) return PRICES[k]; }
  if(/gemini-3.*pro/.test(m)) return [2,12];
  if(/gemini-3.*flash/.test(m)) return [1.5,9];
  if(/gpt-5\.5/.test(m)) return [5,30];
  if(/gpt-5\.4/.test(m)) return [2.5,15];
  if(/gpt-5/.test(m)) return [1.25,10];
  return PRICES['_default'];
}
// Gemini usageMetadata → {inTok(풀과금 입력), outTok(후보+사고), cacheRead}
// 출력은 total-prompt 로 산출: candidates가 사고(thinking) 토큰을 포함하든 별도이든 모두 정확.
function geminiUsage(m){
  if(!m) return {inTok:0,outTok:0,cacheRead:0};
  const cc=m.cachedContentTokenCount||0;
  const pt=m.promptTokenCount||0;
  const tt=m.totalTokenCount||0;
  const cand=m.candidatesTokenCount||0, th=m.thoughtsTokenCount||0;
  const out = (tt>pt) ? (tt-pt) : (cand+th);   // 사고 토큰 포함 보장
  return {inTok:Math.max(0,pt-cc), outTok:out, cacheRead:cc};
}
// USD→KRW 환율: 실시간 fetch(무키·CORS), 24h 캐시, 실패 시 기본 1400
let FX = 1400;
(function loadFx(){ try{ const c=JSON.parse(localStorage.getItem('playFx')||'null'); if(c&&c.rate){ FX=c.rate; if(Date.now()-(c.ts||0)<864e5) return; } }catch(e){} refreshFx(); })();
function setFx(r){ if(r&&r>0){ FX=r; try{localStorage.setItem('playFx',JSON.stringify({rate:r,ts:Date.now()}));}catch(e){} try{renderUsage();}catch(e){} } }
function refreshFx(){
  // CORS 허용 무키 엔드포인트(jsdelivr 통화 API) → 실패 시 폴백 → 그래도 실패면 캐시/기본값 유지
  fetch('https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json')
    .then(r=>r.json()).then(j=>{ const r=j&&j.usd&&j.usd.krw; if(r) setFx(r); else throw 0; })
    .catch(()=>fetch('https://open.er-api.com/v6/latest/USD').then(r=>r.json()).then(j=>{ const r=j&&j.rates&&j.rates.KRW; if(r) setFx(r); }).catch(()=>{}));
}
// inTok=풀과금 입력(미캐시). cacheRead≈0.1×·cacheCreate≈1.25× (Anthropic 프롬프트 캐싱 단가).
function cost(inTok,outTok,model,cacheRead,cacheCreate){
  const [pi,po]=priceOf(model||API.model);
  const inUSD=((inTok||0) + (cacheCreate||0)*1.25 + (cacheRead||0)*0.1)/1e6*pi;
  return (inUSD + (outTok||0)/1e6*po)*FX;
}
// 프로바이더별 '싼 모델'(장기기억 요약용). 없으면 현재 모델로 폴백.
const CHEAP_MODEL={anthropic:'claude-haiku-4-5', gemini:'gemini-2.5-flash-lite', openai:'gpt-5-mini'};
function krw(n){ return '₩'+Math.round(n).toLocaleString('ko-KR'); }
function qlip(n){ return Math.round(n).toLocaleString('ko-KR')+' 클리포트 억지력'; }

function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
/* 한글 조사 자동 선택(받침 유무). 한글 음절이 아니면 받침 없는 형태로 폴백 → '김민석(이)가' 방지. */
function hasBatchim(w){ if(!w) return false; const c=w.charCodeAt(w.length-1);
  if(c<0xAC00||c>0xD7A3) return false; return (c-0xAC00)%28!==0; }
function withJosa(w,batchim,plain){ return (w||'')+(hasBatchim(w)?batchim:plain); }
function jEunNeun(w){ return withJosa(w,'은','는'); }   // 은/는
function jIGa(w){ return withJosa(w,'이','가'); }       // 이/가
function jEulReul(w){ return withJosa(w,'을','를'); }   // 을/를
function jWaGwa(w){ return withJosa(w,'과','와'); }     // 과/와
function jEuRo(w){ if(!w) return w; const c=w.charCodeAt(w.length-1);
  const hangul=c>=0xAC00&&c<=0xD7A3, jong=hangul?(c-0xAC00)%28:0;
  return w+((!hangul||jong===0||jong===8)?'로':'으로'); }   // (으)로: 받침없음·ㄹ → 로
function img(prefix,kind){const im=CANON.images[prefix];if(!im)return null;return kind==='m'?(im.m||im.d):(im.d||im.m);}
function mdRender(src){
  if(!src) return '';
  const lines=src.replace(/\r/g,'').split('\n'); let html='',ul=false;
  const inl=t=>esc(t).replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>').replace(/(^|[^*])\*([^*]+?)\*/g,'$1<em>$2</em>');
  for(let raw of lines){
    if(!raw.trim()){ if(ul){html+='</ul>';ul=false;} continue; }
    let m;
    if(m=raw.match(/^(#{2,4})\s*(.+)$/)){ if(ul){html+='</ul>';ul=false;} html+='<h3>'+inl(m[2])+'</h3>'; continue; }
    if(m=raw.match(/^\s*[-*]\s+(.+)$/)){ if(!ul){html+='<ul>';ul=true;} html+='<li>'+inl(m[1])+'</li>'; continue; }
    if(ul){html+='</ul>';ul=false;} html+='<p>'+inl(raw.trim())+'</p>';
  }
  if(ul)html+='</ul>'; return html;
}

/* ============ 설정 (API, BYO 키) ============ */
const PRESETS = {
  anthropic:{ep:'https://api.anthropic.com/v1/messages', model:'claude-opus-4-8'},
  openai:{ep:'https://api.openai.com/v1/chat/completions', model:'gpt-5.5'},
  gemini:{ep:'https://generativelanguage.googleapis.com/v1beta/models', model:'gemini-3.1-pro'},
  mock:{ep:'', model:'mock'}
};
// 추천 모델 카탈로그 (실제 사용 가능한 ID만; 그 외는 '직접 입력')
const MODELS = [
  {id:'claude-opus-4-8', label:'Claude Opus 4.8', provider:'anthropic', desc:'극한의 몰입감과 창의적 서사력 — 최신 플래그십', rec:true},
  {id:'claude-sonnet-4-6', label:'Claude Sonnet 4.6', provider:'anthropic', desc:'균형 잡힌 속도와 품질'},
  {id:'claude-haiku-4-5', label:'Claude Haiku 4.5', provider:'anthropic', desc:'빠르고 가벼운 응답'},
  {id:'gemini-3.1-pro', label:'Gemini 3.1 Pro', provider:'gemini', desc:'구글 최신 플래그십 · 강력한 추론', rec:true},
  {id:'gemini-3.5-flash', label:'Gemini 3.5 Flash', provider:'gemini', desc:'최신 고속 사고형 모델'},
  {id:'gemini-2.5-pro', label:'Gemini 2.5 Pro', provider:'gemini', desc:'고성능 · 장문 대화에 적합'},
  {id:'gemini-2.5-flash', label:'Gemini 2.5 Flash', provider:'gemini', desc:'빠른 응답'},
  {id:'gpt-5.5', label:'GPT-5.5', provider:'openai', desc:'OpenAI 최신 프런티어'},
  {id:'gpt-5.4', label:'GPT-5.4', provider:'openai', desc:'균형형 고품질'},
  {id:'gpt-5-mini', label:'GPT-5 mini', provider:'openai', desc:'빠르고 저렴'},
  {id:'mock', label:'환영(幻影) · 시연', provider:'mock', desc:'키 없이 흐름 체험'},
];
const PROVIDER_KR = {anthropic:'Anthropic · Claude', openai:'OpenAI 호환', gemini:'Google Gemini', mock:'시연'};
function modelMeta(id){ return MODELS.find(m=>m.id===id)||null; }
function shortModelLabel(){ const m=modelMeta(API.model); if(m) return m.label.replace(/^환영.*/,'시연').replace('Claude ','').replace('Gemini ','Gemini '); return API.model||'모델 선택'; }
let API = {provider:'mock', endpoint:'', model:'mock', key:'', keys:{}};
try{ const s=JSON.parse(localStorage.getItem('playApi')||'null'); if(s) API=s; }catch(e){}
if(!API.keys){ API.keys={}; if(API.key && API.provider && API.provider!=='mock') API.keys[API.provider]=API.key; }  // 구형 마이그레이션
function saveApi(){ localStorage.setItem('playApi', JSON.stringify(API)); }

/* ============ WorldState 엔진 ============ */
let W = null;          // 현재 월드
let convo = [];        // [{role:'user'|'assistant', text}]
const SAVEKEY='playSaves';
const MEM_KEEP=8;      // 최근 메시지는 verbatim 전송(헤세드/게부라) — 약 4턴 즉시 맥락 보존
const MEM_BATCH=6;     // 윈도 밖 누적이 이만큼 쌓이면 장기기억으로 요약(호드)
const PERSONA_KEY='playPersonas';   // 재사용(공용) 페르소나 라이브러리
const TONES=['일상','임무','위기'];
function loadPersonas(){ try{ const v=JSON.parse(localStorage.getItem(PERSONA_KEY)||'[]'); return Array.isArray(v)?v:[]; }catch(e){ return []; } }
function savePersona(p){ const list=loadPersonas(); if(!p.id)p.id='ps-'+Date.now().toString(36); const i=list.findIndex(x=>x.id===p.id); if(i>=0)list[i]=p; else list.push(p); localStorage.setItem(PERSONA_KEY,JSON.stringify(list)); return p; }
function deletePersona(id){ localStorage.setItem(PERSONA_KEY, JSON.stringify(loadPersonas().filter(p=>p.id!==id))); }
function districtKrOf(key){ const d=(ASSETS.districts||[]).find(x=>x.key===key); return d?d.kr:key; }
// 페르소나 → LLM 주입 텍스트(별명은 미주입 — 플레이어 참고용)
function personaDossier(ps){
  const meta=[]; if(ps.age)meta.push(String(ps.age).replace(/세$/,'')+'세'); if(ps.gender)meta.push(ps.gender);
  return '■ '+(ps.name||'당신')+(meta.length?(' [ '+meta.join(' · ')+' ]'):'')+'\n'+(ps.detail||'');
}
function youName(){ return W.meta.persona? (W.meta.persona.name||'당신') : ((byId[W.meta.protagonist]||{}).title||'당신'); }

function loadSaves(){ try{return JSON.parse(localStorage.getItem(SAVEKEY)||'{}');}catch(e){return {};} }
function writeSaves(o){ localStorage.setItem(SAVEKEY, JSON.stringify(o)); }

// 세계의 기억 전역 해금 원장 (회차 간 영속). 기본=잠김.
function loadUnlockedMem(){
  let v=null; try{ v=JSON.parse(localStorage.getItem('playUnlockedMem')||'null'); }catch(e){}
  if(!Array.isArray(v)){
    // 테스트 기본값: 첫 세계의 기억 1개를 해금된 상태로(1회차 완료·시간회귀 설정)
    const first=(ASSETS.modules.find(m=>m.type==='memory')||{}).id;
    v=first?[first]:[];
    localStorage.setItem('playUnlockedMem', JSON.stringify(v));
  }
  return v;
}
function unlockMem(id){ const v=loadUnlockedMem(); if(id&&!v.includes(id)){ v.push(id); localStorage.setItem('playUnlockedMem', JSON.stringify(v)); } }

function clone(o){ return JSON.parse(JSON.stringify(o)); }
function getRef(path){
  const parts=path.split('.'); let o=W;
  for(let i=0;i<parts.length-1;i++){ if(o==null)return [null,null]; o=o[parts[i]]; }
  return [o, parts[parts.length-1]];
}
function getPath(path){ const [o,k]=getRef(path); return o?o[k]:undefined; }
function ensureAffinity(id){ if(!W.affinity[id]) W.affinity[id]={value:0,band:bandOf(0).id,axes:{}}; return W.affinity[id]; }

function bandOf(v){ for(const b of bands){ if(v>=b.min && v<=b.max) return b; } return bands[2]||{id:'neutral',label:'중립',color:'#b6a784',directive:''}; }
function clampFlag(key,val){
  const def=(ASSETS.flags||[]).find(f=>f.key===key);
  if(def && def.type==='number'){ if(def.min!=null)val=Math.max(def.min,val); if(def.max!=null)val=Math.min(def.max,val); }
  return val;
}
function evalCond(c){
  if(!c) return true;
  let v=getPath(c.path); const t=c.value;
  switch(c.op){
    case 'eq':return v===t; case 'ne':return v!==t;
    case 'gt':return v>t; case 'gte':return v>=t; case 'lt':return v<t; case 'lte':return v<=t;
    case 'in':return Array.isArray(t)&&t.includes(v);
    case 'nin':return Array.isArray(t)&&!t.includes(v);
    case 'has':return Array.isArray(v)&&v.includes(t);
    default:return false;
  }
}
function applyDelta(d){
  // affinity 자동 생성
  if(d.path.startsWith('affinity.')){ const id=d.path.split('.')[1]; ensureAffinity(id); }
  const [o,k]=getRef(d.path); if(!o) return;
  let cur=o[k];
  switch(d.op){
    case 'set': o[k]=d.value; break;
    case 'inc': o[k]=(typeof cur==='number'?cur:0)+d.value; break;
    case 'dec': o[k]=(typeof cur==='number'?cur:0)-d.value; break;
    case 'toggle': o[k]=!cur; break;
    case 'push': if(!Array.isArray(cur))o[k]=cur=[]; if(!cur.includes(d.value))cur.push(d.value); break;
    case 'pull': if(Array.isArray(cur)) o[k]=cur.filter(x=>x!==d.value); break;
    default: o[k]=d.value;
  }
  // 범위 클램프
  if(/^affinity\.[^.]+\.value$/.test(d.path)) o[k]=Math.max(-100,Math.min(100,o[k]));
  if(/^affinity\.[^.]+\.axes\./.test(d.path)) o[k]=Math.max(-100,Math.min(100,o[k]));
  if(/^territory\.[^.]+\.stability$/.test(d.path)) o[k]=Math.max(0,Math.min(100,o[k]));
  if(d.path.startsWith('flags.')){ const key=d.path.slice(6); o[k]=clampFlag(key,o[k]); }
}
function recomputeBands(){ for(const id in W.affinity){ const a=W.affinity[id]; a.band=bandOf(a.value).id; } }
function activeModules(){
  return (W.modules.equipped||[]).map(id=>modById[id]).filter(Boolean)
    .filter(m=>(m.requires||[]).every(evalCond));
}
function bandLabelOf(id){ return (bands.find(b=>b.id===id)||{}).label||id; }
function mutate(deltas){
  const beforeBand={}; for(const id in W.affinity) beforeBand[id]=W.affinity[id].band;
  for(const d of deltas){ try{ applyDelta(d); W.log.push(Object.assign({turn:W.meta.turn},d)); }catch(e){} }
  recomputeBands();
  const changes=[];   // 밴드 전이(질적 변화)만 — 토스트·메모리용
  for(const id in W.affinity){ const ob=beforeBand[id], nb=W.affinity[id].band; const c=byId[id];
    if(c && ob && ob!==nb) changes.push({id, title:c.title, from:bandLabelOf(ob), to:bandLabelOf(nb)}); }
  W.meta.turn++;
  return changes;
}
function issueMemories(){
  const got=[];
  for(const r of (ASSETS.issue||[])){
    if(evalCond(r.when)){
      unlockMem(r.grants);   // 전역 원장에 영속 → 다음 회차 시작 화면에서 해금
      if(!W.modules.unlocked.includes(r.grants)){
        W.modules.unlocked.push(r.grants); if(!W.memory.includes(r.grants))W.memory.push(r.grants); got.push(r.grants);
      }
    }
  }
  return got;
}

/* 컨텍스트 조립 (상태 -> 시스템 프롬프트) */
function cleanRaw(raw){
  if(!raw) return '';
  return raw
    .replace(/!\[[^\]]*\]\([^)]*\)/g,'')      // 이미지 마크다운 제거
    .replace(/<img[^>]*>/gi,'')               // HTML 이미지 제거
    .replace(/\n{3,}/g,'\n\n')                // 빈 줄 축약
    .trim();
}
function charDossier(c){
  const bits=[c.title]; if(c.nameEn)bits.push('('+c.nameEn+')');
  const meta=[]; if(c.factionLabel)meta.push(c.factionLabel); if(c.rankLabel)meta.push(c.rankLabel);
  if(c.districtKr)meta.push(c.districtKr); if(c.generation)meta.push(c.generation);
  let head='■ '+bits.join(' '); if(meta.length)head+=' [ '+meta.join(' · ')+' ]';
  const body=cleanRaw(c.raw);
  if(body) return head+'\n'+body;
  // 폴백: raw 없음
  let s=head;
  if(c.personality)s+='\n성격: '+c.personality;
  if(c.tagline)s+='\n요약: '+c.tagline;
  return s;
}
/* 최근 대화에 등장한 캐논 인물 자동 감지 (주인공·동행 제외, 최대 4) */
function detectSceneChars(excludeIds){
  const ex=new Set(excludeIds||[]);
  const recent=(convo||[]).slice(-6).map(m=>m.text||'').join('\n');
  if(!recent.trim()) return [];
  const hits=[];
  for(const id in byId){
    if(ex.has(id)) continue;
    const c=byId[id]; if(!c) continue;
    const t=c.title||''; const en=c.nameEn||'';
    if((t&&t.length>=2&&recent.includes(t))||(en&&en.length>=3&&recent.includes(en))){
      // 마지막 등장 위치로 최신 우선 정렬
      hits.push({id, pos:Math.max(recent.lastIndexOf(t), en?recent.lastIndexOf(en):-1)});
    }
  }
  hits.sort((a,b)=>b.pos-a.pos);
  return hits.slice(0,4).map(h=>h.id);
}
/* ---- 로어(네짜) RAG-lite: 장면 단서로 관련 로어 문서 선별 ---- */
function loreKeys(doc){   // keys는 RisuAI 콤마 구분 문자열(또는 배열) — 토큰화
  const k=doc&&doc.keys;
  if(Array.isArray(k)) return k.filter(x=>x&&String(x).length>=2);
  if(typeof k==='string') return k.split(/[,\n;·|/]+/).map(s=>s.trim()).filter(s=>s.length>=2);
  return [];
}
function loreScore(doc, hay){
  let s=0;
  loreKeys(doc).forEach(k=>{ if(hay.includes(String(k).toLowerCase()))s+=2; });
  const t=(doc.title||''); if(t&&t.length>=2&&hay.includes(t.toLowerCase()))s+=1;
  return s;
}
function loreById(id){ return (CANON.lore||[]).find(d=>d.id===id)||null; }
function loreEntry(d){ const sm=d.summary||d.raw||''; return sm?('■ '+(d.title||'')+'\n'+sm):''; }
function matchSceneLore(coreId, maxN){
  const lore=(CANON.lore||[]); if(!lore.length) return [];
  let hay=((convo||[]).slice(-4).map(m=>m.text||'').join('\n'));
  [W.meta.protagonist].concat(W.meta.companions||[]).forEach(id=>{ const c=byId[id]; if(c)hay+=' '+(c.title||'')+' '+(c.nameEn||''); });
  (ASSETS.flags||[]).forEach(f=>{ if(W.flags[f.key])hay+=' '+(f.label||''); });
  hay=hay.toLowerCase();
  return lore.filter(d=>d.id!==coreId).map(d=>({d,s:loreScore(d,hay)})).filter(x=>x.s>0)
    .sort((a,b)=>b.s-a.s).slice(0,maxN||2).map(x=>x.d);
}
let PROMPT_SEGS={};  // 세피로트 분해용: 카테고리별 주입 텍스트
// assembleContext: {text, stable, volatile} 반환. stable=회차 불변(캐시 대상), volatile=턴 가변.
// dossier·규칙 바이트는 그대로 유지하고 재정렬 없음 — 안정 prefix 끝에만 캐시 breakpoint.
function assembleContext(){
  const STA=[], VOL=[]; PROMPT_SEGS={};
  const seg=(cat,txt,stable)=>{ (stable?STA:VOL).push(txt); PROMPT_SEGS[cat]=(PROMPT_SEGS[cat]||'')+txt+'\n'; };
  seg('binah','[역할] 당신은 현대 일본 배경 마법소녀 세계관의 라이트노벨을 실시간으로 써 내려가는 작가 겸 게임마스터다. 빠른 답이 미덕이 아니다 — 설정·인물·직전 맥락을 충분히 읽고 한 글자씩 써 내려간다.',1);
  seg('binah','[문체] 라이트노벨 산문체. 서술(나레이션)은 반드시 현재형 평어체 종결("~다/~ㄴ다/~았다·었다")로 쓴다. 격식체(\'~합니다/~입니다/~습니다\')로 서술하지 마라 — 격식체는 그렇게 말하는 캐릭터의 대사 안에서만. (예: 서술 "문이 쾅 열린다. 시로네의 어깨가 흠칫 튄다." ↔ 대사 "알겠습니다, 선배.") 무미건조한 보고형 묘사("그녀가 카드를 내밀었다") 금지 — 같은 사실도 시점 인물의 감각·태도가 묻어나게 쓴다. 문장 길이를 의도적으로 변주한다: 긴장엔 짧게 끊고, 정적엔 길고 유려하게.',1);
  seg('binah','[묘사] 말하지 말고 보여줘라. "놀랐다/긴장했다/기뻤다"라고 쓰지 말고 반응으로 — 숨을 멈추고, 시선을 피하고, 손끝이 떨리고, 발걸음이 가벼워진다. 빛·소리·냄새·온도·촉감 같은 오감과 미세한 몸짓, 짧은 내면 독백을 섞어 생생하게. 의성어·의태어를 자연스럽게 녹인다. 설정·정보는 인포덤프 대신 환경·대사·행동에 녹여 드러낸다. 한 번 묘사한 것은 변하지 않는 한 다시 묘사하지 않고, 변했으면 분명히 다시 묘사한다.',1);
  seg('binah','[대사] 이야기는 대사가 끌고 간다 — 묘사보다 대사 비중을 높게 둔다. 각 인물에게 캐논대로 고유한 말투(존댓말/반말·방언·1인칭·말버릇·문장부호 습관)를 주고 끝까지 보존한다. 실제 사람이 말하듯 짧고 자연스러운 리듬으로, 말줄임표·침묵으로 감정을 싣는다. 일상 대화에 전문용어를 남발하지 마라. 관계는 말투(격식↔반말, 끊고 들어옴↔기다림)로 드러낸다.',1);
  seg('binah','[금지] 번역체 사슬을 끊어라 — "단순한 ~가 아니었다", "A가 아니었다. B였다.", "더 이상 ~가 아니었다", "~일 뿐이었다", "그저·단지" 남발은 모두 금지. 번역투(~를 통해/~에 의해), 이중 피동(~되어진다), 헤지 남발(~인 듯하다)도 금지. 메타 복선("이것은 시작에 불과했다", "그들은 아직 몰랐다") 금지 — 현재에 집중. 직전 응답에 나온 문장·묘사 표현을 그대로 반복하지 마라. 애니풍 과장·주인공 버프·인과 비틀기 금지. 일본식 성-이름 순 유지.',1);
  seg('binah','[인물] 프로필은 작업지시서가 아니다 — 인물은 시트에 안 적힌 일도 한다. 체크리스트식 연기 금지. 성격을 나레이터가 설명하지 말고, 작은 반응에서 큰 반응으로 행동·대사를 통해 드러낸다. 반복되는 상호작용으로 인물은 학습하고 변한다(첫 반응 → 적응 → 익숙해짐).',1);
  seg('binah','[시점·진행] 2인칭("당신") 시점. 시점 인물이 알 수 없는 것은 서술도 모른다 — 불확실하면 추측형으로 쓴다. 응답은 2~4문단. 사건은 당신의 상호작용으로 점진적으로 전개한다 — 급작스런 새 인물·사건을 억지로 밀어넣지 마라. 매 턴을 \'어떻게 하시겠습니까?\'·\'당신의 선택은?\' 같은 메타 질문이나 선택지 나열로 닫지 마라. 장면을 여운이나 긴장으로 자연스럽게 멈춰 플레이어가 다음 행동을 이어 쓰게 둔다.',1);
  seg('binah','[표기] 한국어 우선. 고유명사·기술명은 처음 등장할 때만 한자/원어를 괄호로 가볍게 병기(예: 교쿠로(玉露), 적월). 매번 병기하지 말 것.',1);
  seg('binah','\n[등장인물 캐논] 아래 프로필의 말투·성격·전투 스타일·관계를 충실히 반영하되, 체크리스트처럼 나열하지 말고 장면에 자연스럽게 녹여라.',1);
  const p=byId[W.meta.protagonist];
  if(p){ seg('tiphereth','\n[주인공]\n'+charDossier(p),1); }       // dossier 원문 verbatim — 캐시 대상
  else if(W.meta.persona){ seg('tiphereth','\n[당신(시점 인물)]\n'+personaDossier(W.meta.persona),1); }
  const compIds=(W.meta.companions||[]).filter(id=>byId[id]);
  if(compIds.length){ seg('keter','\n[동행 인물]\n'+compIds.map(id=>charDossier(byId[id])).join('\n\n'),1); }
  // 코어 로어(세계 규칙 근간) — 회차 불변 → 캐시 블록(stable)에 항상 주입
  const core=loreById(CANON.coreLoreId); const coreTxt=core?loreEntry(core):'';
  if(coreTxt){ seg('netzach','\n[세계 로어 — 근간]\n'+coreTxt,1); }
  // 최근 장면에 등장한 비동행 캐논 인물 자동 주입 (가변)
  const sceneIds=detectSceneChars([W.meta.protagonist].concat(compIds));
  if(sceneIds.length){ seg('keter','\n[현재 장면 등장 인물]\n'+sceneIds.map(id=>charDossier(byId[id])).join('\n\n')); }
  // 호감도 밴드 행동 지시
  const af=[];
  for(const id in W.affinity){ const c=byId[id]; if(!c)continue; const b=bandOf(W.affinity[id].value);
    af.push('- '+c.title+' ('+b.label+'): '+b.directive); }
  if(af.length){ seg('hod','\n[인물별 현재 태도(호감도)]\n'+af.join('\n')); }
  // 장기 기억(요약된 먼 기억) — 호드. 최근 대화는 messages(헤세드/게부라)로 별도 전송.
  if(W.summary&&W.summary.trim()){ seg('hod','\n[장기 기억 — 지난 전개 요약]\n'+W.summary.trim()); }
  if(W.changeLog&&W.changeLog.length){ seg('hod','\n[최근 관계 변화]\n'+W.changeLog.slice(-5).map(x=>'- '+x.note).join('\n')); }
  // 활성 모듈 서사 지시
  const md=[]; activeModules().forEach(m=>(m.effects.narrative||[]).forEach(n=>md.push('- '+n)));
  if(md.length){ seg('yesod','\n[현재 장착/효과]\n'+md.join('\n')); }
  // 장면 매칭 로어(가변) — 키워드 적중 상위 1~2개 요약
  const scLore=matchSceneLore(CANON.coreLoreId,2).map(loreEntry).filter(Boolean);
  if(scLore.length){ seg('netzach','\n[관련 로어]\n'+scLore.join('\n\n')); }
  // 영역/플래그
  const fl=[];
  (ASSETS.flags||[]).forEach(f=>{ const v=W.flags[f.key]; if(v===true)fl.push(f.label); else if(typeof v==='number'&&v>0)fl.push(f.label+'='+v); });
  if(fl.length) seg('netzach','\n[세계 상태] '+fl.join(' · '));
  if(W.meta.start&&W.meta.start.districtKey){ const dk=W.meta.start.districtKey; const t=(W.territory||{})[dk]||{};
    seg('netzach','\n[현재 위치] '+districtKrOf(dk)+(t.sealed?' (봉인 지역)':'')+(t.stability!=null?(' · 안정도 '+t.stability):'')+(W.meta.start.tone?(' · 분위기 '+W.meta.start.tone):'')); }
  // 상태 델타 프로토콜 (가변부 뒤 — 순서 보존, 작아서 캐시 제외 영향 미미)
  const ex=(W.meta.companions[0]||'char-13');
  seg('malkuth','\n[상태 반영 — 필수] 호감·관계·세계 상태가 조금이라도 움직였다면 그 변화를 먼저 *장면 안에서* 인물의 태도·반응으로 드러내라(수치는 노출 금지). 그리고 응답 맨 끝에 아래 코드펜스를 **항상 정확히 한 번** 붙여라 — 바뀐 게 없으면 빈 배열 `[]`:');
  seg('malkuth','```state');
  seg('malkuth','[{"path":"affinity.'+ex+'.value","op":"inc","value":5},{"path":"affinity.'+ex+'.axes.trust","op":"inc","value":3}]');
  seg('malkuth','```');
  seg('malkuth','허용 path: affinity.<charId>.value(-100~100), affinity.<charId>.axes.<trust|respect|romance>, flags.<키>(토글/증감), territory.<지구>.stability. op: set|inc|dec|toggle. 작은 호의·신뢰·반감도 +3~8로 반영하라. 코드펜스는 독자에게 보이지 않으며, ```json 등 다른 라벨을 쓰지 마라.');
  const stable=STA.join('\n'), volatile=VOL.join('\n');
  return {text: stable+'\n'+volatile, stable: stable, volatile: volatile};
}
// 세피로트 노드 정의(표시 순서·색·실제 출처 라벨·비유)
const SEPHIROT = [
  {key:'keter', name:'케테르 & 호크마', sub:'왕관·지혜', src:'등장인물 원본 — 동행/장면 프로필', color:'#e0913f', why:'모든 것이 시작되는 무한의 원천. 세계관과 인물의 방향성을 결정하는 절대적 근간.'},
  {key:'binah', name:'비나', sub:'이해', src:'시스템 프롬프트 — 문체·서사 규칙', color:'#9bb7e8', why:'상위 에너지를 구체적 형태·구조로 빚는 이성. 설정을 실행 가능한 규칙으로 구조화한다.'},
  {key:'hesed', name:'헤세드', sub:'자비', src:'최근 대화 · 당신의 입력', color:'#e87aa6', why:'끊임없이 확장되는 상호작용의 흐름. 유저가 더해가는 맥락.'},
  {key:'gevurah', name:'게부라', sub:'엄격·힘', src:'최근 대화 · 서사 응답 누적', color:'#d2705a', why:'콘텍스트를 제한·조율하는 힘. 누적된 서사가 현재를 묶는다.'},
  {key:'tiphereth', name:'티페리트', sub:'조화', src:'페르소나 — 주인공 프로필', color:'#f0d060', why:'나무 정중앙의 자아(Ego). 정체성의 중심 축을 잡는 페르소나.'},
  {key:'netzach', name:'네짜흐', sub:'영원', src:'로어 — 세계 상태·영역', color:'#a98be6', why:'반복 참조되는 집단적 기억과 신화. 변하지 않는 설정의 창고.'},
  {key:'hod', name:'호드', sub:'영광', src:'장기 기억 — 호감도·세계의 기억', color:'#5fc0d6', why:'정보를 기록·보존·분석하는 내적 메커니즘. 관계와 기억의 논리.'},
  {key:'yesod', name:'예소드', sub:'기초', src:'캐릭터 — 장착/효과 모듈', color:'#8fd0a8', why:'현실로 출력되기 직전의 아스트랄 통로. 인격의 형태를 갖추는 필터.'},
  {key:'malkuth', name:'말쿠트', sub:'왕국', src:'생성 가이던스 — 상태 델타', color:'#9a8eb8', why:'모든 연산이 한 줄의 텍스트로 물질화되는 현실. 최종 매듭.'},
];

/* 시작 지역 자동 도출(페르소나는 캐논 지역 없음 → 동행 지역, 없으면 Tokyo) */
function deriveStartDistrict(protagId, comps){
  const cand=[protagId].concat(comps||[]).map(id=>byId[id]).filter(Boolean).map(c=>c.districtNorm).filter(Boolean);
  return cand[0]||'Tokyo';
}
/* 새 회차 시작. opts={persona, startDistrict, tone}. persona 모드면 protagId=null. */
function newRun(protagId, companionIds, memoryIds, opts){
  opts=opts||{};
  W = clone(SEED);
  W.meta.saveId = 'run-'+Date.now().toString(36);
  W.meta.protagonist = protagId||null;
  W.meta.persona = opts.persona||null;          // 커스텀 페르소나(없으면 캐논 주인공)
  W.meta.companions = companionIds.slice();
  W.meta.ngPlusCount = memoryIds.length?1:0;
  W.meta.start = {districtKey: opts.startDistrict || deriveStartDistrict(protagId, companionIds), tone: opts.tone || '일상'};
  W.meta.prologueDone = false;
  // 호감도 시드: 캐논 주인공의 관계(페르소나 모드면 생략)
  const p=byId[protagId];
  if(p)(p.relationships||[]).forEach(r=>{ if(r.targetId && byId[r.targetId]){
    const base=ASSETS.seedByRelType[r.type]; if(base!=null){ ensureAffinity(r.targetId).value=base; } }});
  companionIds.forEach(id=>{ const a=ensureAffinity(id); if(a.value<20)a.value=35; });
  recomputeBands();
  // 인벤토리: 주인공 소유 모듈 + 기억 토큰
  const owned=ASSETS.modules.filter(m=>m.ownedBy===protagId).map(m=>m.id);
  W.inventory.owned = owned.concat(memoryIds);
  W.modules.unlocked = memoryIds.slice();
  W.memory = memoryIds.slice();
  // 기본 장착
  const cas=owned.find(id=>id==='outfit-'+protagId+'-casual');
  const wp=owned.find(id=>id==='weapon-'+protagId+'-staff');
  W.inventory.equipped={outfit:cas||null, weapon:wp||null, accessory:null};
  W.modules.equipped=[cas,wp].filter(Boolean).concat(memoryIds);
  W.recap=[];
  W.summary='';        // 장기기억 누적 요약(호드)
  W.summaryUpto=0;     // 요약 완료된 convo 선두 메시지 수
  W.changeLog=[];      // 밴드 전이 등 관계 변화 이벤트(호드 주입·메모리)
  W.usage={runIn:0,runOut:0,runKRW:0,turns:0};
  convo=[];
  saveRun();
}
function saveRun(){ if(!W)return; const s=loadSaves(); s[W.meta.saveId]={world:W, convo:convo, ts:Date.now(),
  name:(byId[W.meta.protagonist]||{}).title||'?'}; writeSaves(s); }
function loadRun(id){ const s=loadSaves(); if(!s[id])return false; W=s[id].world; convo=s[id].convo||[];
  if(W.summary==null)W.summary=''; if(W.summaryUpto==null)W.summaryUpto=0; if(!W.changeLog)W.changeLog=[];
  if(W.meta.persona===undefined)W.meta.persona=null;
  if(!W.meta.start)W.meta.start={districtKey:deriveStartDistrict(W.meta.protagonist,W.meta.companions),tone:'일상'};
  if(W.meta.prologueDone==null)W.meta.prologueDone=true;   // 옛 세이브: 프롤로그 이미 지난 것으로 간주
  return true; }

/* ============ LLM 어댑터 (BYO 키, 스트리밍) ============ */
async function callLLM(system, history, onTok){
  // system: 문자열 또는 {text, stable, volatile}. anthropic은 stable을 cache_control로 분리.
  const sysText=(typeof system==='string')?system:((system&&system.text)||'');
  const sysStable=(system&&typeof system==='object')?system.stable:null;
  const sysVol=(system&&typeof system==='object')?system.volatile:'';
  if(API.provider==='mock') return mockLLM(sysText,history,onTok);
  const ep=API.endpoint||PRESETS[API.provider].ep;
  let url=ep, headers={'Content-Type':'application/json'}, body;
  if(API.provider==='openai'){
    headers['Authorization']='Bearer '+API.key;
    body={model:API.model,stream:true,stream_options:{include_usage:true},messages:[{role:'system',content:sysText}].concat(history.map(m=>({role:m.role,content:m.text})))};
  } else if(API.provider==='anthropic'){
    headers['x-api-key']=API.key; headers['anthropic-version']='2023-06-01';
    headers['anthropic-dangerous-direct-browser-access']='true';
    // 안정 prefix(규칙+프로필+코어로어)에 ephemeral 캐시 breakpoint; 변동부는 캐시 밖.
    let sysBody;
    if(sysStable){
      sysBody=[{type:'text',text:sysStable,cache_control:{type:'ephemeral'}}];
      if(sysVol&&sysVol.trim()) sysBody.push({type:'text',text:sysVol});
    } else { sysBody=sysText; }
    body={model:API.model,max_tokens:4096,system:sysBody,stream:true,messages:history.map(m=>({role:m.role,content:m.text}))};
  } else if(API.provider==='gemini'){
    url=ep+'/'+API.model+':streamGenerateContent?alt=sse&key='+encodeURIComponent(API.key);
    body={systemInstruction:{parts:[{text:sysText}]},
      contents:history.map(m=>({role:m.role==='assistant'?'model':'user',parts:[{text:m.text}]}))};
  }
  const res=await fetch(url,{method:'POST',headers,body:JSON.stringify(body)});
  if(!res.ok){ const t=await res.text().catch(()=>''); throw new Error('HTTP '+res.status+' '+t.slice(0,300)); }
  const reader=res.body.getReader(); const dec=new TextDecoder(); let buf='';
  const usage={inTok:0, outTok:0, cacheRead:0, cacheCreate:0};
  while(true){
    const {value,done}=await reader.read(); if(done)break;
    buf+=dec.decode(value,{stream:true});
    let idx;
    while((idx=buf.indexOf('\n'))>=0){
      let line=buf.slice(0,idx); buf=buf.slice(idx+1); line=line.trim();
      if(!line.startsWith('data:'))continue;
      const data=line.slice(5).trim();
      if(data==='[DONE]')continue;
      let obj; try{obj=JSON.parse(data);}catch(e){continue;}
      const t=extractTok(obj); if(t)onTok(t);
      grabUsage(obj, usage);
    }
  }
  return usage;
}
function extractTok(o){
  if(API.provider==='openai'){ try{return (o.choices&&o.choices[0]&&o.choices[0].delta.content)||'';}catch(e){return '';} }
  if(API.provider==='anthropic'){ if(o.type==='content_block_delta'&&o.delta&&o.delta.type==='text_delta')return o.delta.text; return ''; }
  if(API.provider==='gemini'){ try{return o.candidates[0].content.parts.map(p=>p.text||'').join('');}catch(e){return '';} }
  return '';
}
// 스트림에서 토큰 usage 수집(프로바이더별)
function grabUsage(o, u){
  try{
    if(API.provider==='openai'){ if(o.usage){ u.inTok=o.usage.prompt_tokens||u.inTok; u.outTok=o.usage.completion_tokens||u.outTok; } }
    else if(API.provider==='anthropic'){
      if(o.type==='message_start'&&o.message&&o.message.usage){ const mu=o.message.usage;
        u.inTok=mu.input_tokens||u.inTok; u.outTok=mu.output_tokens||u.outTok;
        u.cacheRead=mu.cache_read_input_tokens||0; u.cacheCreate=mu.cache_creation_input_tokens||0; }
      if(o.type==='message_delta'&&o.usage){ u.outTok=o.usage.output_tokens||u.outTok; }
    }
    else if(API.provider==='gemini'){ if(o.usageMetadata){ const g=geminiUsage(o.usageMetadata);
      // 출력은 사고(thinking) 토큰 포함(geminiUsage가 total-prompt로 산출). 캐시 입력은 0.1× 과금.
      if(g.inTok) u.inTok=g.inTok; if(g.outTok) u.outTok=g.outTok; u.cacheRead=g.cacheRead; } }
  }catch(e){}
}
async function mockLLM(system,history,onTok){
  const last=(history[history.length-1]||{}).text||'';
  const comp=byId[(W.meta.companions||[])[0]]||byId[W.meta.protagonist]||{title:'그녀'};
  const parts=[
    '세피아빛 가로등이 골목을 적신다. ',
    '"'+last.slice(0,40)+'…" — '+jIGa(comp.title)+' 당신의 말끝을 따라 읊조리더니, 옅게 웃었다.\n\n',
    jEunNeun(comp.title)+' 한 걸음 다가서며 당신의 소매를 가만히 붙잡았다. 멀리서 괴이의 기척이 옅게 번졌지만, 지금만큼은 그 온기가 더 또렷했다.\n\n',
    '"…다음엔, 내가 먼저 갈게." 그 말에는 평소답지 않은 신뢰가 묻어 있었다.\n\n',
    '```state\n[{"path":"affinity.'+(comp.id||W.meta.protagonist)+'.value","op":"inc","value":6}]\n```'
  ];
  for(const p of parts){ for(let i=0;i<p.length;i+=3){ onTok(p.slice(i,i+3)); await new Promise(r=>setTimeout(r,8)); } }
}
function stripState(t){ const i=t.indexOf('```state'); return i>=0?t.slice(0,i).trimEnd():t; }
function parseDeltaArray(body){   // 절단(닫는 ] 누락) 보정 포함
  body=(body||'').trim(); if(!body) return [];
  try{ const j=JSON.parse(body); if(Array.isArray(j))return j; }catch(e){}
  const cut=body.lastIndexOf(']');           // 절단 시 마지막 ]까지로 보정
  if(cut>=0){ try{ const j=JSON.parse(body.slice(0,cut+1)); if(Array.isArray(j))return j; }catch(e){} }
  return [];
}
function extractState(t){
  // ```state``` 우선, 없으면 델타형(path/op 포함) ```json``` 도 수용. 닫는 펜스 없어도(절단) 매칭.
  let deltas=[], m=t.match(/```state\s*([\s\S]*?)(?:```|$)/i);
  if(!m){ const jm=t.match(/```json\s*([\s\S]*?)(?:```|$)/i); if(jm&&/["']path["']/.test(jm[1])&&/["']op["']/.test(jm[1])) m=jm; }
  if(m) deltas=parseDeltaArray(m[1]);
  deltas=deltas.filter(d=>d&&typeof d.path==='string'&&typeof d.op==='string');   // 델타 형태만
  // 화면·메모리 노출 방어: state 펜스(닫힘/절단 무관) 제거 + 델타형 json 펜스 제거
  let clean=t.replace(/```state[\s\S]*?(?:```|$)/i,'');
  clean=clean.replace(/```json\s*([\s\S]*?)(?:```|$)/i, (full,b)=> (/["']path["']/.test(b)&&/["']op["']/.test(b))?'':full);
  return {clean:clean.trim(), deltas};
}

/* ============ 라우팅 ============ */
function show(v){
  document.querySelectorAll('.view').forEach(x=>x.classList.remove('active'));
  document.getElementById('view-'+v).classList.add('active');
  document.querySelectorAll('#nav .navbtn').forEach(b=>b.classList.toggle('active',b.dataset.view===v));
  document.body.classList.toggle('on-play', v==='play');
  document.body.classList.remove('nav-open','rail-open');   // 뷰 전환 시 모바일 드로어/시트 닫기
  if(v==='status')renderStatus();
  if(v==='equip')renderEquip();
  if(v==='wiki')ensureWiki();
  if(v==='play')renderUsage();
}
let wikiLoaded=false;
function ensureWiki(){
  if(wikiLoaded) return;
  const fr=document.getElementById('wikiFrame');
  let html=''; try{ html=JSON.parse(document.getElementById('wikidoc').textContent)||''; }catch(e){}
  if(html){ fr.srcdoc=html; wikiLoaded=true; }  // srcdoc → 부모 origin 상속(이미지 공유 가능)
}
function setRunUi(){
  const on=!!W;
  // 회차가 결정되기 전엔 플레이/스테이터스/장비 탭을 숨긴다(시작 화면이 먼저).
  ['navPlay','navStatus','navEquip'].forEach(id=>{const b=document.getElementById(id); b.disabled=!on; b.style.display=on?'':'none';});
  document.getElementById('runtag').textContent = on?('회차 · '+youName()):'';
}

/* ============ 시작 화면 ============ */
let pickP=null, pickC=[], pickM=[], curFaction=null;
let youMode='canon', pickPersona=null, startDistrict=null, startTone='일상';   // 시작 경험 v2
const FAC_ORDER=['rep','bureau','trainee','shikoku','refusal','villain','guest','other'];
const pool=playable.concat(CANON.guests||[]);          // 선택 가능 인물 풀
const facList=f=>pool.filter(c=>c.faction===f);
const factionsPresent=()=>FAC_ORDER.filter(f=>facList(f).length);

function renderStart(){ renderYouMode(); renderPersonaPanel(); renderSlots(); renderTabs(); renderHand(); renderStartSet(); renderMem(); renderSaves(); updateStartBtn(); }
function updateStartBtn(){
  const ok = youMode==='canon' ? !!pickP : !!(pickPersona&&pickPersona.name&&pickPersona.detail);
  document.getElementById('startBtn').disabled=!ok;
}
/* 랜덤 구성: 캐논 주인공 + 동행 0~3 + 지역/분위기 무작위. 이후 사용자가 그대로 시작하거나 수정(고정) 가능. */
function _randInt(n){ return Math.floor(Math.random()*n); }
function randomizeStart(){
  const pl = playable.slice();
  if(!pl.length) return;
  youMode='canon'; pickPersona=null;
  pickP = pl[_randInt(pl.length)].id;
  const rest = pl.filter(c=>c.id!==pickP);
  for(let i=rest.length-1;i>0;i--){ const j=_randInt(i+1); const t=rest[i]; rest[i]=rest[j]; rest[j]=t; }
  pickC = rest.slice(0, _randInt(4)).map(c=>c.id);          // 동행 0~3명
  const ds=ASSETS.districts||[];
  startDistrict = (Math.random()<0.5 || !ds.length) ? deriveStartDistrict(pickP,pickC)
                                                    : ds[_randInt(ds.length)].key;
  startTone = TONES[_randInt(TONES.length)];
  renderStart();
}
function setYouMode(m){ if(youMode===m)return; youMode=m; renderStart(); }
function renderYouMode(){
  document.querySelectorAll('#youMode button').forEach(b=>b.classList.toggle('on',b.dataset.m===youMode));
  const desc=document.getElementById('youModeDesc');
  if(desc) desc.innerHTML = youMode==='persona'
    ? '<b>관측자</b> — 내가 만든 페르소나가 주인공이 됩니다. 세계관 밖에서 들어온 ‘나’로 플레이.'
    : '<b>마기아</b> — 로어 속 세계관에 실재하는 마법소녀가 주인공이 됩니다.';
  const h=document.getElementById('pickHint');
  if(h) h.textContent = youMode==='persona'
    ? '페르소나를 만들거나 고른 뒤, 팩션에서 동행(최대 3)을 선택하세요.'
    : '팩션을 고르고 카드를 누르면 위 슬롯(주인공 → 동행)에 들어갑니다. 슬롯의 ✕ 또는 카드를 다시 눌러 해제.';
}
function _psnVal(id){ const x=document.getElementById(id); return x?x.value:''; }
function _psnGrab(){ return {id:(pickPersona&&pickPersona.id)||null, name:_psnVal('psnName').trim(),
  age:_psnVal('psnAge').trim(), gender:_psnVal('psnGender').trim(), detail:_psnVal('psnDetail').trim()}; }
function renderPersonaPanel(){
  const el=document.getElementById('personaPanel'); if(!el) return;
  if(youMode!=='persona'){ el.className='persona-panel hide'; el.innerHTML=''; return; }
  el.className='persona-panel';
  const list=loadPersonas(); const d=pickPersona||{};
  const chips = list.length ? list.map(p=>'<span class="psn-chip'+(pickPersona&&pickPersona.id===p.id?' on':'')+'" data-id="'+p.id+'">'+esc(p.name)+'<button class="del" data-del="'+p.id+'" title="삭제">✕</button></span>').join('')
    : '<span class="muted" style="font-size:12px">저장된 페르소나 없음 — 아래에서 만들어 보세요.</span>';
  el.innerHTML='<div class="psn-chips">'+chips+'</div><div class="psn-form"><div class="psn-grid">'+
    '<div class="full"><label>이름 <span class="req">*</span></label><input id="psnName" maxlength="40" value="'+esc(d.name||'')+'" placeholder="예: 하와"></div>'+
    '<div><label>나이</label><input id="psnAge" maxlength="12" value="'+esc(d.age||'')+'" placeholder="예: 20"></div>'+
    '<div><label>성별</label><input id="psnGender" maxlength="12" value="'+esc(d.gender||'')+'" placeholder="예: 여성"></div>'+
    '<div class="full"><label>상세 정보 <span class="req">*</span></label><textarea id="psnDetail" maxlength="2000" placeholder="성격·배경·동기·특징을 자유롭게 작성해 주세요.">'+esc(d.detail||'')+'</textarea></div>'+
    '</div><div class="psn-actions"><button type="button" class="btn" id="psnUseOnce">세계관 관측</button>'+
    '<button type="button" class="btn ghost" id="psnSaveShared">고정</button></div></div>';
  el.querySelectorAll('.psn-chip').forEach(c=>c.onclick=e=>{ if(e.target.dataset.del)return; const p=loadPersonas().find(x=>x.id===c.dataset.id); if(p){ pickPersona=Object.assign({},p); renderPersonaPanel(); renderSlots(); updateStartBtn(); } });
  el.querySelectorAll('.psn-chip .del').forEach(b=>b.onclick=e=>{ e.stopPropagation(); deletePersona(b.dataset.del); if(pickPersona&&pickPersona.id===b.dataset.del)pickPersona=null; renderPersonaPanel(); renderSlots(); updateStartBtn(); });
  const commit=(save)=>{ const p=_psnGrab(); if(!p.name||!p.detail){ alert('이름과 상세 정보는 필수입니다.'); return; } pickPersona = save? Object.assign({},savePersona(p)) : (p.id=null,p); renderPersonaPanel(); renderSlots(); updateStartBtn(); };
  document.getElementById('psnUseOnce').onclick=()=>commit(false);
  document.getElementById('psnSaveShared').onclick=()=>commit(true);
}
function renderStartSet(){
  const el=document.getElementById('startSet'); if(!el) return;
  if(!startDistrict) startDistrict = deriveStartDistrict(youMode==='canon'?pickP:null, pickC);
  const opts=(ASSETS.districts||[]).map(d=>'<option value="'+d.key+'"'+(d.key===startDistrict?' selected':'')+'>'+esc(d.kr)+'</option>').join('');
  const tones=TONES.map(t=>'<button type="button" data-t="'+t+'" class="'+(t===startTone?'on':'')+'">'+t+'</button>').join('');
  el.innerHTML='<span class="ss-lab">시작 지역</span><select id="ssDistrict">'+opts+'</select>'+
    '<span class="ss-lab">분위기</span><span class="tonebtns" id="ssTone">'+tones+'</span>';
  document.getElementById('ssDistrict').onchange=function(){ startDistrict=this.value; };
  el.querySelectorAll('#ssTone button').forEach(b=>b.onclick=()=>{ startTone=b.dataset.t; renderStartSet(); });
}

function renderSlots(){
  const slots=[ youMode==='persona' ? {role:'p',persona:true,label:'관측자'} : {role:'p',id:pickP,label:'주인공'},
    {role:'c',id:pickC[0],label:'동행 1'},{role:'c',id:pickC[1],label:'동행 2'},{role:'c',id:pickC[2],label:'동행 3'}];
  document.getElementById('pickSlots').innerHTML=slots.map(s=>{
    if(s.persona){ return (pickPersona&&pickPersona.name)
      ? '<div class="pslot p filled persona"><span class="nm">✦ '+esc(pickPersona.name)+'</span></div>'
      : '<div class="pslot p"><span class="slab">'+s.label+'</span></div>'; }
    if(!s.id) return '<div class="pslot '+s.role+'"><span class="slab">'+s.label+'</span></div>';
    const c=byId[s.id]; const src=img(c.imgPrefix,'d');
    return '<div class="pslot '+s.role+' filled">'+(src?'<img src="'+src+'">':'')+
      '<span class="x" data-id="'+s.id+'">✕</span><span class="nm">'+esc(c.title)+'</span></div>';
  }).join('');
  document.querySelectorAll('#pickSlots .x').forEach(x=>x.onclick=e=>{e.stopPropagation(); selectChar(x.dataset.id);});
}
function renderTabs(){
  const tabs=factionsPresent();
  if(!curFaction||!tabs.includes(curFaction)) curFaction=tabs[0];
  const el=document.getElementById('factionTabs');
  el.innerHTML=tabs.map(f=>{ const lbl=(facList(f)[0]||{}).factionLabel||f;
    return '<button class="ftab '+(f===curFaction?'on':'')+'" data-f="'+f+'">'+esc(lbl)+
      '<span class="ct">'+facList(f).length+'</span></button>';}).join('');
  el.querySelectorAll('.ftab').forEach(b=>b.onclick=()=>{curFaction=b.dataset.f; renderTabs(); renderHand();});
}
function renderHand(){
  const list=facList(curFaction);
  document.getElementById('pickHand').innerHTML=list.map((c,i)=>{
    const src=img(c.imgPrefix,'d'); const taken=c.id===pickP||pickC.includes(c.id);
    const delay=Math.min(i,24)*24;
    return '<div class="fcard '+(taken?'taken':'')+'" data-id="'+c.id+'" style="animation-delay:'+delay+'ms">'+
      (src?'<img src="'+src+'" loading="lazy">':'<div class="noimg">'+esc((c.nameEn||'?')[0])+'</div>')+
      (taken?'<div class="chk">✓</div>':'')+
      '<div class="cap">'+esc(c.title)+'</div></div>';
  }).join('');
  document.querySelectorAll('#pickHand .fcard').forEach(d=>d.onclick=()=>selectChar(d.dataset.id));
  const hw=document.querySelector('.handwrap'); if(hw) hw.scrollLeft=0;
  setTimeout(updateHandNav,0);
}
function updateHandNav(){
  const hw=document.querySelector('.handwrap'); if(!hw)return;
  const prev=document.getElementById('handPrev'), next=document.getElementById('handNext');
  const scrollable=hw.scrollWidth>hw.clientWidth+4;
  prev.classList.toggle('hide',!scrollable); next.classList.toggle('hide',!scrollable);
  if(scrollable){ prev.disabled=hw.scrollLeft<=2; next.disabled=hw.scrollLeft>=hw.scrollWidth-hw.clientWidth-2; }
}
function renderMem(){
  const mem=ASSETS.modules.filter(m=>m.type==='memory');
  const unlocked=loadUnlockedMem();
  pickM=pickM.filter(id=>unlocked.includes(id));   // 잠긴 항목은 장착 불가
  const mc=document.getElementById('memChips');
  if(!mem.length){ mc.innerHTML='<span class="muted">아직 없음 — 회차를 끝내면 발급됩니다.</span>'; return; }
  mc.innerHTML=mem.map(m=>{
    if(!unlocked.includes(m.id))
      return '<span class="chip locked" title="잠김 — 회차를 완료해 시간을 되감으면 해금됩니다"><span class="lk">🔒</span><span class="lt">'+esc(m.title)+'</span></span>';
    return '<span class="chip mem '+(pickM.includes(m.id)?'on':'')+'" data-id="'+m.id+'" title="'+esc(m.desc||'')+'">'+esc(m.title)+'</span>';
  }).join('');
  mc.querySelectorAll('.chip.mem').forEach(el=>el.onclick=()=>{const id=el.dataset.id;
    pickM=pickM.includes(id)?pickM.filter(x=>x!==id):pickM.concat(id); renderMem();});
}
function renderSaves(){
  const saves=loadSaves(); const keys=Object.keys(saves).sort((a,b)=>saves[b].ts-saves[a].ts);
  const sl=document.getElementById('saveList');
  sl.innerHTML = keys.length?keys.map(k=>{const s=saves[k];
    return '<div class="item" data-k="'+k+'"><div><div class="it-t">'+esc(s.name)+'</div>'+
      '<div class="it-s">'+new Date(s.ts).toLocaleString()+' · 턴 '+(s.world.meta.turn||0)+'</div></div>'+
      '<span class="eqb load">불러오기</span></div>';}).join(''):'<div class="muted">저장된 회차 없음</div>';
  sl.querySelectorAll('.item').forEach(el=>el.onclick=()=>{ if(loadRun(el.dataset.k)){ setRunUi(); renderLog(); show('play'); } });
}
function selectChar(id){
  if(youMode==='persona'){               // 페르소나 모드: 핸드 선택은 동행만
    if(pickC.includes(id)) pickC=pickC.filter(x=>x!==id);
    else if(pickC.length<3) pickC.push(id);
    else return;
  } else {
    if(pickP===id){ pickP=null; }
    else if(pickC.includes(id)){ pickC=pickC.filter(x=>x!==id); }
    else if(!pickP){ pickP=id; }
    else if(pickC.length<3){ pickC.push(id); }
    else { return; }   // 슬롯 가득
  }
  renderSlots();
  // 핸드의 taken 상태만 갱신(재빌드 없이 fanin 깜빡임 방지)
  document.querySelectorAll('#pickHand .fcard').forEach(d=>{
    const taken=d.dataset.id===pickP||pickC.includes(d.dataset.id);
    d.classList.toggle('taken',taken);
    let chk=d.querySelector('.chk');
    if(taken&&!chk){ chk=document.createElement('div'); chk.className='chk'; chk.textContent='✓'; d.appendChild(chk); }
    if(!taken&&chk) chk.remove();
  });
  updateStartBtn();
}

/* ============ 플레이 ============ */
function renderLog(){
  const root=document.getElementById('log'); let html=situationCardHtml();
  if(!convo.length){
    html+='<div class="msg sys">— '+esc(youName())+'의 이야기가 시작된다 —</div>';
    // 프롤로그가 이미 생성됐는데 비어있는 예외 상황에만 안내 노출(생성 예정이면 startPrologue가 채움)
    if(W.meta.prologueDone) html+='<div class="msg a"><div class="bub">'+mdRender('당신의 첫 행동이나 대사를 입력해 장면을 시작하세요. (예: "사무소 문을 열고 들어선다")')+'</div></div>';
  } else {
    convo.forEach(m=>{ html+='<div class="msg '+(m.role==='user'?'u':'a')+'"><div class="bub">'+
      (m.role==='user'?esc(m.text):mdRender(m.text))+'</div></div>'; });
  }
  root.innerHTML=html; root.scrollTop=root.scrollHeight;
  renderRail();
}
const MAGIC_CIRCLE='<svg class="mcircle" viewBox="0 0 100 100">'+
  '<g class="r1" stroke-width="1">'+
    '<circle cx="50" cy="50" r="47"/><circle cx="50" cy="50" r="43" stroke-dasharray="2 3" opacity=".7"/>'+
    '<polygon points="50,7 87,71 13,71"/><polygon points="50,93 87,29 13,29"/></g>'+
  '<g class="r2" stroke-width="1">'+
    '<circle cx="50" cy="50" r="34"/><rect x="28" y="28" width="44" height="44"/>'+
    '<rect x="28" y="28" width="44" height="44" transform="rotate(45 50 50)"/></g>'+
  '<g class="pulse" stroke-width="1.3"><circle cx="50" cy="50" r="17"/><circle cx="50" cy="50" r="8"/></g></svg>';
const LOADER_HTML='<div class="loader">'+MAGIC_CIRCLE+'<div class="lcap">마법진 전개 중…</div></div>';
function appendAssistant(){
  const root=document.getElementById('log');
  const d=document.createElement('div'); d.className='msg a';
  const b=document.createElement('div'); b.className='bub'; b.innerHTML=LOADER_HTML;
  d.appendChild(b); root.appendChild(d); root.scrollTop=root.scrollHeight; return b;
}
let busy=false;
async function turn(text){
  if(busy||!text.trim())return; busy=true;
  document.getElementById('sendBtn').disabled=true;
  convo.push({role:'user',text:text});
  // 사용자 메시지 렌더
  const root=document.getElementById('log');
  const u=document.createElement('div'); u.className='msg u';
  u.innerHTML='<div class="bub">'+esc(text)+'</div>'; root.appendChild(u);
  const bub=appendAssistant(); let acc='';   // 생성 중엔 마법진 로더, 본문은 완료 후 일괄 표출
  const histForCall = convo.slice(-MEM_KEEP);  // 슬라이딩 윈도: 최근 메시지만 전송(먼 기억은 호드 요약)
  const sys=assembleContext();
  const segSnap = Object.assign({}, PROMPT_SEGS);  // 분해 스냅샷
  let usage=null;
  try{
    usage = await callLLM(sys, histForCall, t=>{ acc+=t; root.scrollTop=root.scrollHeight; });
  }catch(e){ bub.innerHTML='<span style="color:#e0a35c">[호출 오류] '+esc(e.message)+'</span>'; busy=false;
    document.getElementById('sendBtn').disabled=false; return; }
  let {clean,deltas}=extractState(acc);
  bub.classList.add('reveal'); bub.innerHTML=mdRender(clean); root.scrollTop=root.scrollHeight;
  convo.push({role:'assistant',text:clean});
  const rec=firstSentence(clean);
  if(rec){ W.recap=W.recap||[]; W.recap.push(rec); if(W.recap.length>8) W.recap.shift(); }
  // 하이브리드: 인라인 델타가 비면 싼 모델 구조화 추출로 폴백(mock/키없음 제외)
  if(!deltas.length && API.provider!=='mock'){
    try{ const fb=await extractDeltasFallback(text, clean); if(fb&&fb.length) deltas=fb; }catch(e){}
  }
  if(deltas.length){ const changes=mutate(deltas); renderRail(); flashChanges(changes); recordChanges(changes); }
  accountTurn(segSnap, histForCall, acc, usage);
  saveRun();
  busy=false; document.getElementById('sendBtn').disabled=false;
  maybeSummarize();   // 윈도 밖 누적 시 장기기억 요약(비동기, 비차단)
}
/* 하이브리드 폴백: 서사 콜과 분리해 싼 모델로 상태 델타만 구조화 추출 (인라인 누락 시에만) */
async function extractDeltasFallback(userText, sceneText){
  const key=(API.keys&&API.keys[API.provider])||API.key||''; if(!key) return [];
  const model=CHEAP_MODEL[API.provider]||API.model;
  const ids=[].concat(W.meta.companions||[]); for(const id in W.affinity) if(!ids.includes(id))ids.push(id);
  const roster=ids.map(id=>{const c=byId[id]; if(!c)return null; const a=W.affinity[id]||{}; return c.title+'('+id+', '+(a.value!=null?a.value:0)+')';}).filter(Boolean).join(', ');
  const sys='[상태 변화 추출] 아래 장면에서 *실제로 일어난* 관계·세계 상태 변화만 JSON 배열로 출력하라. 추측·과장 금지, 변화 없으면 [].\n'+
    '허용 path: affinity.<charId>.value(-100~100 증감), affinity.<charId>.axes.<trust|respect|romance>, flags.<키>, territory.<지구>.stability. op: set|inc|dec|toggle.\n'+
    '인물: '+roster+'\n오직 JSON 배열만 출력(코드펜스·설명 금지). 예: [{"path":"affinity.char-13.value","op":"inc","value":5}]';
  const userMsg='[플레이어 입력]\n'+userText+'\n\n[장면]\n'+(sceneText||'').slice(0,1800);
  const ep=API.endpoint||PRESETS[API.provider].ep;
  let url=ep, headers={'Content-Type':'application/json'}, body;
  if(API.provider==='openai'){ headers['Authorization']='Bearer '+key;
    body={model,messages:[{role:'system',content:sys},{role:'user',content:userMsg}],max_tokens:300}; }
  else if(API.provider==='anthropic'){ headers['x-api-key']=key; headers['anthropic-version']='2023-06-01'; headers['anthropic-dangerous-direct-browser-access']='true';
    body={model,max_tokens:300,system:sys,messages:[{role:'user',content:userMsg}]}; }
  else if(API.provider==='gemini'){ url=ep+'/'+model+':generateContent?key='+encodeURIComponent(key);
    body={systemInstruction:{parts:[{text:sys}]},contents:[{role:'user',parts:[{text:userMsg}]}]}; }
  else return [];
  const res=await fetch(url,{method:'POST',headers,body:JSON.stringify(body)}); if(!res.ok) return [];
  const j=await res.json(); let text='';
  if(API.provider==='openai') text=(j.choices&&j.choices[0]&&j.choices[0].message&&j.choices[0].message.content)||'';
  else if(API.provider==='anthropic') text=(j.content||[]).filter(b=>b.type==='text').map(b=>b.text).join('');
  else if(API.provider==='gemini'){ try{ text=j.candidates[0].content.parts.map(p=>p.text||'').join(''); }catch(e){} }
  // 비용 회계
  let inT=0,outT=0,cacheR=0;
  if(j.usage){ inT=j.usage.input_tokens||j.usage.prompt_tokens||0; outT=j.usage.output_tokens||j.usage.completion_tokens||0; }
  else if(j.usageMetadata){ const g=geminiUsage(j.usageMetadata); inT=g.inTok; outT=g.outTok; cacheR=g.cacheRead; }
  if((inT||outT)&&W.usage){ const sc=cost(inT,outT,model,cacheR); W.usage.runIn+=inT; W.usage.runOut+=outT; W.usage.runKRW+=sc; }
  const arr=parseDeltaArray((text||'').replace(/```json|```/g,'').trim());
  return arr.filter(d=>d&&typeof d.path==='string'&&typeof d.op==='string');
}
/* 밴드 전이 가시화(채팅 로그에 칩) + 장기기억 기록 */
function flashChanges(changes){
  if(!changes||!changes.length) return;
  const root=document.getElementById('log'); if(!root) return;
  changes.forEach(ch=>{ const d=document.createElement('div'); d.className='msg chg';
    d.textContent='◈ '+ch.title+' — '+ch.from+' → '+ch.to; root.appendChild(d); });
  root.scrollTop=root.scrollHeight;
}
function recordChanges(changes){
  if(!changes||!changes.length||!W) return;
  W.changeLog=W.changeLog||[];
  changes.forEach(ch=>W.changeLog.push({turn:W.meta.turn, note:jWaGwa(ch.title)+'의 관계가 '+ch.from+'에서 '+jEuRo(ch.to)+' 바뀌었다'}));
  if(W.changeLog.length>12) W.changeLog=W.changeLog.slice(-12);
}
/* ============ 상황 카드 + 프롤로그 ============ */
function situationCardText(){
  const dk=W.meta.start.districtKey, t=(W.territory||{})[dk]||{};
  const ctrl=(t.controller&&byId[t.controller])?byId[t.controller].title:null;
  const comps=(W.meta.companions||[]).map(id=>(byId[id]||{}).title).filter(Boolean);
  const L=['시점 인물: '+youName(),
    '장소: '+districtKrOf(dk)+(t.sealed?' (봉인 지역)':'')+(ctrl?(' · 지역 대표 '+ctrl):'')+(t.stability!=null?(' · 안정도 '+t.stability):''),
    '분위기: '+(W.meta.start.tone||'일상')];
  if(comps.length) L.push('동행: '+comps.join(', '));
  return L.join('\n');
}
function situationCardHtml(){
  if(!W||!W.meta.start) return '';
  const dk=W.meta.start.districtKey, t=(W.territory||{})[dk]||{};
  const ctrl=(t.controller&&byId[t.controller])?byId[t.controller].title:null;
  const comps=(W.meta.companions||[]).map(id=>(byId[id]||{}).title).filter(Boolean);
  const chip=(l,v)=>'<span class="scchip"><b>'+esc(l)+'</b> '+esc(v)+'</span>';
  let c=chip('시점',youName())+chip('장소',districtKrOf(dk)+(t.sealed?' (봉인)':''))+chip('분위기',W.meta.start.tone||'일상');
  if(ctrl)c+=chip('지역대표',ctrl); if(comps.length)c+=chip('동행',comps.join(', '));
  return '<div class="sitcard"><div class="sc-h">◈ 시작 상황</div><div class="sc-chips">'+c+'</div></div>';
}
function fallbackPrologue(){
  const who=youName(); const place=districtKrOf(W.meta.start.districtKey);
  const comps=(W.meta.companions||[]).map(id=>(byId[id]||{}).title).filter(Boolean);
  let s=place+'의 공기가 낮게 가라앉아 있다. '+jEunNeun(who)+' 익숙하면서도 낯선 거리 한복판에 서서, 멀리서 번지는 마나의 잔향에 가만히 귀를 기울인다.\n\n';
  s+= comps.length ? (jIGa(comps[0])+' 곁에서 발걸음을 맞추며 곁눈질로 당신을 살핀다. "…그래서, 이제 어디로 갈 거야?"\n\n')
                   : '괴이의 기척이 옅게 스민 골목 끝에서, 무언가가 당신의 선택을 기다리는 듯하다.\n\n';
  return s+'— 당신의 첫 행동이나 대사를 입력해 장면을 이어가세요.';
}
async function startPrologue(){
  if(!W||W.meta.prologueDone||convo.length) return;
  const root=document.getElementById('log'); if(!root) return;
  const bub=appendAssistant(); let acc='';
  const sys=assembleContext(); const segSnap=Object.assign({},PROMPT_SEGS);
  const guide='\n\n[프롤로그 작성] 지금은 이 회차의 첫 장면이다. 위 설정과 아래 시작 상황을 바탕으로 "당신"('+youName()+') 시점에서 장면을 연다. 인물·지역·분위기를 설명하지 말고 장면으로 보여줘라(2~4문단). 메타 질문·선택지 나열로 닫지 말고 여운으로 멈춰 플레이어가 이어 쓰게 둬라. 이 첫 장면에서는 상태 델타(```state)를 출력하지 마라.\n[시작 상황]\n'+situationCardText();
  const sysForCall={stable:sys.stable, volatile:(sys.volatile||'')+guide, text:(sys.text||'')+guide};
  let usage=null;
  if(API.provider==='mock'){ acc=fallbackPrologue(); }
  else { try{ usage=await callLLM(sysForCall,[{role:'user',text:'(이 회차의 첫 장면을 열어 주세요.)'}],t=>{acc+=t; root.scrollTop=root.scrollHeight;}); }
    catch(e){ acc=fallbackPrologue(); } }
  const {clean}=extractState(acc); const body=(clean&&clean.trim())||fallbackPrologue();
  bub.classList.add('reveal'); bub.innerHTML=mdRender(body); root.scrollTop=root.scrollHeight;
  convo.push({role:'assistant',text:body});
  W.meta.prologueDone=true;
  const rec=firstSentence(body); if(rec){ W.recap=W.recap||[]; W.recap.push(rec); }
  if(usage) accountTurn(segSnap, [], body, usage);
  saveRun();
}
/* ============ 장기기억(호드): 슬라이딩 윈도 밖 대화를 싼 모델로 요약 ============ */
let summarizing=false;
async function maybeSummarize(){
  if(!W||summarizing) return;
  const upto=W.summaryUpto||0;
  const end=convo.length-MEM_KEEP;          // 윈도 밖 경계
  if(end-upto < MEM_BATCH) return;          // 아직 배치 미충족
  const slice=convo.slice(upto,end); if(!slice.length) return;
  summarizing=true;
  let res=null;
  try{ res=await summarizeMemory(slice, W.summary||''); }catch(e){ res=null; }
  let summ=res&&res.text;
  if(!summ){ summ=extractiveSummary(slice, W.summary||''); }   // 호출 실패/mock → 추출 폴백
  if(summ){
    W.summary=summ; W.summaryUpto=end;
    if(res&&(res.inTok||res.outTok)&&W.usage){   // 요약 비용도 회차 누적에 반영
      const sc=cost(res.inTok,res.outTok,res.model,res.cacheRead);
      W.usage.runIn+=res.inTok||0; W.usage.runOut+=res.outTok||0; W.usage.runKRW+=sc;
      W.usage.summaryKRW=(W.usage.summaryKRW||0)+sc;
    }
    saveRun(); renderUsage();
  }
  summarizing=false;
}
function extractiveSummary(slice, prev){
  const bullets=[];
  slice.forEach(m=>{ if(m.role==='assistant'){ const s=firstSentence(m.text); if(s)bullets.push('- '+s); }});
  let lines=((prev?prev+'\n':'')+bullets.join('\n')).split('\n').filter(x=>x.trim());
  if(lines.length>14) lines=lines.slice(-14);
  return lines.join('\n').trim();
}
async function summarizeMemory(slice, prev){
  if(API.provider==='mock') return null;
  const key=(API.keys&&API.keys[API.provider])||API.key||''; if(!key) return null;
  const model=CHEAP_MODEL[API.provider]||API.model;
  const guide='[장기기억 요약 작업] 아래는 진행 중인 라이트노벨 플레이의 지난 대화다. 다음 장면 생성에 필요한 맥락만 *장기 기억*으로 압축하라.\n'+
    '- 무엇을: 인물별 관계·호칭·말투 변화, 약속·목표, 미해결 떡밥/갈등, 판명된 사실·중요한 결정, 감정선의 분기점.\n'+
    '- 어떻게: 평어체("~다") 불릿 8개 이내(각 한 줄). 고유명사는 캐논 표기 유지. 격식체·번역투·헤지 금지.\n'+
    '- 금지: 일어나지 않은 일 창작, 장면 묘사 재현, 사소한 동작 나열. 기존 요약이 있으면 새 내용과 통합해 갱신하고 중복은 제거하라.';
  const prevBlock=prev?('\n[기존 요약]\n'+prev):'';
  const sys=guide+prevBlock;
  const convoText=slice.map(m=>(m.role==='user'?'유저: ':'서사: ')+(m.text||'')).join('\n');
  const userMsg='[요약할 대화]\n'+convoText;
  const ep=API.endpoint||PRESETS[API.provider].ep;
  let url=ep, headers={'Content-Type':'application/json'}, body;
  if(API.provider==='openai'){
    headers['Authorization']='Bearer '+key;
    body={model,messages:[{role:'system',content:sys},{role:'user',content:userMsg}],max_tokens:512};
  } else if(API.provider==='anthropic'){
    headers['x-api-key']=key; headers['anthropic-version']='2023-06-01'; headers['anthropic-dangerous-direct-browser-access']='true';
    body={model,max_tokens:512,system:sys,messages:[{role:'user',content:userMsg}]};
  } else if(API.provider==='gemini'){
    url=ep+'/'+model+':generateContent?key='+encodeURIComponent(key);
    body={systemInstruction:{parts:[{text:sys}]},contents:[{role:'user',parts:[{text:userMsg}]}]};
  } else { return null; }
  const res=await fetch(url,{method:'POST',headers,body:JSON.stringify(body)});
  if(!res.ok) return null;
  const j=await res.json();
  let text='', inTok=0, outTok=0, cacheRead=0;
  if(API.provider==='openai'){ text=(j.choices&&j.choices[0]&&j.choices[0].message&&j.choices[0].message.content)||'';
    if(j.usage){ inTok=j.usage.prompt_tokens||0; outTok=j.usage.completion_tokens||0; } }
  else if(API.provider==='anthropic'){ text=(j.content||[]).filter(b=>b.type==='text').map(b=>b.text).join('');
    if(j.usage){ inTok=j.usage.input_tokens||0; outTok=j.usage.output_tokens||0; } }
  else if(API.provider==='gemini'){ try{ text=j.candidates[0].content.parts.map(p=>p.text||'').join(''); }catch(e){}
    if(j.usageMetadata){ const g=geminiUsage(j.usageMetadata); inTok=g.inTok; outTok=g.outTok; cacheRead=g.cacheRead; } }
  text=(text||'').trim();
  return text?{text, inTok, outTok, cacheRead, model}:null;
}
/* 턴 토큰·비용 회계 + 세피로트 분해 */
function accountTurn(segs, hist, outText, usage){
  if(!W) return;
  // history(최근 대화) 추정 — role별 분리
  let hUser=0, hAsst=0;
  hist.forEach(m=>{ const t=estTokens(m.text); if(m.role==='assistant')hAsst+=t; else hUser+=t; });
  // 세그먼트 추정
  const segEst={ keter:estTokens(segs.keter), binah:estTokens(segs.binah), tiphereth:estTokens(segs.tiphereth),
    netzach:estTokens(segs.netzach), hod:estTokens(segs.hod), yesod:estTokens(segs.yesod), malkuth:estTokens(segs.malkuth),
    hesed:hUser, gevurah:hAsst };
  let estIn=0; for(const k in segEst) estIn+=segEst[k];
  const cacheR=(usage&&usage.cacheRead)||0, cacheC=(usage&&usage.cacheCreate)||0;
  const billedIn=(usage&&usage.inTok)|| estIn || 1;          // 풀과금(미캐시) 입력 — 실제 우선
  const totalPrompt=billedIn+cacheR+cacheC;                  // 전체 프롬프트(캐시 포함) — 구성비/도넛 기준
  const outTok= (usage&&usage.outTok)|| estTokens(outText) || 0;
  const scale = estIn? totalPrompt/estIn : 1;                // 추정 비율을 전체 프롬프트에 맞춤(구성비 보존)
  const breakdown = SEPHIROT.map(s=>{ const tok=Math.round((segEst[s.key]||0)*scale);
    return {key:s.key, name:s.name, sub:s.sub, src:s.src, color:s.color, why:s.why, tok}; });
  const totIn = breakdown.reduce((a,b)=>a+b.tok,0)||totalPrompt;
  breakdown.forEach(b=>b.pct=Math.round(b.tok/totIn*1000)/10);
  const c = cost(billedIn,outTok,API.model,cacheR,cacheC);   // 비용은 캐시 할인 반영
  const u = W.usage || (W.usage={runIn:0,runOut:0,runKRW:0,turns:0});
  u.lastIn=totalPrompt; u.lastOut=outTok; u.lastKRW=c; u.lastBreakdown=breakdown; u.lastModel=API.model;
  u.lastCacheRead=cacheR; u.lastCacheCreate=cacheC; u.lastBilledIn=billedIn;
  u.runIn+=totalPrompt; u.runOut+=outTok; u.runKRW+=c; u.runCacheRead=(u.runCacheRead||0)+cacheR; u.turns++;
  renderUsage();
}
function renderUsage(){
  const el=document.getElementById('hud'); if(!el||!W) return;
  const u=W.usage; if(!u||!u.turns){ el.innerHTML='<span class="muted" style="font-size:11.5px">아직 소모된 억지력이 없습니다 — 첫 응답 후 표시됩니다.</span>'; return; }
  const mock=API.provider==='mock';
  const tcost=mock?' · 시연 ₩0':' ('+krw(u.lastKRW)+')';
  const rcost=mock?' · ₩0':' ('+krw(u.runKRW)+')';
  const cache=(u.lastCacheRead>0)?'<span class="hud-sep">·</span><span class="hud-i hud-cache" title="프롬프트 캐시에서 재사용된 입력 토큰 — 입력 비용 약 1/10">⚡ 캐시 적중 <b>'+qlip(u.lastCacheRead)+'</b></span>':'';
  el.innerHTML='<span class="hud-i">이번 턴 ▸ <b>'+qlip(u.lastIn+u.lastOut)+'</b>'+tcost+'</span>'+cache+
    '<span class="hud-sep">·</span><span class="hud-i">이번 회차 ▸ <b>'+qlip(u.runIn+u.runOut)+'</b>'+rcost+'</span>'+
    '<button class="qbtn hud-btn" id="qlipBtn">⛧ 소모 억지력 보기 (세부)</button>';
  const b=document.getElementById('qlipBtn'); if(b) b.onclick=openQlip;
}
function openQlip(){
  const u=W&&W.usage; const bd=(u&&u.lastBreakdown)||[];
  const box=document.getElementById('qlipBody');
  if(!bd.length){ box.innerHTML='<p class="muted">아직 분석할 입력이 없습니다.</p>'; }
  else{
    const tot=bd.reduce((a,x)=>a+x.tok,0)||1;
    // 도넛(conic-gradient)
    let acc=0, stops=[];
    bd.forEach(x=>{ const p=x.tok/tot*100; stops.push(x.color+' '+acc.toFixed(2)+'% '+(acc+p).toFixed(2)+'%'); acc+=p; });
    const donut='<div class="donut" style="background:conic-gradient('+stops.join(',')+')"><div class="donut-h"><b>'+Math.round(u.lastIn).toLocaleString('ko-KR')+'</b><span>입력 토큰</span></div></div>';
    const cacheNote=(u.lastCacheRead>0)?'<br><span class="muted">⚡ 캐시 적중 '+qlip(u.lastCacheRead)+' — 입력 비용 약 1/10</span>':'';
    const rows=bd.map(x=>'<div class="qrow"><span class="swatch" style="background:'+x.color+'"></span>'+
      '<div class="qmain"><div class="qtop"><b>'+esc(x.name)+'</b> <span class="qsub">'+esc(x.sub)+'</span>'+
      '<span class="qnum">'+x.tok.toLocaleString('ko-KR')+' <span class="qpct">'+x.pct+'%</span></span></div>'+
      '<div class="qsrc">'+esc(x.src)+'</div><div class="qwhy">'+esc(x.why)+'</div></div></div>').join('');
    box.innerHTML='<div class="qlip-head">'+donut+'<div class="qlip-cap">입력 토큰 상세 — 세피로트 분해<br><span class="muted">모델 '+esc(u.lastModel||API.model)+' · 출력 '+qlip(u.lastOut)+'</span>'+cacheNote+'</div></div>'+
      '<div class="qlist">'+rows+'</div>'+
      '<p class="muted" style="font-size:11px;margin-top:10px">프롬프트 버전·추정 방식에 따라 상세 토큰에 차이가 발생할 수 있습니다. (총량은 API usage, 구간 비율은 추정)</p>';
  }
  document.getElementById('qlipModal').classList.add('on');
}
/* 빠른 액션: 상황묘사 — 플레이어 입력 없이 장면을 이어 묘사 */
function quickNarrate(){
  if(busy||!W) return;
  turn('(내 행동을 기다리지 말고, 장면을 한 박자 자연스럽게 이어서 묘사해 줘.)');
}
/* 빠른 액션: 추천답변 — 후보 3개를 받아 선택지 칩으로 */
async function suggestReplies(){
  if(busy||!W) return;
  const box=document.getElementById('choices');
  box.innerHTML='<span class="muted" style="font-size:12px">추천 답변 생성 중…</span>';
  const sys=assembleContext().text+'\n\n[작업] 위 상황에서 플레이어("당신")가 취할 법한 짧은 행동/대사 후보를 정확히 3개, 각 줄 앞에 "- "를 붙여 한 줄씩 제시하라. 서사·설명·번호 없이 후보 문장만.';
  let out='';
  try{
    if(API.provider==='mock'){ out='- 조심스럽게 다가가 말을 건다\n- 한 걸음 물러서 상황을 살핀다\n- 손을 내밀어 그녀를 돕는다'; }
    else { const u=await callLLM(sys, convo.slice(-MEM_KEEP).concat([{role:'user',text:'(추천 답변 후보 3개만)'}]), t=>{ out+=t; });
      if(u&&W&&W.usage){ W.usage.runIn+=(u.inTok||0); W.usage.runOut+=(u.outTok||0); W.usage.runKRW+=cost(u.inTok,u.outTok,API.model); renderUsage(); } }
  }catch(e){ box.innerHTML='<span style="color:#e0a35c;font-size:12px">[추천 실패] '+esc(e.message)+'</span>'; return; }
  const opts=out.split(/\n/).map(s=>s.replace(/^[\s\-*•·\d.)]+/,'').trim()).filter(Boolean).slice(0,3);
  box.innerHTML='';
  opts.forEach(o=>{ const b=document.createElement('button'); b.className='choice'; b.textContent=o;
    b.onclick=()=>{ const i=document.getElementById('userInput'); i.value=o; box.innerHTML=''; i.focus(); };
    box.appendChild(b); });
  if(!opts.length) box.innerHTML='<span class="muted" style="font-size:12px">후보를 만들지 못했습니다.</span>';
}
function firstSentence(t){
  let s=(t||'').replace(/[#*>`_]/g,'').replace(/\s+/g,' ').trim().replace(/^["'“”‘’\-\s]+/,'');
  const m=s.match(/^[\s\S]*?[.!?。…！？]/);
  let out=(m?m[0]:s).trim();
  if(out.length>96) out=out.slice(0,94).trim()+'…';
  return out;
}
function renderRail(){
  const root=document.getElementById('railList'); if(!W){root.innerHTML='';return;}
  const ids=Object.keys(W.affinity).sort((a,b)=>W.affinity[b].value-W.affinity[a].value); let html='';
  ids.forEach(id=>{ const c=byId[id]; if(!c)return; const a=W.affinity[id]; const b=bandOf(a.value);
    const pct=(a.value+100)/2; const src=img(c.imgPrefix,'d');
    html+='<div class="mini">'+(src?'<img src="'+src+'">':'<div class="av">'+esc((c.nameEn||'?')[0])+'</div>')+
      '<div style="flex:1;min-width:0"><div class="nm" style="display:flex;align-items:center;gap:6px">'+esc(c.title)+
      '<span class="bandtag" style="background:'+b.color+'33;color:'+b.color+'">'+b.label+'</span>'+
      '<span class="affnum">'+(a.value>0?'+':'')+a.value+'</span></div>'+
      '<div class="bar"><i style="width:'+pct+'%;background:'+b.color+'"></i></div></div></div>';
  });
  root.innerHTML=html||'<div class="muted" style="font-size:12px">아직 관계 변화 없음</div>';
}

/* ============ 스테이터스 뷰 (마스터-디테일) ============ */
let statusSel=null;
function statusIds(){
  const set=new Set(Object.keys(W.affinity)); (W.meta.companions||[]).forEach(i=>set.add(i));
  return Array.from(set).filter(id=>byId[id])
    .sort((a,b)=>((W.affinity[b]||{}).value||0)-((W.affinity[a]||{}).value||0));
}
function renderStatus(){
  if(!W) return;
  renderRecap();
  const ids=statusIds();
  if(!statusSel||!ids.includes(statusSel)) statusSel=ids[0]||null;
  renderStatusList(); renderStatusDetail(statusSel);
}
function renderRecap(){
  const el=document.getElementById('statusRecap'); if(!el)return;
  const r=(W.recap||[]).slice(-5).reverse();
  el.innerHTML='<h4>최근 전개</h4>'+(r.length
    ?'<ul>'+r.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul>'
    :'<div class="muted">아직 전개가 없습니다 — 플레이를 진행하면 최근 장면이 요약됩니다.</div>');
}
function renderStatusList(){
  const ids=statusIds(); const root=document.getElementById('statusList');
  if(!ids.length){ root.innerHTML='<div class="muted" style="padding:8px;font-size:12px">관계 데이터가 아직 없습니다.</div>';
    document.getElementById('statusDetail').innerHTML=''; return; }
  root.innerHTML=ids.map(id=>{ const c=byId[id]; const a=W.affinity[id]||{value:0}; const b=bandOf(a.value); const src=img(c.imgPrefix,'d');
    return '<div class="srow '+(id===statusSel?'on':'')+'" data-id="'+id+'">'+
      (src?'<img src="'+src+'">':'<div class="av">'+esc((c.nameEn||'?')[0])+'</div>')+
      '<div class="sm"><div class="snm"><span class="dot" style="background:'+b.color+'"></span>'+esc(c.title)+
      '<span class="affnum">'+(a.value>0?'+':'')+a.value+'</span></div>'+
      '<div class="bar"><i style="width:'+((a.value+100)/2)+'%;background:'+b.color+'"></i></div></div></div>';
  }).join('');
  root.querySelectorAll('.srow').forEach(el=>el.onclick=()=>{ statusSel=el.dataset.id;
    root.querySelectorAll('.srow').forEach(r=>r.classList.toggle('on',r.dataset.id===statusSel));
    renderStatusDetail(statusSel); });
}
function renderStatusDetail(id){
  const root=document.getElementById('statusDetail'); if(!id){ root.innerHTML=''; return; }
  const c=byId[id]; const a=W.affinity[id]||{value:0,axes:{}}; const b=bandOf(a.value); const src=img(c.imgPrefix,'d');
  const axhtml=(ASSETS.axes||[]).map(ax=>{ const v=(a.axes&&a.axes[ax])||0; const pct=(v+100)/2;
    return '<div class="axline"><div class="axhd"><span class="axn">'+(AXIS_KR[ax]||ax)+'</span>'+
      '<span class="axv">'+(v>0?'+':'')+v+'</span></div>'+
      '<div class="bar"><i style="width:'+pct+'%;background:var(--bureau)"></i></div></div>';}).join('');
  const p=byId[W.meta.protagonist]; let rel='';
  if(p&&p.relationships){ const r=p.relationships.find(x=>x.targetId===id); if(r) rel='<div class="relnote">관계 — '+esc(r.text)+'</div>'; }
  const meta=[c.factionLabel,c.rankLabel,c.districtKr,c.generation].filter(Boolean).join(' · ');
  root.innerHTML='<div class="sp">'+(src?'<img src="'+src+'">':'<div class="av">'+esc((c.nameEn||'?')[0])+'</div>')+'</div>'+
    '<div class="sbody"><div class="nmrow"><h3>'+esc(c.title)+'</h3>'+
    '<span class="bandtag" style="background:'+b.color+'33;color:'+b.color+'">'+b.label+'</span>'+
    '<span class="affnum">호감도 '+(a.value>0?'+':'')+a.value+'</span></div>'+
    '<div class="en">'+esc(c.nameEn||'')+(meta?' · '+esc(meta):'')+'</div>'+
    '<div class="bar" style="height:9px"><i style="width:'+((a.value+100)/2)+'%;background:'+b.color+'"></i></div>'+
    '<div class="axes">'+axhtml+'</div>'+rel+'</div>';
}

/* ============ 장비/복장 뷰 ============ */
function itemRow(m, on, slot, sub){
  return '<div class="item '+(on?'on':'')+'" data-id="'+m.id+'" data-slot="'+slot+'">'+
    '<div style="display:flex;align-items:center;gap:10px;min-width:0">'+
      (m.img?'<img class="it-th" src="'+m.img+'">':'')+
      '<div style="min-width:0"><div class="it-t">'+esc(m.title)+'</div>'+
      '<div class="it-s">'+esc(sub)+'</div></div></div>'+
    '<span class="eqb">'+(on?'해제':'장착')+'</span></div>';
}
function renderEquip(){
  if(!W)return; const pid=W.meta.protagonist; const p=byId[pid];
  const eqOutfit=W.inventory.equipped.outfit;
  const kind=(eqOutfit&&modById[eqOutfit]&&modById[eqOutfit].imgKind)||'d';
  const src=img(p.imgPrefix,kind);
  document.getElementById('equipPortrait').innerHTML=
    (src?'<img src="'+src+'">':'<div class="av">'+esc((p.nameEn||'?')[0])+'</div>')+
    '<div class="pname">'+esc(p.title)+'<span>'+esc(p.nameEn||'')+(p.rankLabel?' · '+esc(p.rankLabel):'')+'</span></div>';
  const owned=W.inventory.owned.map(id=>modById[id]).filter(Boolean);
  const slots=[['outfit','복장'],['weapon','무기'],['accessory','장신구']];
  let html='';
  slots.forEach(([slot,label])=>{
    const items=owned.filter(m=>(m.slot||'')===slot);
    html+='<div class="slot"><div class="lab">'+label+'</div>';
    if(!items.length) html+='<div class="muted" style="font-size:12px">보유 항목 없음</div>';
    items.forEach(m=>{ const on=W.inventory.equipped[slot]===m.id;
      html+=itemRow(m, on, slot, TYPE_KR[m.type]||m.type); });
    html+='</div>';
  });
  // 세계의 기억(장착 효과, 슬롯 없음)
  const mems=owned.filter(m=>m.type==='memory');
  if(mems.length){ html+='<div class="slot"><div class="lab">세계의 기억</div>'+
    mems.map(m=>itemRow(m, W.modules.equipped.includes(m.id), 'memory', m.desc||'세계의 기억')).join('')+'</div>'; }
  document.getElementById('equipSlots').innerHTML=html;
  document.querySelectorAll('#equipSlots .item').forEach(el=>el.onclick=()=>toggleEquip(el.dataset.id, el.dataset.slot));
  // 활성 효과 미리보기
  const eff=[]; activeModules().forEach(m=>(m.effects.narrative||[]).forEach(n=>eff.push(n)));
  document.getElementById('equipEffects').innerHTML = eff.length?
    '<h3>현재 적용 효과</h3>'+eff.map(e=>'<p class="muted" style="margin:.3em 0">· '+esc(e)+'</p>').join(''):'';
}
function toggleEquip(id, slot){
  const m=modById[id]; if(!m)return;
  if(slot==='memory'){
    if(W.modules.equipped.includes(id)) W.modules.equipped=W.modules.equipped.filter(x=>x!==id);
    else W.modules.equipped.push(id);
  } else {
    const cur=W.inventory.equipped[slot];
    if(cur===id){ W.inventory.equipped[slot]=null; W.modules.equipped=W.modules.equipped.filter(x=>x!==id); }
    else {
      // 슬롯 교체 + 충돌 해제
      if(cur) W.modules.equipped=W.modules.equipped.filter(x=>x!==cur);
      (m.conflictsWith||[]).forEach(cf=>W.modules.equipped=W.modules.equipped.filter(x=>x!==cf));
      W.inventory.equipped[slot]=id;
      if(!W.modules.equipped.includes(id)) W.modules.equipped.push(id);
    }
    // 해금 효과 적용
    (m.effects.unlocks||[]).forEach(u=>{ if(u in W.flags) W.flags[u]=true; });
  }
  saveRun(); renderEquip(); renderRail();
}

/* ============ 설정 모달 (모델 카드 + 직접 입력) ============ */
let SETDRAFT=null;  // 모달 작업 드래프트
function openSettings(){
  SETDRAFT={provider:API.provider, endpoint:API.endpoint||'', model:API.model||'mock',
            key:(API.keys&&API.keys[API.provider])||API.key||''};
  // 카탈로그에 없는 현재 모델이면 고급 영역을 펼쳐 노출
  document.getElementById('setAdv').open = !modelMeta(SETDRAFT.model);
  renderModelList(); syncAdvFields(); syncKeyField();
  document.getElementById('modal').classList.add('on');
}
function renderModelList(){
  const wrap=document.getElementById('modelList'); wrap.innerHTML='';
  MODELS.forEach(m=>{
    const sel = m.id===SETDRAFT.model;
    const el=document.createElement('div'); el.className='mcard'+(sel?' sel':'');
    el.innerHTML='<div class="mc-main"><div class="mc-top"><b>'+esc(m.label)+'</b>'
      +(m.rec?'<span class="mc-rec">추천</span>':'')+'</div>'
      +'<div class="mc-tag">'+esc(PROVIDER_KR[m.provider]||m.provider)+'</div>'
      +'<div class="mc-desc">'+esc(m.desc)+'</div></div>'
      +'<div class="mc-check">'+(sel?'✓':'')+'</div>';
    el.onclick=()=>selectModel(m.id);
    wrap.appendChild(el);
  });
}
function selectModel(id){
  const m=modelMeta(id); if(!m) return;
  SETDRAFT.provider=m.provider; SETDRAFT.model=m.id; SETDRAFT.endpoint='';
  SETDRAFT.key=(API.keys&&API.keys[m.provider])||'';
  document.getElementById('setAdv').open=false;
  renderModelList(); syncAdvFields(); syncKeyField();
}
function syncAdvFields(){
  document.getElementById('setProvider').value=SETDRAFT.provider;
  document.getElementById('setEndpoint').value=SETDRAFT.endpoint||'';
  document.getElementById('setEndpoint').placeholder=(PRESETS[SETDRAFT.provider]||{}).ep||'(불필요)';
  document.getElementById('setModel').value=SETDRAFT.model||'';
}
function syncKeyField(){
  const isMock=SETDRAFT.provider==='mock';
  document.getElementById('setKeyWrap').style.display=isMock?'none':'block';
  document.getElementById('setKeyLabel').textContent='아카식 개인 식별자 · A.P.I.  ('+(PROVIDER_KR[SETDRAFT.provider]||'API')+' 키)';
  document.getElementById('setKey').value=SETDRAFT.key||'';
  const has=!!(API.keys&&API.keys[SETDRAFT.provider]);
  document.getElementById('setKeyHint').textContent = isMock?'' : (has?'저장된 키가 있습니다 · 비우면 유지됩니다':'이 모델을 쓰려면 키가 필요합니다');
}
function saveSettings(){
  // 고급 영역 값 반영(직접 입력 우선)
  SETDRAFT.provider=document.getElementById('setProvider').value;
  SETDRAFT.endpoint=document.getElementById('setEndpoint').value.trim();
  const mv=document.getElementById('setModel').value.trim();
  if(mv) SETDRAFT.model=mv;
  const kv=document.getElementById('setKey').value.trim();
  API.provider=SETDRAFT.provider;
  API.endpoint=SETDRAFT.endpoint;
  API.model=SETDRAFT.model||(PRESETS[API.provider]||{}).model||'mock';
  if(API.provider!=='mock'){
    if(kv){ API.keys[API.provider]=kv; }            // 새 키 저장
    API.key=API.keys[API.provider]||'';             // 기존 키 유지
  } else { API.key=''; }
  saveApi(); renderModelChip();
  document.getElementById('modal').classList.remove('on');
}
function renderModelChip(){
  const c=document.getElementById('modelChip'); if(!c) return;
  c.querySelector('.mchip-name').textContent=shortModelLabel();
}

/* ============ 모듈 가져오기 (이미지+메타데이터) ============ */
function importModules(){
  const raw=document.getElementById('impArea').value.trim(); if(!raw)return;
  let data; try{ data=JSON.parse(raw); }catch(e){ alert('JSON 파싱 실패: '+e.message); return; }
  const arr=Array.isArray(data)?data:[data];
  const extra=loadExtraMods(); let added=0;
  arr.forEach(m=>{ if(!m||!m.id||!m.title) return;
    m.type=m.type||'item'; m.requires=m.requires||[];
    m.effects=m.effects||{narrative:[],state:[],unlocks:[]};
    registerMod(m);
    const i=extra.findIndex(x=>x.id===m.id); if(i>=0)extra[i]=m; else extra.push(m);
    if(W && !W.inventory.owned.includes(m.id)) W.inventory.owned.push(m.id);
    added++; });
  localStorage.setItem('playMods', JSON.stringify(extra));
  if(W) saveRun();
  document.getElementById('impModal').classList.remove('on');
  document.getElementById('impArea').value='';
  if(document.querySelector('#view-equip.active')) renderEquip();
  alert(added?(added+'개 모듈을 인벤토리에 추가했습니다.'):'추가할 유효한 모듈이 없습니다 (필수: id, title).');
}

/* ============ boot ============ */
function boot(){
  document.getElementById('navPlay').onclick=()=>show('play');
  document.getElementById('navStatus').onclick=()=>show('status');
  document.getElementById('navEquip').onclick=()=>show('equip');
  document.getElementById('navWiki').onclick=()=>show('wiki');
  document.getElementById('navStart').onclick=()=>{show('start');renderStart();};
  document.getElementById('btnSettings').onclick=openSettings;
  document.getElementById('setClose').onclick=()=>document.getElementById('modal').classList.remove('on');
  document.getElementById('qlipClose').onclick=()=>document.getElementById('qlipModal').classList.remove('on');
  document.getElementById('setSave').onclick=saveSettings;
  // 고급(직접 입력) 필드 → 드래프트 동기화
  document.getElementById('setProvider').onchange=function(){ SETDRAFT.provider=this.value; SETDRAFT.endpoint=''; SETDRAFT.key=(API.keys&&API.keys[this.value])||''; syncAdvFields(); syncKeyField(); renderModelList(); };
  document.getElementById('setEndpoint').oninput=function(){ SETDRAFT.endpoint=this.value; };
  document.getElementById('setModel').oninput=function(){ SETDRAFT.model=this.value; renderModelList(); };
  document.getElementById('setKey').oninput=function(){ SETDRAFT.key=this.value; };
  document.getElementById('impOpen').onclick=()=>document.getElementById('impModal').classList.add('on');
  document.getElementById('impClose').onclick=()=>document.getElementById('impModal').classList.remove('on');
  document.getElementById('impAdd').onclick=importModules;
  const hw=document.querySelector('.handwrap');
  const pageScroll=dir=>{ if(hw) hw.scrollBy({left:dir*hw.clientWidth*0.72,behavior:'smooth'}); };
  document.getElementById('handPrev').onclick=()=>pageScroll(-1);
  document.getElementById('handNext').onclick=()=>pageScroll(1);
  if(hw) hw.addEventListener('scroll',updateHandNav,{passive:true});
  window.addEventListener('resize',updateHandNav);
  // 모바일: 햄버거 드로어 + 레일 시트
  document.getElementById('navToggle').onclick=()=>document.body.classList.toggle('nav-open');
  document.getElementById('railToggle').onclick=()=>{ renderRail(); document.body.classList.toggle('rail-open'); };
  document.getElementById('scrim').onclick=()=>document.body.classList.remove('nav-open','rail-open');
  document.querySelectorAll('#youMode button').forEach(b=>b.onclick=()=>setYouMode(b.dataset.m));
  { const rb=document.getElementById('randomBtn'); if(rb) rb.onclick=randomizeStart; }
  document.getElementById('startBtn').onclick=()=>{
    if(youMode==='persona'){
      if(!pickPersona||!pickPersona.name||!pickPersona.detail){alert('페르소나의 이름과 상세 정보를 입력하세요.');return;}
      newRun(null, pickC, pickM, {persona:pickPersona, startDistrict, tone:startTone});
    } else {
      if(!pickP){alert('주인공을 선택하세요.');return;}
      newRun(pickP, pickC, pickM, {startDistrict, tone:startTone});
    }
    setRunUi(); renderLog(); show('play'); startPrologue();
  };
  document.getElementById('sendBtn').onclick=()=>{ const i=document.getElementById('userInput');
    const v=i.value; i.value=''; turn(v); };
  document.getElementById('userInput').addEventListener('keydown',e=>{
    if(e.key==='Enter'&&!e.shiftKey){ e.preventDefault(); document.getElementById('sendBtn').click(); }});
  document.getElementById('modelChip').onclick=openSettings;
  document.getElementById('qNarrate').onclick=quickNarrate;
  document.getElementById('qSuggest').onclick=suggestReplies;
  renderModelChip();
  document.getElementById('endRunBtn').onclick=()=>{
    if(!W)return; const got=issueMemories(); saveRun();
    alert(got.length?('회차를 마칩니다. 세계의 기억 발급: '+got.map(g=>(modById[g]||{}).title||g).join(', ')):'회차를 마칩니다. 새로 발급된 기억은 없습니다.');
    show('start'); renderStart();
  };
  setRunUi(); show('start'); renderStart();
}
boot();
"""

HTML_SHELL = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>바벨의 도서관 : 마법소녀 레코드</title>
<style>/*__CSS__*/</style>
</head>
<body>
<div id="app">
  <header id="topbar">
    <button class="tbtn navtoggle" id="navToggle" aria-label="메뉴">☰</button>
    <div class="brand">바벨의 도서관<small>Magical Girl Record</small></div>
    <nav id="nav">
      <button class="navbtn" id="navStart" data-view="start">시작 · 회차</button>
      <button class="navbtn" id="navPlay" data-view="play">플레이</button>
      <button class="navbtn" id="navStatus" data-view="status">스테이터스</button>
      <button class="navbtn" id="navEquip" data-view="equip">장비/복장</button>
      <button class="navbtn" id="navWiki" data-view="wiki">위키</button>
    </nav>
    <span id="topspacer"></span>
    <span id="runtag"></span>
    <button class="tbtn" id="btnSettings" title="API 설정 — 부를 인격 파편(LLM)의 출처·식별자를 정합니다">⚙ 인격 파편 조율</button>
  </header>
  <div id="scrim"></div>
  <main>
    <!-- 시작 / 회차 선택 -->
    <section id="view-start" class="view active">
      <div class="pad">
        <div class="hero">
          <div class="hero-kicker">Babel Library · Magical Girl Record</div>
          <h1 class="hero-title">바벨의 도서관</h1>
          <div class="hero-sub">: 마법소녀 레코드</div>
        </div>
        <div class="card2 pick-card">
          <h3 class="center">‘당신’과 동행 구성</h3>
          <div class="youmode" id="youMode">
            <button type="button" data-m="persona">✦ 관측자</button>
            <button type="button" data-m="canon">마기아</button>
          </div>
          <p class="youmode-desc" id="youModeDesc"></p>
          <div id="personaPanel" class="persona-panel"></div>
          <div class="pickslots" id="pickSlots"></div>
          <div class="ftabs" id="factionTabs"></div>
          <p class="muted center" id="pickHint" style="font-size:12px;margin:10px 0 0"></p>
          <div class="handnav">
            <button class="harrow" id="handPrev" title="이전">‹</button>
            <div class="handwrap"><div class="hand" id="pickHand"></div></div>
            <button class="harrow" id="handNext" title="다음">›</button>
          </div>
          <div class="startset" id="startSet"></div>
        </div>
        <div class="card2">
          <h3>세계의 기억 장착 (NG+)</h3>
          <div class="chips" id="memChips"></div>
        </div>
        <div class="card2">
          <h3>이어하기</h3>
          <div id="saveList"></div>
        </div>
        <div class="row" style="justify-content:center">
          <button class="btn ghost" id="randomBtn" title="주인공·동행·지역·분위기를 무작위로 구성합니다">🎲 랜덤 구성</button>
          <button class="btn" id="startBtn">이 구성으로 시작 ▶</button>
          <button class="btn ghost" id="btnSettings2" onclick="document.getElementById('btnSettings').click()">먼저 인격 파편 조율</button>
        </div>
        <div class="warn">아카식 개인 식별자(A.P.I. — API 키)는 이 브라우저(localStorage)에만 깃들고, 선택한 차원 좌표(엔드포인트)로만 직접 전송됩니다. 개인용 식별자를 쓰고, 공용 PC에서는 사용 후 지우세요. 로컬 차원 좌표(Ollama·LM Studio 등)는 CORS 허용이 필요합니다. 식별자 없이도 <b>환영(mock)</b>으로 흐름을 체험할 수 있습니다.</div>
      </div>
    </section>

    <!-- 플레이 -->
    <section id="view-play" class="view">
      <button id="railToggle" class="railtoggle" aria-label="관계 보기">관계 ▸</button>
      <div id="playmain">
        <div id="log"></div>
        <div id="composer">
          <div id="choices"></div>
          <div class="actbar">
            <button class="mchip" id="modelChip" title="AI 모델 선택"><span class="mchip-ic">✦</span><span class="mchip-name">모델</span><span class="mchip-cv">⌄</span></button>
            <button class="qbtn" id="qNarrate" title="플레이어 입력 없이 장면을 이어 묘사">✶ 상황묘사</button>
            <button class="qbtn" id="qSuggest" title="취할 만한 행동 후보 제안">✦ 추천답변</button>
          </div>
          <div id="hud" class="hud"></div>
          <div class="inwrap">
            <textarea id="userInput" class="tin" placeholder="행동이나 대사를 입력… (Enter 전송 · Shift+Enter 줄바꿈)"></textarea>
            <button class="btn" id="sendBtn">전송</button>
          </div>
        </div>
      </div>
      <aside id="rail">
        <h4>호감도</h4>
        <div id="railList"></div>
        <div style="margin-top:18px"><button class="btn ghost" id="endRunBtn" style="width:100%">회차 종료 · 기억 발급</button></div>
      </aside>
    </section>

    <!-- 스테이터스 -->
    <section id="view-status" class="view">
      <div class="pad">
        <div class="kicker">Status</div>
        <h2 class="title">스테이터스 창</h2>
        <div class="recap" id="statusRecap"></div>
        <div class="status-wrap"><div class="slist" id="statusList"></div><div class="sdetail" id="statusDetail"></div></div>
      </div>
    </section>

    <!-- 장비/복장 -->
    <section id="view-equip" class="view">
      <div class="pad">
        <div class="kicker">Equipment</div>
        <h2 class="title">장비 · 복장</h2>
        <div class="equip-wrap">
          <div class="portrait" id="equipPortrait"></div>
          <div>
            <div class="inv-tools"><button class="btn ghost" id="impOpen">＋ 모듈 가져오기</button></div>
            <div id="equipSlots"></div>
            <div id="equipEffects"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- 위키 (격리 iframe 임베드) -->
    <section id="view-wiki" class="view">
      <iframe id="wikiFrame" title="마법소녀 세계관 위키"></iframe>
    </section>
  </main>
</div>

<!-- 세피로트(클리포트 억지력) 모달 -->
<div id="qlipModal">
  <div class="mbox">
    <span class="close" id="qlipClose">×</span>
    <h3>클리포트 억지력 <span style="font-size:13px;color:var(--ink-faint);font-weight:400">세피로트 분해</span></h3>
    <div id="qlipBody"></div>
  </div>
</div>

<!-- 설정 모달 -->
<div id="modal">
  <div class="mbox">
    <span class="close" id="setClose">×</span>
    <h3>인격 파편 조율 <span style="font-size:13px;color:var(--ink-faint);font-weight:400" title="API 설정 — 외부 LLM 연결">(AI 모델 · 연결 설정)</span></h3>
    <p class="muted" style="font-size:12px;margin:.1em 0 12px">불러올 인격 파편(AI 모델)을 고르고, 본인 식별자(API 키)를 새긴다.</p>
    <label class="fld"><span class="tip" data-tip="AI 모델 — 어떤 LLM으로 이야기를 생성할지">파편의 위계 <span style="opacity:.6">(AI 모델)</span></span></label>
    <div id="modelList" class="mlist"></div>
    <div id="setKeyWrap">
      <label class="fld"><span class="tip" data-tip="API 키 — Application Programming Interface Key. 본인 키를 입력하세요(이 브라우저에만 저장)" id="setKeyLabel">아카식 개인 식별자 · A.P.I. (API 키)</span></label>
      <input class="tin" id="setKey" type="password" placeholder="이 브라우저에만 깃듭니다">
      <div class="muted" id="setKeyHint" style="font-size:11px;margin-top:4px"></div>
    </div>
    <details id="setAdv" class="adv">
      <summary><span class="tip" data-tip="직접 입력 — 카탈로그에 없는 모델/로컬·타사 엔드포인트(OpenRouter·Ollama·LM Studio 등)">직접 입력 · 고급</span></summary>
      <label class="fld"><span class="tip" data-tip="프로바이더 — 어떤 LLM 서비스를 쓸지">권능의 출처 (프로바이더)</span></label>
      <select class="tin" id="setProvider">
        <option value="mock">환영(幻影) · 시연 — 키 불필요</option>
        <option value="anthropic">Anthropic · Claude</option>
        <option value="openai">OpenAI 호환</option>
        <option value="gemini">Google Gemini</option>
      </select>
      <label class="fld"><span class="tip" data-tip="엔드포인트 URL — 비우면 프로바이더 기본값">차원 좌표 (엔드포인트) <span style="opacity:.6">(비우면 기본)</span></span></label>
      <input class="tin" id="setEndpoint" placeholder="">
      <label class="fld"><span class="tip" data-tip="모델 ID (예: claude-opus-4-8, gemini-3.1-pro, gemini-3.5-flash, gpt-5.5, openrouter 모델명)">모델 ID</span></label>
      <input class="tin" id="setModel" placeholder="모델 ID">
      <div class="warn" style="margin-top:8px">OpenAI 호환은 <code>/chat/completions</code> 전체 URL을, Gemini는 <code>.../v1beta/models</code> 기본 URL을 엔드포인트로 씁니다.</div>
    </details>
    <div class="warn">식별자는 localStorage에 깃들어 선택한 엔드포인트로만 직접 전송됩니다.</div>
    <div class="row" style="margin-top:14px"><button class="btn" id="setSave">새기기</button></div>
  </div>
</div>

<!-- 모듈 가져오기 모달 -->
<div id="impModal">
  <div class="mbox">
    <span class="close" id="impClose">×</span>
    <h3>모듈 가져오기</h3>
    <p class="muted" style="font-size:12px;margin:.2em 0 8px">이미지·메타데이터가 담긴 모듈 JSON을 붙여넣어 인벤토리에 추가합니다. 단일 객체 또는 배열.</p>
    <textarea class="tin" id="impArea" rows="9" spellcheck="false" placeholder='{
  "id": "item-moonlit-charm",
  "type": "item",
  "slot": "accessory",
  "title": "월광 부적",
  "img": "data:image/webp;base64,...",
  "effects": { "narrative": ["은은한 월광이 주인공을 감싼다."] }
}'></textarea>
    <div class="warn">필수: <code>id</code>, <code>title</code>. 선택: <code>type</code>(outfit·equipment·item·memory) · <code>slot</code> · <code>img</code>(data URI) · <code>effects.narrative[]</code>. 추가된 모듈은 이 브라우저에 저장되어 이후 회차에서도 인벤토리에 나타납니다.</div>
    <div class="row" style="margin-top:12px"><button class="btn" id="impAdd">인벤토리에 추가</button></div>
  </div>
</div>

<script id="canon" type="application/json">__CANON__</script>
<script id="world" type="application/json">__WORLD__</script>
<script id="assets" type="application/json">__ASSETS__</script>
<script id="wikidoc" type="application/json">__WIKIDOC__</script>
<script>/*__JS__*/</script>
</body>
</html>
"""


# 임베드 위키(iframe)용 플럼 테마 오버라이드 — 위키 세피아 토큰을 플레이 팔레트로 통일.
# (wiki_template.page(..., extra_css=)로 위키 CSS 뒤에 append → 나중 선언이 이김)
WIKI_THEME_CSS = r"""
/* === 플레이 앱 플럼 통일 (임베드 위키) === */
:root{
  --bg:#160a22; --bg2:#1e0f30; --panel:#2a0f38; --panel2:#3a1a50;
  --ink:#ece2f6; --ink-dim:#bcaad6; --ink-faint:#8d7ab0;
  --gold:#b98cff; --gold-bright:#d9c4ff; --gold-deep:#6e4fa0;
  --line:#4a2f6b; --line-soft:#33214d;
  --rep:#d9b65f; --bureau:#7fb6ff; --trainee:#8fd0a8;
  --shikoku:#d98fc9; --refusal:#e87a8c; --villain:#b98cff; --guest:#a89ac0;
  --shadow:0 12px 40px rgba(8,2,18,.6);
}
body{ background: radial-gradient(135% 95% at 50% -8%, #34184f 0%, #2a0f38 38%, var(--bg) 72%, #170b25 100%); }
::-webkit-scrollbar-thumb{ background:#3a2350; border:2px solid var(--bg); }
.fc-rep{--c:#d9b65f}.fc-bureau{--c:#7fb6ff}.fc-trainee{--c:#8fd0a8}
.fc-shikoku{--c:#d98fc9}.fc-refusal{--c:#e87a8c}.fc-villain{--c:#b98cff}
.fc-guest{--c:#a89ac0}.fc-other{--c:#a89ac0}
"""


def page(canon_json, world_json, assets_json, wikidoc_json="null"):
    css = CSS.replace("__NOISE__", NOISE)
    js = JS
    safe = lambda s: s.replace("</", "<\\/")
    html = (HTML_SHELL
            .replace("/*__CSS__*/", css)
            .replace("/*__JS__*/", js)
            .replace("__CANON__", safe(canon_json))
            .replace("__WORLD__", safe(world_json))
            .replace("__ASSETS__", safe(assets_json))
            .replace("__WIKIDOC__", safe(wikidoc_json)))
    return html
