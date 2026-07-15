
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
