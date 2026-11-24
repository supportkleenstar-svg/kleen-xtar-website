/* Kleen Xtar inner pages: nav, mobile menu, WhatsApp bar, blog filters. */
(function () {
  'use strict';
  var root = document.querySelector('.kx');
  if (!root) return;
  var nav = root.querySelector('.kx-nav'), mnav = root.querySelector('#kx-mnav'),
      burger = root.querySelector('.kx-burger'), mbar = root.querySelector('.kx-mbar');

  function setMenu(open) {
    if (!mnav) return;
    mnav.classList.toggle('is-open', open);
    nav.classList.toggle('is-menu', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.documentElement.style.overflow = open ? 'hidden' : '';
  }
  if (burger) burger.addEventListener('click', function () { setMenu(!mnav.classList.contains('is-open')); });
  if (mnav) Array.prototype.forEach.call(mnav.querySelectorAll('a'), function (a) { a.addEventListener('click', function () { setMenu(false); }); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && mnav && mnav.classList.contains('is-open')) { setMenu(false); burger.focus(); }
  });

  var ticking = false;
  function onScroll() {
    ticking = false;
    var y = window.scrollY || window.pageYOffset;
    nav.classList.toggle('is-solid', y > 24);
    if (mbar) mbar.classList.toggle('is-show', y > 360);
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* blog index: filter cards by topic */
  var tags = root.querySelectorAll('.kx-tags button');
  Array.prototype.forEach.call(tags, function (b) {
    b.addEventListener('click', function () {
      var t = b.getAttribute('data-tag');
      Array.prototype.forEach.call(tags, function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      Array.prototype.forEach.call(root.querySelectorAll('.kx-post'), function (p) {
        p.hidden = !(t === 'all' || p.getAttribute('data-tag') === t);
      });
    });
  });
})();
