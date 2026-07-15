"""CSS and JS assets for the generated site (imported by build_site.py)."""

CSS = r"""
:root{
  --bg:#f7f7fb; --bg-soft:#ffffff; --panel:#ffffff; --panel-2:#f2f2f8;
  --text:#1c1d29; --muted:#6b6d80; --border:#e6e6ef;
  --accent:#6d5efc; --accent-soft:#ece9ff; --accent-ink:#4b3fd6;
  --shadow:0 1px 2px rgba(20,20,50,.06),0 8px 24px rgba(20,20,50,.06);
  --radius:14px; --sidebar-w:288px; --content-w:800px;
  --code-bg:#f5f5fb;
  --font:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif;
}
:root[data-theme="dark"]{
  --bg:#0e0f17; --bg-soft:#141520; --panel:#171826; --panel-2:#1d1f30;
  --text:#e7e8f2; --muted:#9a9cb3; --border:#262838;
  --accent:#8b7cff; --accent-soft:#221f3d; --accent-ink:#b8adff;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 12px 30px rgba(0,0,0,.35);
  --code-bg:#12131d;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:var(--font);
  line-height:1.65;-webkit-font-smoothing:antialiased;font-size:16px}
a{color:var(--accent-ink);text-decoration:none}
a:hover{text-decoration:underline}
code,pre,kbd{font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace}

.layout{display:flex;min-height:100vh}
.main{flex:1;min-width:0;display:flex;flex-direction:column}

/* Sidebar */
.sidebar{width:var(--sidebar-w);flex:0 0 var(--sidebar-w);background:var(--bg-soft);
  border-right:1px solid var(--border);position:sticky;top:0;height:100vh;
  overflow-y:auto;padding:22px 16px;display:flex;flex-direction:column;gap:16px}
.brand{display:flex;align-items:center;gap:12px;padding:6px 8px;border-radius:12px}
.brand:hover{text-decoration:none;background:var(--panel-2)}
.brand-mark{display:grid;place-items:center;width:42px;height:42px;border-radius:12px;
  background:linear-gradient(135deg,var(--accent),#b06cff);color:#fff;font-weight:800;
  font-size:15px;letter-spacing:.5px;box-shadow:var(--shadow)}
.brand-text{font-weight:700;font-size:14px;line-height:1.25;color:var(--text)}
.search-open{display:flex;align-items:center;gap:8px;width:100%;padding:10px 12px;
  border:1px solid var(--border);background:var(--panel);color:var(--muted);
  border-radius:12px;cursor:pointer;font-size:14px;text-align:left}
.search-open:hover{border-color:var(--accent)}
.search-open .kbd{margin-left:auto;border:1px solid var(--border);border-radius:6px;
  padding:1px 7px;font-size:12px;background:var(--panel-2)}
.nav{display:flex;flex-direction:column;gap:2px;overflow-y:auto}
.nav-subject summary{list-style:none;display:flex;align-items:center;gap:10px;
  padding:9px 10px;border-radius:10px;cursor:pointer;font-weight:600;font-size:14px}
.nav-subject summary::-webkit-details-marker{display:none}
.nav-subject summary:hover{background:var(--panel-2)}
.nav-emoji{font-size:17px}
.nav-subject ul{list-style:none;margin:2px 0 6px;padding:0 0 0 12px;
  border-left:1px solid var(--border);margin-left:18px;display:flex;flex-direction:column;gap:1px}
.nav-subject ul a{display:block;padding:6px 10px;border-radius:8px;color:var(--muted);
  font-size:13px;line-height:1.35}
.nav-subject ul a:hover{background:var(--panel-2);color:var(--text);text-decoration:none}
.nav-subject ul a.active{background:var(--accent-soft);color:var(--accent-ink);font-weight:600}
.sidebar-foot{margin-top:auto;font-size:13px;color:var(--muted)}

/* Topbar */
.topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:12px;
  padding:12px 24px;background:color-mix(in srgb,var(--bg-soft) 88%,transparent);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--border)}
.crumbs{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--muted);
  flex-wrap:wrap;min-width:0}
.crumbs a{color:var(--muted)}
.crumbs a:hover{color:var(--accent-ink)}
.crumbs span:last-child{color:var(--text);font-weight:600}
.crumbs .sep{opacity:.5}
.spacer{flex:1}
.icon-btn{border:1px solid var(--border);background:var(--panel);color:var(--text);
  width:38px;height:38px;border-radius:10px;cursor:pointer;font-size:16px;display:grid;place-items:center}
.icon-btn:hover{border-color:var(--accent)}
.menu-btn{display:none}
#theme-toggle .i-moon{display:none}
:root[data-theme="dark"] #theme-toggle .i-sun{display:none}
:root[data-theme="dark"] #theme-toggle .i-moon{display:inline}

/* Content */
.content{width:100%;max-width:var(--content-w);margin:0 auto;padding:34px 24px 60px}
.content.wide{max-width:1080px}
.page-foot{max-width:var(--content-w);margin:0 auto;padding:24px;color:var(--muted);
  font-size:13px;border-top:1px solid var(--border);width:100%}

/* Article */
.note-head{display:flex;align-items:center;gap:14px;margin:0 0 20px}
.note-emoji{font-size:30px}
.note h1{font-size:28px;line-height:1.25;margin:0;letter-spacing:-.01em}
.note h2{font-size:21px;margin:34px 0 12px;letter-spacing:-.01em}
.note h3{font-size:17px;margin:26px 0 10px}
.note p{margin:14px 0}
.note ol,.note ul{padding-left:24px;margin:14px 0}
.note li{margin:5px 0}
.wikilink{border-bottom:1px solid var(--accent-soft)}
.missing{color:#c2410c;background:#fff2ea;border-radius:5px;padding:0 5px;font-size:.92em}
:root[data-theme="dark"] .missing{color:#fca55d;background:#2a1c12}

.note-img{display:block;max-width:100%;height:auto;margin:16px auto;border-radius:12px;
  border:1px solid var(--border);box-shadow:var(--shadow);background:#fff;cursor:zoom-in}
.imglink{display:block}
.imglink:hover{text-decoration:none}

pre{background:var(--code-bg);border:1px solid var(--border);border-radius:12px;
  padding:16px 18px;overflow:auto;margin:16px 0;font-size:13.5px;line-height:1.55}
pre code{background:none;padding:0}
:not(pre)>code{background:var(--panel-2);border:1px solid var(--border);border-radius:6px;
  padding:1px 6px;font-size:.9em}
.hljs{background:none!important}

.katex-display{overflow-x:auto;overflow-y:hidden;padding:8px 2px;margin:16px 0}
.katex{font-size:1.05em}

/* Landing */
.landing .content{padding-top:20px}
.hero{padding:26px 0 8px}
.hero-badge{display:inline-block;background:var(--accent-soft);color:var(--accent-ink);
  font-weight:600;font-size:13px;padding:6px 12px;border-radius:999px;margin-bottom:18px}
.hero h1{font-size:40px;line-height:1.12;margin:0 0 14px;letter-spacing:-.02em;
  background:linear-gradient(120deg,var(--text),var(--accent-ink));
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.hero .lead{font-size:18px;color:var(--muted);max-width:620px;margin:0}
.hero-stats{display:flex;gap:28px;margin:26px 0 8px;flex-wrap:wrap}
.hero-stats div{display:flex;flex-direction:column}
.hero-stats b{font-size:26px;color:var(--accent-ink)}
.hero-stats span{font-size:13px;color:var(--muted)}

.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));
  gap:16px;margin-top:24px}
.card{position:relative;display:flex;align-items:center;gap:16px;padding:20px;
  background:var(--panel);border:1px solid var(--border);border-radius:var(--radius);
  box-shadow:var(--shadow);transition:transform .15s,border-color .15s}
.card:hover{transform:translateY(-3px);border-color:var(--accent);text-decoration:none}
.card-emoji{font-size:32px;width:56px;height:56px;display:grid;place-items:center;
  background:var(--accent-soft);border-radius:14px;flex:0 0 auto}
.card-body{flex:1;min-width:0}
.card h3{margin:0 0 4px;font-size:17px;color:var(--text)}
.card-meta{margin:0;font-size:13px;color:var(--muted)}
.badge{position:absolute;top:14px;right:14px;font-size:11px;font-weight:700;
  color:var(--accent-ink);background:var(--accent-soft);padding:3px 9px;border-radius:999px}
.card-arrow{color:var(--accent);font-size:20px;opacity:0;transition:opacity .15s,transform .15s}
.card:hover .card-arrow{opacity:1;transform:translateX(3px)}

/* Task list on subject overview */
.tasklist{margin-top:34px}
.tasklist h2{font-size:19px;margin-bottom:12px}
.tasklist a{display:flex;align-items:center;gap:12px;padding:13px 16px;margin:8px 0;
  background:var(--panel);border:1px solid var(--border);border-radius:12px;color:var(--text)}
.tasklist a:hover{border-color:var(--accent);text-decoration:none;background:var(--panel-2)}
.tasklist a span{flex:1}
.tasklist a em{color:var(--accent);font-style:normal}

/* Search modal */
.search-modal{position:fixed;inset:0;z-index:100;background:rgba(10,10,25,.45);
  backdrop-filter:blur(3px);display:flex;justify-content:center;align-items:flex-start;padding-top:12vh}
.search-modal[hidden]{display:none}
.search-box{width:min(620px,92vw);background:var(--panel);border:1px solid var(--border);
  border-radius:16px;box-shadow:var(--shadow);overflow:hidden}
#search-input{width:100%;border:none;outline:none;background:none;color:var(--text);
  font-size:17px;padding:18px 20px;border-bottom:1px solid var(--border)}
#search-results{list-style:none;margin:0;padding:6px;max-height:52vh;overflow-y:auto}
#search-results li{padding:11px 14px;border-radius:10px;cursor:pointer}
#search-results li.sel,#search-results li:hover{background:var(--accent-soft)}
#search-results .r-title{font-weight:600;font-size:14px}
#search-results .r-sub{font-size:12px;color:var(--muted)}
#search-results .r-empty{color:var(--muted);padding:14px;text-align:center}
.search-hint{padding:10px 16px;font-size:12px;color:var(--muted);border-top:1px solid var(--border)}

/* Lightbox */
.lightbox{position:fixed;inset:0;z-index:200;background:rgba(6,6,16,.9);
  display:flex;align-items:center;justify-content:center;cursor:zoom-out;padding:24px}
.lightbox[hidden]{display:none}
.lightbox img{max-width:96vw;max-height:92vh;border-radius:10px;box-shadow:0 20px 60px rgba(0,0,0,.5)}

@media (max-width:860px){
  .sidebar{position:fixed;left:0;top:0;z-index:60;transform:translateX(-100%);
    transition:transform .22s ease;box-shadow:var(--shadow)}
  .sidebar.open{transform:translateX(0)}
  .menu-btn{display:grid}
  .hero h1{font-size:30px}
  .content{padding:22px 16px 50px}
}
"""

JS = r"""
document.addEventListener('DOMContentLoaded', function () {
  var root = document.documentElement;

  function syncHl(){
    var dark = root.getAttribute('data-theme') === 'dark';
    var l = document.getElementById('hl-light');
    var d = document.getElementById('hl-dark');
    if (l) l.disabled = dark;
    if (d) d.disabled = !dark;
  }
  syncHl();

  var toggle = document.getElementById('theme-toggle');
  if (toggle) toggle.addEventListener('click', function(){
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch(e){}
    syncHl();
  });

  // Mobile menu
  var menu = document.getElementById('menu-btn');
  var sidebar = document.getElementById('sidebar');
  if (menu && sidebar) menu.addEventListener('click', function(){ sidebar.classList.toggle('open'); });
  document.addEventListener('click', function(e){
    if (sidebar && sidebar.classList.contains('open') &&
        !sidebar.contains(e.target) && e.target !== menu) sidebar.classList.remove('open');
  });

  // KaTeX
  if (window.renderMathInElement) {
    renderMathInElement(document.querySelector('.content') || document.body, {
      delimiters: [
        {left: '$$', right: '$$', display: true},
        {left: '$', right: '$', display: false}
      ],
      throwOnError: false
    });
  }

  // Highlight.js
  if (window.hljs) {
    document.querySelectorAll('pre code').forEach(function(b){ try{ hljs.highlightElement(b); }catch(e){} });
  }

  // Lightbox
  var lb = document.createElement('div');
  lb.className = 'lightbox'; lb.hidden = true;
  lb.innerHTML = '<img alt="">';
  document.body.appendChild(lb);
  var lbImg = lb.querySelector('img');
  document.querySelectorAll('[data-lightbox]').forEach(function(a){
    a.addEventListener('click', function(e){
      e.preventDefault();
      lbImg.src = a.getAttribute('href');
      lb.hidden = false;
    });
  });
  lb.addEventListener('click', function(){ lb.hidden = true; lbImg.src=''; });

  // Search
  var modal = document.getElementById('search-modal');
  var input = document.getElementById('search-input');
  var results = document.getElementById('search-results');
  var openBtn = document.getElementById('search-open');
  var data = [], sel = 0;
  var base = window.SITE_ROOT || '';

  function loadData(){
    if (data.length) return Promise.resolve();
    return fetch(base + 'search-index.json').then(function(r){return r.json();}).then(function(j){ data = j; });
  }
  function openSearch(){
    if (!modal) return;
    loadData().then(function(){ modal.hidden = false; input.value=''; render(''); input.focus(); });
  }
  function closeSearch(){ if (modal) modal.hidden = true; }

  function render(q){
    q = q.trim().toLowerCase();
    var items = !q ? data.slice(0, 8) : data.filter(function(d){
      return (d.title + ' ' + d.subject + ' ' + d.text).toLowerCase().indexOf(q) !== -1;
    }).slice(0, 12);
    sel = 0;
    if (!items.length){ results.innerHTML = '<li class="r-empty">Ничего не найдено</li>'; return; }
    results.innerHTML = items.map(function(d,i){
      return '<li data-url="'+base+d.url+'" class="'+(i===0?'sel':'')+'">'+
        '<div class="r-title">'+esc(d.title)+'</div>'+
        '<div class="r-sub">'+esc(d.subject)+'</div></li>';
    }).join('');
    Array.prototype.forEach.call(results.children, function(li){
      li.addEventListener('click', function(){ location.href = li.getAttribute('data-url'); });
    });
  }
  function esc(s){ return (s||'').replace(/[&<>]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]; }); }
  function move(dir){
    var lis = results.querySelectorAll('li[data-url]'); if(!lis.length) return;
    lis[sel] && lis[sel].classList.remove('sel');
    sel = (sel + dir + lis.length) % lis.length;
    lis[sel].classList.add('sel'); lis[sel].scrollIntoView({block:'nearest'});
  }

  if (openBtn) openBtn.addEventListener('click', openSearch);
  if (input) input.addEventListener('input', function(){ render(input.value); });
  if (modal) modal.addEventListener('click', function(e){ if (e.target === modal) closeSearch(); });
  document.addEventListener('keydown', function(e){
    if (e.key === '/' && modal && modal.hidden && !/input|textarea/i.test(document.activeElement.tagName)){
      e.preventDefault(); openSearch();
    } else if (modal && !modal.hidden){
      if (e.key === 'Escape') closeSearch();
      else if (e.key === 'ArrowDown'){ e.preventDefault(); move(1); }
      else if (e.key === 'ArrowUp'){ e.preventDefault(); move(-1); }
      else if (e.key === 'Enter'){
        var cur = results.querySelector('li.sel'); if (cur) location.href = cur.getAttribute('data-url');
      }
    }
  });
});
"""
