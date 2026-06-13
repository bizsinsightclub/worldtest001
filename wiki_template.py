# -*- coding: utf-8 -*-
"""HTML/CSS/JS 템플릿. build_wiki.py 가 DATA(JSON)를 주입해 단일 HTML 을 만든다."""

# 종이 질감 노이즈 (작은 SVG feTurbulence, data-uri)
NOISE = ("data:image/svg+xml;base64,"
         "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNjAiIGhl"
         "aWdodD0iMTYwIj48ZmlsdGVyIGlkPSJuIj48ZmVUdXJidWxlbmNlIHR5cGU9ImZyYWN0YWxO"
         "b2lzZSIgYmFzZUZyZXF1ZW5jeT0iMC44IiBudW1PY3RhdmVzPSIyIiBzdGl0Y2hUaWxlcz0i"
         "c3RpdGNoIi8+PC9maWx0ZXI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmls"
         "dGVyPSJ1cmwoI24pIiBvcGFjaXR5PSIwLjYiLz48L3N2Zz4=")

CSS = r"""
:root{
  --bg:#16110b; --bg2:#1f1810; --panel:#241c12; --panel2:#2c2216;
  --ink:#ece0c8; --ink-dim:#b6a784; --ink-faint:#8a7a5c;
  --gold:#c9a24b; --gold-bright:#e6c879; --gold-deep:#8a6d2c;
  --line:#3d3019; --line-soft:#2b2114;
  --rep:#d9b65f; --bureau:#6fb1c4; --trainee:#8fc08a;
  --shikoku:#c77dbb; --refusal:#d2705a; --villain:#9a7bd0; --guest:#9a8e76;
  --shadow:0 8px 30px rgba(0,0,0,.55);
}
*{box-sizing:border-box}
html,body{margin:0;height:100%}
body{
  background:
    radial-gradient(120% 80% at 50% -10%, #2a2013 0%, var(--bg) 55%, #0d0a06 100%);
  color:var(--ink);
  font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',system-ui,sans-serif;
  font-size:15px; line-height:1.6; overflow:hidden;
}
body::before{ /* 종이 질감 */
  content:""; position:fixed; inset:0; pointer-events:none; z-index:9999;
  background-image:url('__NOISE__'); background-size:160px; opacity:.05;
  mix-blend-mode:overlay;
}
body::after{ /* 비네팅 */
  content:""; position:fixed; inset:0; pointer-events:none; z-index:9998;
  box-shadow:inset 0 0 220px 60px rgba(0,0,0,.65);
}
h1,h2,h3,.serif{font-family:'Iowan Old Style','Palatino Linotype','Book Antiqua',Palatino,'Nanum Myeongjo',Georgia,serif;}
::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-thumb{background:#3a2d18;border-radius:6px;border:2px solid var(--bg)}
::-webkit-scrollbar-track{background:transparent}

/* ---- 팩션 색 클래스 ---- */
.fc-rep{--c:#e0bd5c}.fc-bureau{--c:#5fc0d6}.fc-trainee{--c:#84cf86}
.fc-shikoku{--c:#d98fc9}.fc-refusal{--c:#e87a55}.fc-villain{--c:#a98be6}
.fc-guest{--c:#a89a80}.fc-other{--c:#a89a80}

/* ---- 루비 ---- */
ruby{ruby-position:over}
rt{font-size:.5em;color:var(--gold);letter-spacing:.04em;font-weight:600}
.sub{display:block;font-size:.62em;color:var(--ink-faint);letter-spacing:.05em;
  font-family:'Iowan Old Style',Palatino,serif;font-style:italic;margin-top:2px}

/* ---- 레이아웃 ---- */
#app{display:grid;grid-template-columns:264px 1fr;grid-template-rows:64px 1fr;
  height:100vh;}
#topbar{grid-column:1/3;display:flex;align-items:center;gap:18px;padding:0 22px;
  border-bottom:1px solid var(--line);
  background:linear-gradient(180deg,#241b10,#1a140c);
  box-shadow:0 2px 18px rgba(0,0,0,.5);z-index:50}
.brand{font-size:20px;font-weight:700;letter-spacing:.02em;color:var(--gold-bright);
  text-shadow:0 1px 0 #000; white-space:nowrap}
.brand small{display:block;font-size:10px;letter-spacing:.34em;color:var(--ink-faint);
  font-weight:400;text-transform:uppercase}
#search{margin-left:auto;position:relative}
#search input{background:#120d07;border:1px solid var(--line);color:var(--ink);
  padding:9px 14px 9px 34px;border-radius:20px;width:260px;font-size:13px;outline:none}
#search input:focus{border-color:var(--gold-deep);box-shadow:0 0 0 2px rgba(201,162,75,.15)}
#search .ic{position:absolute;left:11px;top:8px;color:var(--ink-faint)}
#searchResults{position:absolute;top:42px;right:0;width:330px;max-height:60vh;overflow:auto;
  background:var(--panel);border:1px solid var(--line);border-radius:10px;
  box-shadow:var(--shadow);display:none;z-index:100}
#searchResults a{display:flex;gap:10px;align-items:center;padding:8px 12px;
  color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line-soft)}
#searchResults a:hover{background:var(--panel2)}
#searchResults img{width:30px;height:30px;border-radius:5px;object-fit:cover;object-position:top}
#searchResults .k{font-size:11px;color:var(--ink-faint)}

/* ---- 사이드바 ---- */
#side{border-right:1px solid var(--line);background:linear-gradient(180deg,#1c150d,#15100a);
  padding:14px 10px;overflow-y:auto}
.navsec{margin-bottom:6px}
.navbtn{display:flex;align-items:center;gap:11px;width:100%;text-align:left;
  background:none;border:none;color:var(--ink-dim);padding:10px 12px;border-radius:8px;
  font-size:14px;cursor:pointer;font-family:inherit;letter-spacing:.01em}
.navbtn .ic{width:20px;text-align:center;font-size:15px;opacity:.85}
.navbtn:hover{background:var(--panel);color:var(--ink)}
.navbtn.active{background:linear-gradient(90deg,rgba(201,162,75,.18),transparent);
  color:var(--gold-bright);box-shadow:inset 2px 0 0 var(--gold)}
.navsub{margin:2px 0 8px 10px;border-left:1px solid var(--line-soft);padding-left:6px;display:none}
.navsub.open{display:block}
.navsub a{display:block;color:var(--ink-faint);text-decoration:none;font-size:12.5px;
  padding:5px 10px;border-radius:6px;cursor:pointer}
.navsub a:hover{color:var(--ink);background:var(--panel)}
.sideband{font-size:10px;letter-spacing:.28em;color:var(--ink-faint);
  text-transform:uppercase;padding:14px 12px 6px}

/* ---- 메인 ---- */
#main{overflow:auto;position:relative}
.view{display:none;height:100%}
.view.active{display:block}
.pad{padding:26px 32px}

/* ---- 도감(코덱스) ---- */
#view-codex{display:none;grid-template-columns:minmax(380px,460px) 1fr;height:100%}
#view-codex.active{display:grid}
#detail{border-right:1px solid var(--line);overflow:auto;position:relative;
  background:radial-gradient(120% 60% at 50% 0,#241a0f,#140f08)}
.dt-hero{position:relative;height:62%;min-height:430px;overflow:hidden}
.dt-hero .bgwash{position:absolute;inset:0;
  background:radial-gradient(80% 70% at 50% 30%,rgba(201,162,75,.10),transparent 70%)}
.dt-hero img{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
  height:104%;filter:drop-shadow(0 20px 40px rgba(0,0,0,.6))}
.dt-hero .fade{position:absolute;inset:0;
  background:linear-gradient(180deg,transparent 55%,#140f08 99%)}
.dt-stars{position:absolute;top:16px;left:20px;font-size:15px;color:var(--gold-bright);
  letter-spacing:2px;text-shadow:0 1px 3px #000;z-index:3}
.imgtoggle{position:absolute;top:14px;right:16px;z-index:4;display:flex;gap:4px;
  background:rgba(10,8,5,.6);border:1px solid var(--line);border-radius:18px;padding:3px}
.imgtoggle button{background:none;border:none;color:var(--ink-dim);font-size:11px;
  padding:5px 12px;border-radius:14px;cursor:pointer;font-family:inherit}
.imgtoggle button.on{background:var(--gold);color:#1a1209;font-weight:700}
.dt-body{padding:0 26px 30px}
.dt-name{font-size:30px;font-weight:700;line-height:1.15;margin:-46px 0 2px;position:relative;z-index:3;
  text-shadow:0 2px 8px #000}
.dt-stage{color:var(--gold);font-size:15px;margin-bottom:4px}
.faction-chip{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:700;
  padding:7px 16px;border-radius:16px;color:var(--c);border:1.5px solid var(--c);
  background:color-mix(in srgb,var(--c) 16%,transparent);margin-bottom:16px;letter-spacing:.02em}
.faction-chip::before{content:"";width:10px;height:10px;border-radius:50%;background:var(--c);
  box-shadow:0 0 9px var(--c)}
.statgrid{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line-soft);
  border:1px solid var(--line);border-radius:10px;overflow:hidden;margin-bottom:16px}
.stat{background:var(--panel);padding:10px 14px}
.stat .l{font-size:10.5px;letter-spacing:.12em;color:var(--ink-faint);text-transform:uppercase}
.stat .v{font-size:14px;color:var(--ink);margin-top:2px}
.tagline{font-style:italic;color:var(--ink-dim);border-left:2px solid var(--gold-deep);
  padding:6px 0 6px 14px;margin:14px 0;font-size:13.5px}
.detailbtn{display:block;width:100%;text-align:center;margin-top:8px;
  background:linear-gradient(180deg,#e6c879,#c9a24b);color:#1a1209;font-weight:700;
  border:none;padding:13px;border-radius:8px;cursor:pointer;font-family:inherit;
  letter-spacing:.06em;font-size:14px;box-shadow:0 4px 14px rgba(201,162,75,.25)}
.detailbtn:hover{filter:brightness(1.08)}
.dt-empty{display:flex;align-items:center;justify-content:center;height:100%;
  color:var(--ink-faint);text-align:center;padding:40px}

/* ---- 컬렉션 그리드 ---- */
#collection{overflow:auto;padding:18px 22px}
.coltools{display:flex;align-items:center;gap:14px;margin-bottom:16px;flex-wrap:wrap}
.coltools .label{font-size:11px;letter-spacing:.2em;color:var(--ink-faint);text-transform:uppercase}
.filterbtn{display:inline-flex;align-items:center;gap:7px;background:var(--panel);
  border:1px solid var(--line);color:var(--ink-dim);
  padding:7px 14px;border-radius:16px;font-size:12.5px;cursor:pointer;font-family:inherit}
.filterbtn[data-f]:not([data-f="all"])::before{content:"";width:8px;height:8px;border-radius:50%;
  background:var(--c,var(--gold));box-shadow:0 0 6px var(--c,var(--gold))}
.filterbtn:hover{border-color:var(--c,var(--gold-deep));color:var(--ink)}
.filterbtn.on{background:var(--c,var(--gold));color:#1a1209;border-color:var(--c,var(--gold));font-weight:700}
.filterbtn.on::before{background:#1a1209;box-shadow:none}
.colcount{margin-left:auto;font-size:12px;color:var(--ink-faint)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(124px,1fr));gap:14px}
.card{position:relative;border-radius:10px;overflow:hidden;cursor:pointer;
  background:var(--panel);border:1px solid var(--line);border-top:3px solid var(--c);
  aspect-ratio:3/4;transition:transform .14s,box-shadow .14s,border-color .14s}
.card:hover{transform:translateY(-4px);box-shadow:var(--shadow);border-color:var(--gold-deep);
  border-top-color:var(--c)}
.card.sel{border-color:var(--gold);border-top-color:var(--c);box-shadow:0 0 0 2px rgba(201,162,75,.4)}
.card img{width:100%;height:100%;object-fit:cover;object-position:top center}
.card .noimg{display:flex;align-items:center;justify-content:center;height:100%;
  color:var(--ink-faint);font-size:34px;font-family:serif}
.card .cap{position:absolute;left:0;right:0;bottom:0;padding:18px 9px 8px;
  background:linear-gradient(180deg,transparent,rgba(8,6,3,.94));}
.card .cap .nm{font-size:12.5px;font-weight:700;line-height:1.2}
.card .cap .en{font-size:9.5px;color:var(--ink-faint);letter-spacing:.03em}
.card .badge{position:absolute;top:6px;left:7px;font-size:10px;color:var(--gold-bright);
  text-shadow:0 1px 2px #000;letter-spacing:1px}
.card .fdot{position:absolute;top:8px;right:8px;width:9px;height:9px;border-radius:50%;
  box-shadow:0 0 6px currentColor}
.subhead{grid-column:1/-1;font-size:13px;letter-spacing:.18em;color:var(--gold);
  text-transform:uppercase;border-bottom:1px solid var(--line);padding:14px 0 6px;margin-top:6px}

/* ---- 모달 ---- */
#modal{position:fixed;inset:0;background:rgba(6,4,2,.82);z-index:500;display:none;
  align-items:center;justify-content:center;padding:40px}
#modal.open{display:flex}
.modal-box{background:var(--panel);border:1px solid var(--gold-deep);border-radius:14px;
  max-width:780px;width:100%;max-height:86vh;overflow:auto;box-shadow:var(--shadow);
  position:relative}
.modal-box .mhead{display:flex;gap:18px;padding:22px 26px;border-bottom:1px solid var(--line);
  position:sticky;top:0;background:linear-gradient(180deg,#2a2013,#241c12);z-index:2}
.modal-box .mhead img{width:90px;height:120px;object-fit:cover;object-position:top;
  border-radius:8px;border:1px solid var(--line)}
.modal-close{position:absolute;top:14px;right:16px;background:none;border:none;
  color:var(--ink-dim);font-size:24px;cursor:pointer;z-index:3}
.md{padding:8px 28px 30px}
.md h2{font-size:19px;color:var(--gold-bright);border-bottom:1px solid var(--line);
  padding-bottom:5px;margin:22px 0 10px}
.md h3{font-size:16px;color:var(--gold);margin:18px 0 8px}
.md h4{font-size:13px;letter-spacing:.12em;color:var(--ink-dim);text-transform:uppercase;
  margin:16px 0 6px}
.md p{margin:8px 0;color:var(--ink-dim)}
.md ul{margin:8px 0;padding-left:20px}
.md li{margin:4px 0;color:var(--ink-dim)}
.md strong{color:var(--ink)}
.md em{color:var(--gold)}

/* ---- 로어 페이지 ---- */
#view-lore .lore-wrap{max-width:820px;margin:0 auto}
.page-title{font-size:30px;color:var(--gold-bright);margin:0 0 4px}
.page-kicker{font-size:11px;letter-spacing:.28em;color:var(--ink-faint);
  text-transform:uppercase;margin-bottom:18px}

/* ---- 관계도 ---- */
#view-graph{display:none;grid-template-columns:1fr 330px;height:100%}
#view-graph.active{display:grid}
#graphStage{position:relative;overflow:hidden;
  background:radial-gradient(80% 80% at 50% 42%,#211810,#15100a 70%,#0d0a06)}
#graphCanvas{display:block;width:100%;height:100%;cursor:grab}
#graphCanvas:active{cursor:grabbing}
.graph-tools{position:absolute;top:16px;left:18px;z-index:5;display:flex;gap:6px;flex-wrap:wrap;
  max-width:66%}
#graphTip{position:absolute;pointer-events:none;background:rgba(12,9,5,.95);
  border:1px solid var(--gold-deep);border-radius:8px;padding:9px 12px;max-width:300px;
  font-size:12px;color:var(--ink);display:none;z-index:6;box-shadow:var(--shadow)}
#graphTip b{color:var(--gold-bright)}
#graphPanel{border-left:1px solid var(--line);background:var(--panel);overflow:auto;padding:20px}
#graphPanel .gp-hint{color:var(--ink-faint);font-size:12.5px;line-height:1.7}
#graphPanel .gp-head{display:flex;gap:12px;align-items:center;margin-bottom:6px}
#graphPanel .gp-head img{width:56px;height:56px;border-radius:8px;object-fit:cover;object-position:top;
  border:1px solid var(--line)}
#graphPanel .gp-head .nm{font-size:18px;font-weight:700}
#graphPanel .gp-head .en{font-size:11px;color:var(--ink-faint)}
.gp-sec{font-size:11px;letter-spacing:.18em;color:var(--gold);text-transform:uppercase;
  margin:16px 0 8px;border-bottom:1px solid var(--line);padding-bottom:4px}
.gp-rel{padding:9px 0;border-bottom:1px solid var(--line-soft);cursor:pointer}
.gp-rel:hover{background:var(--panel2)}
.gp-rel .top{display:flex;align-items:center;gap:8px;margin-bottom:3px}
.gp-rel .tgt{font-size:13.5px;font-weight:600;color:var(--ink)}
.rel-badge{font-size:10px;padding:1px 8px;border-radius:9px;color:#15100a;font-weight:700}
.gp-rel .desc{font-size:12px;color:var(--ink-dim);line-height:1.5}
.gp-legend{display:flex;flex-wrap:wrap;gap:8px 14px;margin-top:8px}
.gp-legend .li{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--ink-dim)}
.gp-legend .sw{width:16px;height:3px;border-radius:2px}
.gp-back{margin-top:14px;background:none;border:1px solid var(--gold-deep);color:var(--gold-bright);
  padding:8px 14px;border-radius:8px;cursor:pointer;font-family:inherit;font-size:12.5px;width:100%}
.gp-back:hover{background:rgba(201,162,75,.12)}

/* ---- 지도 ---- */
#view-map{display:none;grid-template-columns:1fr 340px;height:100%}
#view-map.active{display:grid}
#mapStage{position:relative;overflow:hidden;
  background:radial-gradient(80% 80% at 45% 40%,#1a2733 0%,#10141b 60%,#0b0d12 100%)}
#mapStage svg{width:100%;height:100%}
.district{cursor:pointer}
.district .reg{fill:var(--dc);stroke:#10130f;stroke-width:.5;
  transition:filter .15s;filter:saturate(.85) brightness(.92)}
.district:hover .reg{filter:saturate(1.1) brightness(1.3)}
.district.sel .reg{stroke:var(--gold-bright);stroke-width:1.4;filter:saturate(1.15) brightness(1.25)
  drop-shadow(0 0 5px rgba(230,200,121,.5))}
.district.sealed .reg{fill:#3a1a28;stroke:#7a3a5e;stroke-width:.9;stroke-dasharray:3 2;
  filter:brightness(.9)}
.dlabel{pointer-events:none}
.dlabel .lbl{fill:#e3d6ba;font-size:11px;font-weight:600;text-anchor:middle;opacity:.78;
  font-family:'Pretendard',sans-serif;paint-order:stroke;stroke:#0c0f0a;stroke-width:2.6px;
  stroke-linejoin:round;transition:font-size .12s,opacity .12s,fill .12s}
.dlabel.sel .lbl{fill:var(--gold-bright);font-size:14px;opacity:1;font-weight:700}
.dlabel[data-d="Shikoku"] .lbl{fill:#d98fc9;opacity:.95}
.seal-mark{font-size:20px;text-anchor:middle;fill:#d98fc9;pointer-events:none;
  paint-order:stroke;stroke:#0c0f0a;stroke-width:3px}
#mapInfo{border-left:1px solid var(--line);background:var(--panel);overflow:auto;padding:22px}
#mapInfo h2{color:var(--gold-bright);margin:0 0 2px;font-size:22px}
#mapInfo .mi-sub{color:var(--ink-faint);font-size:12px;letter-spacing:.1em;margin-bottom:14px}
.mi-role{font-size:11px;letter-spacing:.2em;color:var(--gold);text-transform:uppercase;
  margin:16px 0 6px;border-bottom:1px solid var(--line);padding-bottom:4px}
.mi-char{display:flex;gap:11px;align-items:center;padding:7px 6px;border-radius:8px;cursor:pointer}
.mi-char:hover{background:var(--panel2)}
.mi-char img{width:42px;height:42px;border-radius:6px;object-fit:cover;object-position:top}
.mi-char .nm{font-size:13px;font-weight:600}
.mi-char .rk{font-size:11px;color:var(--ink-faint)}

/* ---- 연표 (세로, 현재=위 → 과거=아래, 불에 새겨지듯) ---- */
#view-timeline .pad{max-width:860px;margin:0 auto}
.tl-hint{font-size:11.5px;color:var(--ink-faint);margin:2px 0 22px;letter-spacing:.04em}
.tl-v{position:relative;padding:10px 0 80px}
.tl-v::before{content:"";position:absolute;left:31px;top:6px;bottom:40px;width:2px;
  background:linear-gradient(180deg,#ffd98a,var(--gold) 8%,var(--gold-deep) 55%,#2a2012);
  box-shadow:0 0 10px rgba(230,168,58,.35)}
.tl-row{position:relative;padding:0 0 56px 76px;opacity:1}
.tl-row .node{position:absolute;left:22px;top:3px;width:19px;height:19px;border-radius:50%;
  background:radial-gradient(circle at 40% 35%,#ffe6a8,#c9a24b 70%);
  box-shadow:0 0 0 4px rgba(201,162,75,.12),0 0 14px #e6a83a;z-index:2}
.tl-row .when{font-size:12px;letter-spacing:.12em;color:var(--gold)}
.tl-row h3{font-family:'Iowan Old Style',Palatino,'Nanum Myeongjo',Georgia,serif;
  font-size:25px;margin:3px 0 1px;color:var(--gold-bright);text-shadow:0 0 6px rgba(230,168,58,.25)}
.tl-row .en{font-size:12px;font-style:italic;color:var(--ink-faint);margin-bottom:9px}
.tl-row p{margin:0;font-size:14px;color:var(--ink-dim);line-height:1.65;max-width:680px;
  border-left:1px solid var(--line);padding-left:16px}
.tl-row.present h3{color:#fff0cf}
.tl-row.present .node{background:radial-gradient(circle,#fff,#ffd98a);
  box-shadow:0 0 0 5px rgba(230,200,121,.2),0 0 22px #ffcf6a}

@media (prefers-reduced-motion: no-preference){
  .tl-row{opacity:.12;transform:translateY(26px);transition:opacity .8s ease,transform .8s ease}
  .tl-row.in{opacity:1;transform:none}
  .tl-row.in h3{animation:engrave 1.3s ease forwards}
  .tl-row.in .node{animation:emberpulse 1.3s ease}
  @keyframes engrave{
    0%{color:#241a0e;text-shadow:none}
    28%{color:#ff7a2a;text-shadow:0 0 16px #ff5a18,0 0 30px #ff2e00}
    60%{color:#ffb24a;text-shadow:0 0 12px rgba(255,140,40,.6)}
    100%{color:var(--gold-bright);text-shadow:0 0 6px rgba(230,168,58,.25)}
  }
  @keyframes emberpulse{
    0%{box-shadow:0 0 0 2px rgba(201,162,75,.1),0 0 4px #e6a83a}
    35%{box-shadow:0 0 0 6px rgba(255,110,30,.25),0 0 26px #ff7a1a}
    100%{box-shadow:0 0 0 4px rgba(201,162,75,.12),0 0 14px #e6a83a}
  }
}

/* ---- 캘린더 ---- */

.calwheel{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}
.evt{background:linear-gradient(160deg,var(--panel2),var(--panel));border:1px solid var(--line);
  border-radius:12px;padding:16px 18px;cursor:pointer;transition:.14s;position:relative;overflow:hidden}
.evt:hover{border-color:var(--gold-deep);transform:translateY(-3px);box-shadow:var(--shadow)}
.evt .mo{font-size:34px;font-weight:700;color:var(--gold-deep);font-family:serif;line-height:1}
.evt .mo small{font-size:13px}
.evt h3{margin:6px 0 6px;font-size:17px;color:var(--ink)}
.evt p{margin:0;font-size:12px;color:var(--ink-dim);display:-webkit-box;-webkit-line-clamp:3;
  -webkit-box-orient:vertical;overflow:hidden}
.evt .season{position:absolute;top:14px;right:16px;font-size:18px;opacity:.5}
"""

JS = r"""
const DATA = __DATA__;
const FACTIONS = {
  rep:{label:'지역 대표',color:'var(--rep)'}, bureau:{label:'마법소녀청·협력',color:'var(--bureau)'},
  trainee:{label:'연습생',color:'var(--trainee)'}, shikoku:{label:'시고쿠 (타마모)',color:'var(--shikoku)'},
  refusal:{label:'졸업거부회',color:'var(--refusal)'}, villain:{label:'괴이·빌런',color:'var(--villain)'},
  guest:{label:'게스트',color:'var(--guest)'}, other:{label:'기타',color:'var(--guest)'},
};
const FACTION_ORDER = ['rep','bureau','trainee','shikoku','refusal','villain','guest','other'];
const byId = {};
DATA.characters.forEach(c=>byId[c.id]=c);
DATA.guests.forEach(g=>byId[g.id]=g);
const allCards = DATA.characters.concat(DATA.guests);

function img(prefix,kind){
  const im = DATA.images[prefix];
  if(!im) return null;
  if(kind==='m') return im.m || im.d;
  return im.d || im.m;
}
function esc(s){return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}

/* ---------- 영문 라벨/헤더 -> 한국어 ---------- */
const LABELS = {
  'name':'이름','japanese name':'일본어 이름','hiragana':'히라가나',
  'korean name order':'한국어 표기','stage name':'스테이지명',
  'former stage name':'이전 스테이지명','self-name':'자칭','formal name':'정식 명칭',
  'rank':'랭크','former rank':'이전 랭크','threat class':'위협 등급','age':'나이',
  'management office':'사무소','generation':'세대','assigned district':'담당 지구',
  'current territory':'현재 영역','former position':'이전 직책','position':'직책',
  'species':'종족','type':'유형','height':'신장','appearance':'외형',
  'transformation outfit':'변신 의상','casual outfit':'평상복','personality':'성격',
  'unique magical staff form':'고유 마법 지팡이','specialized common magic':'특화 공통 마법',
  'specialized common magical techniques':'특화 공통 마법','role':'역할',
  'current status':'현재 상태','mentor':'멘토','motif':'모티프','disposition':'성향',
  // 섹션 헤더
  'magical girl':'마법소녀','magical girl rank':'마법소녀 등급','public image':'대외 이미지',
  'personality details':'성격 상세','combat style':'전투 스타일',
  'combat characteristics':'전투 특성','relationships':'관계','relationship':'관계',
  'speech style and example':'말투와 예시','speech style and example ':'말투와 예시',
  'speech style':'말투','roleplaying notes':'롤플레이 노트','roleplaying role':'롤플레이 역할',
  'awakening':'각성','background':'배경','background and awakening':'배경과 각성',
  'core concept':'핵심 콘셉트','overview':'개요','weaknesses and limits':'약점과 한계',
  'profile':'프로필','anomalies':'괴이','anomaly grades':'괴이 등급',
  'anomaly types':'괴이 유형','district assignments':'지구 배정',
  'bureau support policy':'마법소녀청 지원 정책','timeline':'연표',
};
function koHeading(t){
  const k=t.trim().toLowerCase();
  if(LABELS[k]) return LABELS[k];
  // 'Mikami Akane / Akakagerō profile' -> 이름부 유지 + 프로필
  return t.replace(/\bprofile\b/i,'프로필').replace(/\bProfile\b/,'프로필');
}
function koVal(label,val){
  // 라벨별 열거형 값 한국어화
  if(/rank|랭크/i.test(label)){
    if(/special grade/i.test(val)) return '특급';
    const g=val.match(/grade\s*(\d)/i); if(g) return g[1]+'급';
  }
  if(/generation|세대/i.test(label)){
    const g=val.match(/(\d)(?:st|nd|rd|th)?\s*gen/i); if(g) return g[1]+'세대';
    if(/third/i.test(val))return'3세대'; if(/second/i.test(val))return'2세대'; if(/first/i.test(val))return'1세대';
  }
  if(/species|종족/i.test(label)){
    if(/^human$/i.test(val.trim())) return '인간';
  }
  return val;
}
function koLabel(t){
  const m=t.match(/^([A-Za-z][A-Za-z \/'-]*?):\s*([\s\S]*)$/);
  if(m && LABELS[m[1].trim().toLowerCase()]){
    const lab=LABELS[m[1].trim().toLowerCase()];
    return lab+': '+koVal(lab,m[2]);
  }
  return t;
}

/* ---------- 미니 마크다운 렌더러 ---------- */
function mdRender(src){
  if(!src) return '';
  const lines = src.replace(/\r/g,'').split('\n');
  let html='', listDepth=-1;
  function closeLists(to){ while(listDepth>=to){html+='</ul>';listDepth--;} }
  function inline(t){
    return esc(t)
      .replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')
      .replace(/(^|[^*])\*([^*]+?)\*/g,'$1<em>$2</em>');
  }
  for(let raw of lines){
    if(!raw.trim()){ closeLists(0); continue; }
    let m;
    if(m=raw.match(/^(#{2,4})\s*(.+)$/)){
      closeLists(0); const lv=m[1].length; html+=`<h${lv}>${inline(koHeading(m[2]))}</h${lv}>`; continue;
    }
    if(m=raw.match(/^(\s*)[-*]\s+(.+)$/)){
      const depth=Math.floor(m[1].length/2);
      if(depth>listDepth){ while(listDepth<depth){html+='<ul>';listDepth++;} }
      else if(depth<listDepth){ closeLists(depth);}
      html+=`<li>${inline(koLabel(m[2]))}</li>`; continue;
    }
    closeLists(0); html+=`<p>${inline(raw.trim())}</p>`;
  }
  closeLists(0); return html;
}

/* ---------- 라우팅 ---------- */
function show(view){
  document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
  document.getElementById('view-'+view).classList.add('active');
  document.querySelectorAll('.navbtn').forEach(b=>b.classList.toggle('active',b.dataset.view===view));
  if(view==='graph') initGraph();
  if(view==='map') initMap();
  if(view==='timeline') observeTimeline();
}

/* ---------- 도감 ---------- */
let curFilter='all', imgKind='d', selId=null;
function renderCollection(){
  const root=document.getElementById('grid');
  let list = allCards.filter(c=>curFilter==='all'||c.faction===curFilter);
  // 진영별 그룹
  const groups={};
  list.forEach(c=>{(groups[c.faction]=groups[c.faction]||[]).push(c);});
  let html='';
  FACTION_ORDER.forEach(f=>{
    if(!groups[f]) return;
    html+=`<div class="subhead">${FACTIONS[f].label} · ${groups[f].length}</div>`;
    groups[f].forEach(c=>{ html+=cardHtml(c); });
  });
  root.innerHTML=html||'<p style="color:var(--ink-faint)">결과 없음</p>';
  document.getElementById('colcount').textContent=`${list.length} / ${allCards.length}`;
  root.querySelectorAll('.card').forEach(el=>{
    el.onclick=()=>selectChar(el.dataset.id);
  });
}
function cardHtml(c){
  const src=img(c.imgPrefix,'d');
  const col=FACTIONS[c.faction].color;
  const star = c.stars?('★'.repeat(Math.min(c.stars,6))):'';
  return `<div class="card fc-${c.faction} ${c.id===selId?'sel':''}" data-id="${c.id}">
    ${src?`<img src="${src}" loading="lazy">`:`<div class="noimg">${esc((c.nameEn||'?')[0])}</div>`}
    ${star?`<div class="badge">${star}</div>`:''}
    <div class="fdot" style="background:${col};color:${col}"></div>
    <div class="cap"><div class="nm">${esc(c.title)}</div>
      <div class="en">${esc(c.nameEn||'')}</div></div></div>`;
}
function selectChar(id){
  selId=id; imgKind='d';
  document.querySelectorAll('.card').forEach(el=>el.classList.toggle('sel',el.dataset.id===id));
  renderDetail(byId[id]);
}
function ruby(base,top){ return top?`<ruby>${esc(base)}<rt>${esc(top)}</rt></ruby>`:esc(base); }

function renderDetail(c){
  const root=document.getElementById('detail');
  if(!c){root.innerHTML='<div class="dt-empty">왼쪽 도감에서<br>캐릭터를 선택하세요</div>';return;}
  const col=FACTIONS[c.faction].color;
  const hasM = c.imgPrefix && DATA.images[c.imgPrefix] && DATA.images[c.imgPrefix].m;
  const src = img(c.imgPrefix,imgKind);
  const star = c.stars?'★'.repeat(Math.min(c.stars,6)):'';
  const stat=(l,v)=> v?`<div class="stat"><div class="l">${l}</div><div class="v">${esc(v)}</div></div>`:'';
  const topName = [c.nameJp,c.nameEn].filter(Boolean).join(' · ');
  root.innerHTML=`
    <div class="dt-hero">
      <div class="bgwash"></div>
      ${star?`<div class="dt-stars">${star}</div>`:''}
      ${hasM?`<div class="imgtoggle">
        <button class="${imgKind==='d'?'on':''}" data-k="d">일상</button>
        <button class="${imgKind==='m'?'on':''}" data-k="m">변신</button></div>`:''}
      ${src?`<img src="${src}">`:`<div class="dt-empty">초상화 없음</div>`}
      <div class="fade"></div>
    </div>
    <div class="dt-body">
      <div class="dt-name">${esc(c.title)}${topName?`<span class="sub">${esc(topName)}</span>`:''}</div>
      ${c.stage?`<div class="dt-stage">${ruby(stageBase(c.stage),stageRuby(c))}</div>`:''}
      <span class="faction-chip fc-${c.faction}">${FACTIONS[c.faction].label}</span>
      <div class="statgrid">
        ${stat('랭크',c.rankLabel)}${stat('세대',c.generation)}
        ${stat('담당 지구',c.districtKr||c.districtNorm||c.district)}${stat('나이',c.age)}
        ${stat('종족',c.species)}${stat('신장',c.height)}
        ${stat('사무소',c.office)}${stat('성격유형',mbti(c.personality))}
      </div>
      ${c.staff?`<div class="stat" style="border:1px solid var(--line);border-radius:8px;margin-bottom:12px">
        <div class="l">고유 마법 지팡이</div><div class="v">${esc(c.staff)}</div></div>`:''}
      ${c.tagline?`<div class="tagline">"${esc(c.tagline)}"</div>`:''}
      ${c.raw?`<button class="detailbtn" onclick="openModal('${c.id}')">상세 설명 펼쳐보기</button>`:''}
    </div>`;
  root.querySelectorAll('.imgtoggle button').forEach(b=>b.onclick=()=>{imgKind=b.dataset.k;renderDetail(c);});
}
function stageBase(s){return s.replace(/\(.*?\)/,'').trim();}
function stageRuby(c){
  const m=c.stage&&c.stage.match(/\((.+?)\)/);
  return m?m[1]:'';
}
function mbti(p){ if(!p) return null; const m=p.match(/[EI][NS][TF][JP]/); return m?m[0]+(p.match(/\d+w\d+/)?(' · '+p.match(/\d+w\d+/)[0]):''):null;}

function openModal(id){
  const c=byId[id]; const box=document.getElementById('modalBody');
  const src=img(c.imgPrefix,imgKind)||img(c.imgPrefix,'d');
  box.innerHTML=`<button class="modal-close" onclick="closeModal()">×</button>
    <div class="mhead">${src?`<img src="${src}">`:''}
      <div><h2 style="margin:0;color:var(--gold-bright);font-size:24px">${esc(c.title)}</h2>
      <div style="color:var(--ink-faint);font-size:13px">${esc([c.nameJp,c.nameEn].filter(Boolean).join(' · '))}</div>
      ${c.stage?`<div style="color:var(--gold);margin-top:4px">${esc(c.stage)}</div>`:''}</div></div>
    <div class="md">${mdRender(c.raw)}</div>`;
  document.getElementById('modal').classList.add('open');
}
function closeModal(){document.getElementById('modal').classList.remove('open');}

/* ---------- 로어 페이지 ---------- */
function renderLore(id){
  const p=DATA.lore.find(x=>x.id===id)||DATA.lore[0];
  document.getElementById('loreBody').innerHTML=
    `<div class="lore-wrap"><div class="page-kicker">${esc(p.folder||'세계 설정')}</div>
     <h1 class="page-title">${esc(p.title)}</h1><div class="md">${mdRender(p.raw)}</div></div>`;
  document.querySelectorAll('#loreNav a').forEach(a=>a.classList.toggle('active',a.dataset.id===p.id));
  show('lore');
}

/* ---------- 연표 (세로 · 현재→과거 · 각인) ---------- */
function renderTimeline(){
  const rows=DATA.history.slice().reverse().map((h,i)=>`
    <div class="tl-row ${i===0?'present':''}"><div class="node"></div>
      <div class="when">${esc(h.t)}</div><h3>${esc(h.title)}</h3>
      <div class="en">${esc(h.sub)}</div><p>${esc(h.desc)}</p></div>`).join('');
  document.getElementById('view-timeline').innerHTML=`<div class="pad">
    <div class="page-kicker">역사 연표 · Chronicle</div>
    <h1 class="page-title">시고쿠의 비극과 마법소녀 시대</h1>
    <div class="tl-hint">↓ 아래로 내려갈수록 과거로 거슬러 올라갑니다 — 지나간 시간이 불에 새겨집니다.</div>
    <div class="tl-v">${rows}</div></div>`;
  observeTimeline();
}
let tlObserver=null;
function observeTimeline(){
  const root=document.getElementById('main');
  const rows=document.querySelectorAll('#view-timeline .tl-row');
  if(!('IntersectionObserver' in window)){ rows.forEach(r=>r.classList.add('in')); return; }
  if(tlObserver) tlObserver.disconnect();
  tlObserver=new IntersectionObserver(ents=>{
    ents.forEach(e=>{ if(e.isIntersecting) e.target.classList.add('in'); });
  },{root:root, threshold:0.2});
  rows.forEach(r=>tlObserver.observe(r));
}

/* ---------- 캘린더 ---------- */
function renderCalendar(){
  const seasons={4:'🌸',5:'🎏',6:'🌧',7:'🎆',8:'📺',9:'🍇',10:'🎃',11:'🍁',12:'❄'};
  const evts=DATA.events.slice().sort((a,b)=>(a.month||13)-(b.month||13));
  let cal=evts.map(e=>`<div class="evt" onclick="openEvent('${e.id}')">
    <div class="season">${seasons[e.month]||'✦'}</div>
    <div class="mo">${e.month?(e.month+'<small>월</small>'):'<span style="font-size:17px">수시</span>'}</div>
    <h3>${esc(e.title)}</h3><p>${esc(plain(e.raw))}</p></div>`).join('');
  document.getElementById('view-calendar').innerHTML=`<div class="pad">
    <div class="page-kicker">연간 고정 이벤트 · Annual Calendar</div>
    <h1 class="page-title">사계의 행사</h1>
    <div class="calwheel" style="margin-top:18px">${cal}</div></div>`;
}
function plain(raw){
  const lines=(raw||'').split('\n').filter(l=>l.trim() && !/^#{1,4}\s/.test(l));
  return lines.join(' ').replace(/[#*\-]/g,' ').replace(/\s+/g,' ').trim().slice(0,140);
}
function openEvent(id){
  const e=DATA.events.find(x=>x.id===id);
  document.getElementById('modalBody').innerHTML=
    `<button class="modal-close" onclick="closeModal()">×</button>
     <div class="md" style="padding-top:24px"><div class="md">${mdRender(e.raw)}</div></div>`;
  document.getElementById('modal').classList.add('open');
}

/* ---------- 관계 그래프 (팩션 클러스터 + 클릭 포커스) ---------- */
const REL_COLOR={friend:'#7fae6e',family:'#d98fc9',mentor:'#5fc0d6',rival:'#e0b94b',
  enemy:'#e0584b',former:'#b48be6',love:'#e88fb0',colleague:'#8a7a52'};
const REL_LABEL={friend:'친구',family:'가족',mentor:'사제',rival:'라이벌',
  enemy:'적대',former:'옛 인연',love:'연심',colleague:'동료'};
const GFAC=['rep','trainee','bureau','shikoku','refusal','villain','other','guest'];
let graphInited=false, gNodes=[], gEdges=[], gFilter='all', gHover=null, gDrag=null,
    gFocus=null, gNbr=new Set(), gDragMoved=false;

function facColor(f){
  const v=getComputedStyle(document.body).getPropertyValue('--'+f).trim();
  return v||'#c9a24b';
}
function initGraph(){
  if(graphInited){ resizeGraph(); return; }
  graphInited=true;
  const cv=document.getElementById('graphCanvas');
  const inEdge=new Set();
  DATA.edges.forEach(e=>{inEdge.add(e.source);inEdge.add(e.target);});
  gNodes=DATA.characters.filter(c=>inEdge.has(c.id)).map(c=>({id:c.id,c:c,x:0,y:0,vx:0,vy:0}));
  const nmap={}; gNodes.forEach(n=>nmap[n.id]=n);
  gEdges=DATA.edges.filter(e=>nmap[e.source]&&nmap[e.target])
    .map(e=>({s:nmap[e.source],t:nmap[e.target],text:e.text,type:e.type||'colleague'}));
  // 팩션별 초기 배치
  gNodes.forEach((n,i)=>{const fc=facCenter(n.c.faction,400);
    n.x=fc.x+(i%7-3)*16; n.y=fc.y+((i*13)%7-3)*16;});
  // 필터 버튼
  const tools=document.getElementById('graphTools');
  tools.innerHTML=`<button class="filterbtn on" data-f="all">전체</button>`+
    GFAC.filter(f=>gNodes.some(n=>n.c.faction===f))
      .map(f=>`<button class="filterbtn fc-${f}" data-f="${f}">${FACTIONS[f].label}</button>`).join('');
  tools.querySelectorAll('.filterbtn').forEach(b=>b.onclick=()=>{
    gFilter=b.dataset.f; tools.querySelectorAll('.filterbtn').forEach(x=>x.classList.toggle('on',x===b));});
  gNodes.forEach(n=>{const s=img(n.c.imgPrefix,'d'); if(s){const im=new Image();im.src=s;n.im=im;}});
  resizeGraph(); setupGraphEvents(cv); renderGraphPanel(null);
  requestAnimationFrame(stepGraph);
}
let GW=0,GH=0,gcx=0,gcy=0;
function resizeGraph(){
  const cv=document.getElementById('graphCanvas');const r=cv.parentElement.getBoundingClientRect();
  cv.width=r.width;cv.height=r.height;GW=r.width;GH=r.height;gcx=GW/2;gcy=GH/2;
}
function facCenter(f,Rover){
  const present=GFAC.filter(ff=>gNodes.some(n=>n.c.faction===ff));
  const i=present.indexOf(f); const n=Math.max(present.length,1);
  const a=i/n*Math.PI*2 - Math.PI/2;
  const R=Rover||Math.min(GW,GH)*0.33;
  return {x:Math.cos(a)*R, y:Math.sin(a)*R};
}
const NODE_R=18, MINDIST=46;
function stepGraph(){
  if(!document.getElementById('view-graph').classList.contains('active')){requestAnimationFrame(stepGraph);return;}
  const vis=n=>gFilter==='all'||n.c.faction===gFilter;
  for(let i=0;i<gNodes.length;i++){const a=gNodes[i];if(!vis(a))continue;
    // 팩션 중심 인력
    const fc=facCenter(a.c.faction); a.vx+=(fc.x-a.x)*0.022; a.vy+=(fc.y-a.y)*0.022;
    for(let j=i+1;j<gNodes.length;j++){const b=gNodes[j];if(!vis(b))continue;
      let dx=a.x-b.x,dy=a.y-b.y,d2=dx*dx+dy*dy+0.01,d=Math.sqrt(d2);
      let f=1500/d2; dx/=d;dy/=d;
      a.vx+=dx*f;a.vy+=dy*f;b.vx-=dx*f;b.vy-=dy*f;
      if(d<MINDIST){const push=(MINDIST-d)*0.5;a.vx+=dx*push;a.vy+=dy*push;b.vx-=dx*push;b.vy-=dy*push;}}}
  gEdges.forEach(e=>{if(!vis(e.s)||!vis(e.t))return;
    let dx=e.t.x-e.s.x,dy=e.t.y-e.s.y,d=Math.sqrt(dx*dx+dy*dy)+.01;let f=(d-95)*0.012;
    dx/=d;dy/=d;e.s.vx+=dx*f;e.s.vy+=dy*f;e.t.vx-=dx*f;e.t.vy-=dy*f;});
  gNodes.forEach(n=>{if(!vis(n))return;n.vx*=0.85;n.vy*=0.85;
    if(n!==gDrag){n.x+=n.vx;n.y+=n.vy;}});
  drawGraph(vis); requestAnimationFrame(stepGraph);
}
function tx(n){return gcx+n.x;} function ty(n){return gcy+n.y;}
function dim(n,vis){ // 표시 알파
  if(!vis(n)) return 0.07;
  if(gFocus){ return (n===gFocus||gNbr.has(n.id))?1:0.10; }
  return 1;
}
function drawGraph(vis){
  const cv=document.getElementById('graphCanvas');const x=cv.getContext('2d');
  x.clearRect(0,0,GW,GH);
  gEdges.forEach(e=>{
    const on=vis(e.s)&&vis(e.t); if(!on){return;}
    const focused = gFocus && (e.s===gFocus||e.t===gFocus);
    const hovered = gHover && (e.s===gHover||e.t===gHover);
    let alpha = gFocus ? (focused?0.95:0.05) : (hovered?0.9:0.34);
    if(alpha<0.06) return;
    x.globalAlpha=alpha;
    x.strokeStyle=REL_COLOR[e.type]||'#8a7a52';
    x.lineWidth=(focused||hovered)?2.4:1.2;
    x.beginPath();x.moveTo(tx(e.s),ty(e.s));x.lineTo(tx(e.t),ty(e.t));x.stroke();
  });
  x.globalAlpha=1;
  gNodes.forEach(n=>{const a=dim(n,vis);if(a<=0.02)return;
    const big=(n===gHover||n===gFocus); const R=big?24:NODE_R;
    const col=facColor(n.c.faction);
    x.globalAlpha=a;
    x.save();x.beginPath();x.arc(tx(n),ty(n),R,0,7);x.closePath();x.clip();
    if(n.im&&n.im.complete){x.drawImage(n.im,tx(n)-R,ty(n)-R,R*2,R*2.2);}else{x.fillStyle='#332813';x.fill();}
    x.restore();
    x.beginPath();x.arc(tx(n),ty(n),R,0,7);x.lineWidth=big?3.4:2.4;x.strokeStyle=col;x.stroke();
    if(big||(gFocus&&gNbr.has(n.id))){x.fillStyle='#ece0c8';x.font='600 12px Pretendard,sans-serif';
      x.textAlign='center';x.lineWidth=3;x.strokeStyle='rgba(10,8,5,.9)';
      x.strokeText(n.c.title,tx(n),ty(n)+R+15);x.fillText(n.c.title,tx(n),ty(n)+R+15);}
    x.globalAlpha=1;});
}
function setFocus(n){
  gFocus=n; gNbr=new Set();
  if(n){ DATA.edges.forEach(e=>{ if(e.source===n.id)gNbr.add(e.target);
    if(e.target===n.id)gNbr.add(e.source); }); }
  renderGraphPanel(n);
}
function renderGraphPanel(n){
  const p=document.getElementById('graphPanel');
  if(!n){
    const legend=Object.keys(REL_LABEL).map(t=>`<div class="li"><span class="sw" style="background:${REL_COLOR[t]}"></span>${REL_LABEL[t]}</div>`).join('');
    p.innerHTML=`<div class="gp-sec">관계도 보기</div>
      <div class="gp-hint">노드를 <b>클릭</b>하면 그 인물의 관계만 강조되고, 아래에 관계 목록이 나타납니다.
      진영별로 무리지어 배치되어 있습니다. 상단 필터로 진영만 따로 볼 수 있습니다.</div>
      <div class="gp-sec">관계 유형</div><div class="gp-legend">${legend}</div>`;
    return;
  }
  const c=n.c; const src=img(c.imgPrefix,'d');
  const rels=(c.relationships||[]).slice().sort((a,b)=>(a.targetId?0:1)-(b.targetId?0:1));
  const rows=rels.map(r=>{
    const tnode=byId[r.targetId];
    const name=tnode?tnode.title:r.target;
    const ty=r.type||'colleague';
    return `<div class="gp-rel" ${r.targetId?`onclick="focusById('${r.targetId}')"`:''}>
      <div class="top"><span class="tgt">${esc(name)}</span>
        <span class="rel-badge" style="background:${REL_COLOR[ty]}">${REL_LABEL[ty]}</span></div>
      <div class="desc">${esc(r.text||'')}</div></div>`;
  }).join('') || '<div class="gp-hint">관계 정보 없음</div>';
  p.innerHTML=`<div class="gp-head">${src?`<img src="${src}">`:''}
      <div><div class="nm">${esc(c.title)}</div><div class="en">${esc([c.nameJp,c.nameEn].filter(Boolean).join(' · '))}</div>
      <span class="faction-chip fc-${c.faction}" style="margin:6px 0 0;font-size:11px;padding:3px 10px">${FACTIONS[c.faction].label}</span></div></div>
    <div class="gp-sec">관계 ${rels.length}</div>${rows}
    <button class="gp-back" onclick="show('codex');selectChar('${c.id}')">도감에서 보기 →</button>
    <button class="gp-back" style="margin-top:8px;border-color:var(--line)" onclick="clearFocus()">전체 보기</button>`;
}
function focusById(id){ const n=gNodes.find(x=>x.id===id); if(n) setFocus(n); }
function clearFocus(){ setFocus(null); }
function setupGraphEvents(cv){
  const tip=document.getElementById('graphTip');
  function pick(mx,my){let best=null,bd=24*24;gNodes.forEach(n=>{
    if(!(gFilter==='all'||n.c.faction===gFilter))return;
    const dx=mx-tx(n),dy=my-ty(n),d=dx*dx+dy*dy;if(d<bd){bd=d;best=n;}});return best;}
  cv.onmousemove=ev=>{const r=cv.getBoundingClientRect();const mx=ev.clientX-r.left,my=ev.clientY-r.top;
    if(gDrag){gDrag.x=mx-gcx;gDrag.y=my-gcy;gDrag.vx=gDrag.vy=0;gDragMoved=true;return;}
    const n=pick(mx,my);gHover=n;
    if(n){const rels=DATA.edges.filter(e=>e.source===n.id||e.target===n.id);
      tip.style.display='block';tip.style.left=(ev.clientX+14)+'px';tip.style.top=(ev.clientY+12)+'px';
      tip.innerHTML=`<b>${esc(n.c.title)}</b> <span style="color:var(--ink-faint)">${esc(n.c.nameEn||'')}</span><br>
        <span style="color:var(--ink-faint)">${FACTIONS[n.c.faction].label} · 관계 ${rels.length} · 클릭하면 강조</span>`;
      cv.style.cursor='pointer';}
    else{tip.style.display='none';cv.style.cursor='grab';}};
  cv.onmousedown=ev=>{const r=cv.getBoundingClientRect();gDrag=pick(ev.clientX-r.left,ev.clientY-r.top);gDragMoved=false;};
  window.addEventListener('mouseup',()=>{gDrag=null;});
  cv.onclick=ev=>{if(gDragMoved){gDragMoved=false;return;}
    const r=cv.getBoundingClientRect();const n=pick(ev.clientX-r.left,ev.clientY-r.top);
    if(n){ setFocus(n); } else { clearFocus(); }};
  window.addEventListener('resize',()=>{if(document.getElementById('view-graph').classList.contains('active'))resizeGraph();});
}

/* ---------- 지도 ---------- */
let mapInited=false;
const MAP_POS=__MAPPOS__;
const MAPGEO=__MAPGEO__;
function krName(d){ return (MAPGEO&&MAPGEO.kr[d]) || (MAP_POS[d]&&MAP_POS[d].kr) || d; }
function initMap(){
  if(mapInited)return; mapInited=true;
  if(!MAPGEO){ initMapFallback(); return; }
  const stage=document.getElementById('mapStage'), g=MAPGEO;
  const byD={}; g.prefs.forEach(p=>{(byD[p.district]=byD[p.district]||[]).push(p);});
  let svg=`<svg viewBox="0 0 ${g.viewW} ${g.viewH}" preserveAspectRatio="xMidYMid meet">`;
  g.districts.forEach(d=>{
    svg+=`<g class="district ${d.sealed?'sealed':''}" data-d="${d.key}">`;
    (byD[d.key]||[]).forEach(p=>{ svg+=`<path class="reg" d="${p.d}" style="--dc:${d.color}"/>`; });
    svg+=`</g>`;
  });
  g.districts.forEach(d=>{
    svg+=`<g class="dlabel" data-d="${d.key}">
      ${d.sealed?`<text class="seal-mark" x="${d.labelX}" y="${d.labelY-15}">⛩</text>`:''}
      <text class="lbl" x="${d.labelX}" y="${d.labelY}">${esc(krName(d.key))}</text></g>`;
  });
  svg+=`</svg>`;
  stage.innerHTML=svg;
  stage.querySelectorAll('.district').forEach(gn=>gn.onclick=()=>selectDistrict(gn.dataset.d));
  selectDistrict('Tokyo');
}
function initMapFallback(){
  const stage=document.getElementById('mapStage');
  let svg=`<svg viewBox="0 0 720 920" preserveAspectRatio="xMidYMid meet">`;
  for(const d in MAP_POS){const p=MAP_POS[d];const sealed=d==='Shikoku';
    svg+=`<g class="district ${sealed?'sealed':''}" data-d="${d}">
      <ellipse class="reg" cx="${p.x}" cy="${p.y}" rx="46" ry="30" style="--dc:#3a4a52"/>
      <text class="lbl" x="${p.x}" y="${p.y+4}">${p.kr.split(' ')[0]}</text></g>`;}
  svg+=`</svg>`; stage.innerHTML=svg;
  stage.querySelectorAll('.district').forEach(g=>g.onclick=()=>selectDistrict(g.dataset.d));
  selectDistrict('Tokyo');
}
function selectDistrict(d){
  document.querySelectorAll('.district,.dlabel').forEach(g=>g.classList.toggle('sel',g.dataset.d===d));
  const info=document.getElementById('mapInfo');
  const kr=krName(d);
  const norms = d==='Hokkaido' ? ['Northern Hokkaido','Southern Hokkaido'] : [d];
  const inD=c=>norms.includes(c.districtNorm);
  const reps=DATA.characters.filter(c=>inD(c)&&c.faction==='rep');
  const trs=DATA.characters.filter(c=>inD(c)&&c.faction==='trainee');
  const others=DATA.characters.filter(c=>inD(c)&&!['rep','trainee'].includes(c.faction));
  function row(c){const s=img(c.imgPrefix,'d');return `<div class="mi-char" onclick="show('codex');selectChar('${c.id}')">
    ${s?`<img src="${s}">`:'<div style="width:42px"></div>'}
    <div><div class="nm">${esc(c.title)}</div><div class="rk">${esc(c.rankLabel||'')} · ${FACTIONS[c.faction].label}</div></div></div>`;}
  if(d==='Shikoku'){
    info.innerHTML=`<h2 style="color:var(--shikoku)">시고쿠</h2>
      <div class="mi-sub">SHIKOKU · 봉인된 영역</div>
      <p style="color:var(--ink-dim);font-size:13px">최초의 백귀야행으로 황폐화되어 봉인된 무인 지대.
      아치 에너미 <b style="color:var(--shikoku)">타마모노마에</b>가 지배하며, 납치·세뇌된 마법소녀들이
      그녀의 '가족'으로 살아간다.</p>
      <div class="mi-role">시고쿠의 존재들</div>
      ${DATA.characters.filter(c=>c.faction==='shikoku'||c.nameEn==='Tamamo-no-Mae').map(row).join('')}`;
    return;
  }
  info.innerHTML=`<h2>${esc(kr)}</h2><div class="mi-sub">${esc(d.toUpperCase())}</div>
    ${reps.length?`<div class="mi-role">지역 대표</div>${reps.map(row).join('')}`:''}
    ${trs.length?`<div class="mi-role">연습생</div>${trs.map(row).join('')}`:''}
    ${others.length?`<div class="mi-role">기타</div>${others.map(row).join('')}`:''}
    ${!reps.length&&!trs.length&&!others.length?'<p style="color:var(--ink-faint)">등록된 마법소녀 정보 없음</p>':''}`;
}

/* ---------- 검색 ---------- */
function setupSearch(){
  const inp=document.getElementById('searchInput'),res=document.getElementById('searchResults');
  inp.oninput=()=>{const q=inp.value.trim().toLowerCase();if(!q){res.style.display='none';return;}
    const hits=[];
    allCards.forEach(c=>{const hay=[c.title,c.nameEn,c.nameJp,c.stage,c.tagline,c.rankLabel].join(' ').toLowerCase();
      if(hay.includes(q))hits.push({type:'c',o:c});});
    DATA.lore.forEach(l=>{if((l.title+' '+l.keys+' '+l.raw).toLowerCase().includes(q))hits.push({type:'l',o:l});});
    DATA.events.forEach(e=>{if((e.title+' '+e.keys+' '+e.raw).toLowerCase().includes(q))hits.push({type:'e',o:e});});
    res.innerHTML=hits.slice(0,30).map(h=>{
      if(h.type==='c'){const s=img(h.o.imgPrefix,'d');return `<a onclick="pickSearch('c','${h.o.id}')">
        ${s?`<img src="${s}">`:'<div style="width:30px"></div>'}<div><div>${esc(h.o.title)}</div>
        <div class="k">${esc(h.o.nameEn||'')} · ${FACTIONS[h.o.faction].label}</div></div></a>`;}
      const lbl=h.type==='l'?'세계 설정':'이벤트';
      return `<a onclick="pickSearch('${h.type}','${h.o.id}')"><div style="width:30px;text-align:center">${h.type==='l'?'📜':'📅'}</div>
        <div><div>${esc(h.o.title)}</div><div class="k">${lbl}</div></div></a>`;
    }).join('')||'<a><div class="k">결과 없음</div></a>';
    res.style.display='block';};
  document.addEventListener('click',e=>{if(!document.getElementById('search').contains(e.target))res.style.display='none';});
}
function pickSearch(type,id){
  document.getElementById('searchResults').style.display='none';
  document.getElementById('searchInput').value='';
  if(type==='c'){show('codex');selectChar(id);}
  else if(type==='l'){renderLore(id);}
  else{show('timeline');openEvent(id);}
}

/* ---------- 부트 ---------- */
function boot(){
  document.body.querySelector('#noise-src');
  // 사이드바 로어 네비
  const folders={};
  DATA.lore.forEach(l=>{(folders[l.folder||'세계 설정']=folders[l.folder||'세계 설정']||[]).push(l);});
  let nav='';
  for(const f in folders){ nav+=folders[f].map(l=>`<a data-id="${l.id}" onclick="renderLore('${l.id}')">${esc(l.title)}</a>`).join(''); }
  document.getElementById('loreNav').innerHTML=nav;
  renderCollection();
  // 첫 캐릭터 선택
  selectChar(DATA.characters[0].id);
  renderTimeline();
  renderCalendar();
  setupSearch();
  // 필터 버튼
  const fb=document.getElementById('filters');
  fb.innerHTML=`<button class="filterbtn on" data-f="all">전체</button>`+
    FACTION_ORDER.filter(f=>allCards.some(c=>c.faction===f))
      .map(f=>`<button class="filterbtn fc-${f}" data-f="${f}">${FACTIONS[f].label}</button>`).join('');
  fb.querySelectorAll('.filterbtn').forEach(b=>b.onclick=()=>{curFilter=b.dataset.f;
    fb.querySelectorAll('.filterbtn').forEach(x=>x.classList.toggle('on',x===b));renderCollection();});
  document.querySelectorAll('.navbtn').forEach(b=>b.onclick=()=>{
    if(b.dataset.view==='lore'){renderLore(DATA.lore[0].id);}else{show(b.dataset.view);}});
  document.getElementById('modal').onclick=e=>{if(e.target.id==='modal')closeModal();};
  document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal();});
}
boot();
"""


def page(data_json, mappos_json, mapgeo_json="null"):
    html = HTML_SHELL
    css = CSS.replace("__NOISE__", NOISE)
    js = (JS.replace("__DATA__", data_json)
            .replace("__MAPPOS__", mappos_json)
            .replace("__MAPGEO__", mapgeo_json))
    html = html.replace("/*__CSS__*/", css).replace("/*__JS__*/", js)
    return html


HTML_SHELL = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>마법소녀 세계관 위키 · Magical Girl Lorebook</title>
<style>/*__CSS__*/</style>
</head>
<body>
<div id="app">
  <header id="topbar">
    <div class="brand">마법소녀 세계관 위키<small>Magical Girl Lorebook</small></div>
    <div id="search">
      <span class="ic">⌕</span>
      <input id="searchInput" placeholder="캐릭터 · 설정 · 이벤트 검색…" autocomplete="off">
      <div id="searchResults"></div>
    </div>
  </header>
  <nav id="side">
    <div class="navsec">
      <button class="navbtn active" data-view="codex"><span class="ic">❖</span>캐릭터 도감</button>
      <button class="navbtn" data-view="lore"><span class="ic">📜</span>세계 설정</button>
      <div class="navsub open" id="loreNav"></div>
      <button class="navbtn" data-view="graph"><span class="ic">⁂</span>관계도</button>
      <button class="navbtn" data-view="map"><span class="ic">⌖</span>지구 지도</button>
      <button class="navbtn" data-view="timeline"><span class="ic">⏚</span>연표</button>
      <button class="navbtn" data-view="calendar"><span class="ic">❂</span>캘린더</button>
    </div>
    <div class="sideband">Interactive Fantasy Lore</div>
  </nav>
  <main id="main">
    <section id="view-codex" class="view active">
      <div id="detail"></div>
      <div id="collection">
        <div class="coltools">
          <span class="label">진영</span>
          <div id="filters" style="display:flex;gap:7px;flex-wrap:wrap"></div>
          <span class="colcount" id="colcount"></span>
        </div>
        <div class="grid" id="grid"></div>
      </div>
    </section>
    <section id="view-lore" class="view"><div class="pad" id="loreBody"></div></section>
    <section id="view-graph" class="view">
      <div id="graphStage">
        <div class="graph-tools" id="graphTools"></div>
        <canvas id="graphCanvas"></canvas>
        <div id="graphTip"></div>
      </div>
      <div id="graphPanel"></div>
    </section>
    <section id="view-map" class="view">
      <div id="mapStage"></div>
      <div id="mapInfo"></div>
    </section>
    <section id="view-timeline" class="view"></section>
    <section id="view-calendar" class="view"></section>
  </main>
</div>
<div id="modal"><div class="modal-box" id="modalBody"></div></div>
<script>/*__JS__*/</script>
</body>
</html>
"""
