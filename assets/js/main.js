/* ColorWorks Vinyl - shared script: header state, phone menu, reveal on scroll. */
(function () {
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.menu-toggle');
  var menu = document.getElementById('site-menu');

  function onScroll() { if (header) header.classList.toggle('is-scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  function setMenu(open) {
    if (!toggle || !menu) return;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    menu.classList.toggle('is-open', open);
    if (header) header.classList.toggle('is-menu-open', open);
  }
  if (toggle && menu) {
    toggle.addEventListener('click', function () { setMenu(toggle.getAttribute('aria-expanded') !== 'true'); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) {
      if (toggle.getAttribute('aria-expanded') !== 'true') return;
      if (e.key === 'Escape') { setMenu(false); toggle.focus(); return; }
      if (e.key !== 'Tab') return;
      // Keep focus inside the open menu: its links and the close button.
      var f = Array.prototype.slice.call(menu.querySelectorAll('a')).concat([toggle]);
      var i = f.indexOf(document.activeElement);
      e.preventDefault();
      f[i === -1 ? 0 : (i + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus();
    });
    window.matchMedia('(min-width: 861px)').addEventListener('change', function (m) { if (m.matches) setMenu(false); });
  }

  var items = document.querySelectorAll('.reveal');
  function show(el) { el.classList.add('is-in'); }
  if (!('IntersectionObserver' in window)) { items.forEach(show); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { show(e.target); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  items.forEach(function (el) { io.observe(el); });
  document.addEventListener('focusin', function (e) { var r = e.target.closest && e.target.closest('.reveal'); if (r) show(r); });
  window.addEventListener('beforeprint', function () { items.forEach(show); });
})();

/* Pass 3 gallery: prev/next buttons, Left/Right/Home/End keys on the track, "n of N" counter. No autoplay. */
(function () {
  var still = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('.carousel').forEach(function (c) {
    var track = c.querySelector('.carousel-track'), slides = track.querySelectorAll('.slide');
    var nav = c.querySelector('.carousel-nav'), count = c.querySelector('.carousel-count');
    var prev = c.querySelector('[data-dir="-1"]'), next = c.querySelector('[data-dir="1"]');
    var n = slides.length, cur = 0, raf = 0;
    if (!nav || n < 2) return;
    nav.hidden = false;
    function index() {
      var x = track.scrollLeft, best = 0, d = Infinity;
      slides.forEach(function (s, i) { var dd = Math.abs(s.offsetLeft - track.offsetLeft - x); if (dd < d) { d = dd; best = i; } });
      if (track.scrollLeft + track.clientWidth >= track.scrollWidth - 2) best = n - 1;
      return best;
    }
    function update() {
      raf = 0; cur = index();
      count.textContent = (cur + 1) + ' of ' + n;
      prev.setAttribute('aria-disabled', String(cur === 0));
      next.setAttribute('aria-disabled', String(cur === n - 1));
    }
    function go(i) {
      i = Math.max(0, Math.min(n - 1, i));
      track.scrollTo({ left: slides[i].offsetLeft - track.offsetLeft, behavior: still.matches ? 'auto' : 'smooth' });
    }
    prev.addEventListener('click', function () { go(cur - 1); });
    next.addEventListener('click', function () { go(cur + 1); });
    track.addEventListener('keydown', function (e) {
      var k = { ArrowLeft: cur - 1, ArrowRight: cur + 1, Home: 0, End: n - 1 }[e.key];
      if (k === undefined) return;
      e.preventDefault(); go(k);
    });
    track.addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(update); }, { passive: true });
    window.addEventListener('resize', function () { if (!raf) raf = requestAnimationFrame(update); });
    update();
  });
})();
