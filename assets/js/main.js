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
