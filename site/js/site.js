/* Beachvibes Surfshop — site behaviour. Concept by Salty Code Studio. */
(() => {
  const d = document;
  d.documentElement.classList.add('js');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, el = d) => el.querySelector(s);
  const $$ = (s, el = d) => [...el.querySelectorAll(s)];
  const WA = '5997009744';

  /* ---------- Store hours, in Bonaire time ---------- */
  const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const STORES = {
    playa:   { name: 'Beachvibes Playa',   open: [0, 1, 1, 1, 1, 1, 1].map((o, i) => i === 0 ? null : [10, 17]) },
    salty:   { name: 'Salty Crew Bonaire', open: [null, [10, 17], [10, 17], [10, 17], [10, 17], [10, 17], [10, 17]] },
    sorobon: { name: 'Beachvibes Sorobon', open: [[10, 17], [10, 17], [10, 17], [10, 17], [10, 17], [10, 17], [10, 17]] }
  };
  // Bonaire is UTC-4 all year (no daylight saving), so plain UTC maths is exact.
  function bonaireNow() {
    const t = new Date(Date.now() - 4 * 3600e3);
    return { day: t.getUTCDay(), mins: t.getUTCHours() * 60 + t.getUTCMinutes() };
  }
  const hh = h => String(h).padStart(2, '0') + ':00';
  function status(key) {
    const s = STORES[key]; if (!s) return null;
    const { day, mins } = bonaireNow();
    const today = s.open[day];
    if (today && mins >= today[0] * 60 && mins < today[1] * 60) return { open: true, text: `Open now, closes ${hh(today[1])}` };
    if (today && mins < today[0] * 60) return { open: false, text: `Closed, opens ${hh(today[0])} today` };
    for (let i = 1; i <= 7; i++) {
      const dd = (day + i) % 7, o = s.open[dd];
      if (o) return { open: false, text: `Closed, opens ${i === 1 ? 'tomorrow' : DAYS[dd]} ${hh(o[0])}` };
    }
    return { open: false, text: 'Closed' };
  }
  function paintStatus() {
    $$('[data-status]').forEach(el => {
      const st = status(el.dataset.status); if (!st) return;
      el.classList.toggle('is-open', st.open);
      const t = $('[data-status-text]', el) || el;
      const prefix = el.dataset.prefix ? el.dataset.prefix + ': ' : '';
      t.textContent = prefix + (el.dataset.short && st.open ? 'open now' : el.dataset.short ? 'closed now' : st.text);
    });
    const { day } = bonaireNow();
    $$('.hours tr[data-days]').forEach(tr => tr.classList.toggle('is-today', tr.dataset.days.split(' ').includes(String(day))));
  }
  paintStatus(); setInterval(paintStatus, 60000);

  /* ---------- Header ---------- */
  const header = $('.site-header');
  let scrolledAt = 8; // header turns solid after this many px
  const onScroll = () => header && header.classList.toggle('is-scrolled', scrollY > scrolledAt);
  addEventListener('scroll', onScroll, { passive: true });

  /* ---------- Hero logo docks into the header (home) ---------- */
  const heroLogo = $('.hero-logo'), slot = $('.hero-logo-slot'), headLogo = $('.site-header .brand .logo-ink');
  if (heroLogo && slot && headLogo && !reduce) {
    const root = d.documentElement;
    let start, end, dist, ticking = false;
    const ease = t => 1 - (1 - t) * (1 - t);
    const measure = () => {
      root.classList.remove('dock');
      if (heroLogo.parentNode !== slot) slot.appendChild(heroLogo);
      heroLogo.style.transform = ''; heroLogo.style.width = ''; heroLogo.style.height = ''; heroLogo.style.filter = '';
      const r = slot.getBoundingClientRect(), img = heroLogo.getBoundingClientRect();
      start = { x: img.left, y: img.top + scrollY, w: img.width, h: img.height };
      // target = the header logo in its final, scrolled state, with the header stuck to the top
      const hs = headLogo.style.transition; headLogo.style.transition = 'none';
      header.classList.add('is-scrolled'); headLogo.style.display = 'block';
      const e = headLogo.getBoundingClientRect(), ht = header.getBoundingClientRect().top;
      end = { x: e.left, y: e.top - ht, w: e.width, h: e.height };
      headLogo.style.display = ''; header.classList.remove('is-scrolled'); headLogo.style.transition = hs;
      dist = Math.max(80, start.y - end.y); // it docks exactly when it scrolls up to the header
      scrolledAt = dist - 2;
      heroLogo.style.width = start.w + 'px'; heroLogo.style.height = start.h + 'px';
      d.body.appendChild(heroLogo); // out of the hero, so nothing can draw over it
      root.classList.add('dock');
      frame();
    };
    const frame = () => {
      ticking = false;
      const p = Math.min(1, Math.max(0, scrollY / dist)), k = ease(p);
      // rides up with the page (so it never covers the text) while shrinking toward the header logo
      const y = Math.max(end.y, start.y - scrollY), x = start.x + (end.x - start.x) * k;
      const s = 1 + (end.w / start.w - 1) * k;
      heroLogo.style.transform = `translate3d(${x.toFixed(1)}px,${y.toFixed(1)}px,0) scale(${s.toFixed(4)})`;
      // fade from white to the dark header logo over the last stretch, so the swap is invisible
      const ink = Math.min(1, Math.max(0, (p - .55) / .45));
      heroLogo.style.filter = `brightness(${(1 - ink * .92).toFixed(3)}) drop-shadow(0 4px 18px rgba(14,42,59,${(.35 * (1 - ink)).toFixed(3)}))`;
      const docked = p >= 1;
      heroLogo.style.visibility = docked ? 'hidden' : 'visible';
      root.classList.toggle('dock-pending', !docked);
      onScroll();
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }, { passive: true });
    addEventListener('resize', () => requestAnimationFrame(measure));
    (heroLogo.complete ? measure() : heroLogo.addEventListener('load', measure, { once: true }));
    d.fonts && d.fonts.ready.then(measure);
  }
  onScroll();

  const menuBtn = $('.menu-btn'), mnav = $('.mobile-nav');
  if (menuBtn && mnav) {
    const setNav = open => {
      menuBtn.setAttribute('aria-expanded', open);
      menuBtn.querySelector('span').textContent = open ? 'Close' : 'Menu';
      mnav.classList.toggle('is-open', open);
      mnav.toggleAttribute('inert', !open);
      d.body.classList.toggle('nav-open', open);
      if (open) $('a', mnav).focus();
    };
    mnav.setAttribute('inert', '');
    menuBtn.addEventListener('click', () => setNav(menuBtn.getAttribute('aria-expanded') !== 'true'));
    d.addEventListener('keydown', e => { if (e.key === 'Escape' && mnav.classList.contains('is-open')) { setNav(false); menuBtn.focus(); } });
    matchMedia('(min-width: 981px)').addEventListener('change', e => e.matches && setNav(false));
  }

  /* ---------- Hero: one orchestrated entrance ---------- */
  const hero = $('.hero');
  if (hero) {
    const img = $('.hero-media img, .hero-bg', hero);
    const go = () => requestAnimationFrame(() => hero.classList.add('is-in'));
    if (reduce || !img || img.complete) setTimeout(go, 60); else { img.addEventListener('load', go, { once: true }); setTimeout(go, 1200); }
  }

  /* ---------- Rails ---------- */
  $$('[data-rail]').forEach(wrap => {
    const rail = $('.rail', wrap), prev = $('[data-prev]', wrap), next = $('[data-next]', wrap);
    if (!rail) return;
    const step = () => rail.firstElementChild.getBoundingClientRect().width + 20;
    const upd = () => { prev.disabled = rail.scrollLeft < 8; next.disabled = rail.scrollLeft + rail.clientWidth > rail.scrollWidth - 8; };
    prev && prev.addEventListener('click', () => rail.scrollBy({ left: -step(), behavior: reduce ? 'auto' : 'smooth' }));
    next && next.addEventListener('click', () => rail.scrollBy({ left: step(), behavior: reduce ? 'auto' : 'smooth' }));
    rail.addEventListener('scroll', upd, { passive: true }); addEventListener('resize', upd); upd();
  });

  /* ---------- Product filters ---------- */
  const filters = $('[data-filters]');
  if (filters) {
    const items = $$('[data-cat]');
    filters.addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      $$('button', filters).forEach(x => x.setAttribute('aria-pressed', x === b));
      const f = b.dataset.filter;
      let n = 0;
      items.forEach(it => { const show = f === 'all' || it.dataset.cat.split(' ').includes(f); it.hidden = !show; n += show; });
      const live = $('[data-result-count]'); if (live) live.textContent = `${n} ${n === 1 ? 'item' : 'items'} shown`;
    });
  }

  /* ---------- Quick view ---------- */
  const qv = $('#quickview');
  if (qv) {
    let lastFocus;
    $$('[data-product]').forEach(btn => btn.addEventListener('click', () => {
      const p = JSON.parse(btn.dataset.product);
      lastFocus = btn;
      const media = $('.qv-media', qv);
      media.classList.toggle('is-packshot', !!p.packshot);
      $('img', media).src = p.img; $('img', media).alt = p.alt;
      $('h2', qv).textContent = p.name;
      $('[data-qv-brand]', qv).textContent = p.brand;
      $('[data-qv-price]', qv).textContent = p.price || 'Ask in store';
      $('[data-qv-where]', qv).textContent = p.where;
      $('[data-qv-note]', qv).textContent = p.note || '';
      const opts = $('[data-qv-opts]', qv);
      opts.innerHTML = '';
      if (p.colors && p.colors.length) {
        opts.hidden = false;
        opts.innerHTML = '<legend>Colour</legend>' + p.colors.map((c, i) =>
          `<label class="opt"><input type="radio" name="qv-color" value="${c[0]}" ${i ? '' : 'checked'}><span><i style="background:${c[1]}"></i>${c[0]}</span></label>`).join('');
      } else opts.hidden = true;
      const wa = $('[data-qv-wa]', qv);
      const build = () => {
        const col = $('input[name="qv-color"]:checked', qv);
        const msg = `Hi Beachvibes! Could you put aside the ${p.name}${col ? ' in ' + col.value : ''} for me? I'd like to pick it up at ${p.whereShort || 'the store'}.`;
        wa.href = `https://wa.me/${WA}?text=${encodeURIComponent(msg)}`;
      };
      build(); opts.onchange = build;
      qv.showModal();
    }));
    qv.addEventListener('close', () => lastFocus && lastFocus.focus());
    qv.addEventListener('click', e => { if (e.target === qv) qv.close(); });
    $('[data-close]', qv).addEventListener('click', () => qv.close());
  }

  /* ---------- Lookbook tabs + lightbox ---------- */
  const tablist = $('[role="tablist"]');
  if (tablist) {
    const tiles = $$('.masonry button');
    const tabs = $$('[role="tab"]', tablist);
    const select = tab => {
      tabs.forEach(t => { t.setAttribute('aria-selected', t === tab); t.tabIndex = t === tab ? 0 : -1; });
      const f = tab.dataset.set;
      tiles.forEach(t => t.hidden = !(f === 'all' || t.dataset.set.split(' ').includes(f)));
    };
    tablist.addEventListener('click', e => { const t = e.target.closest('[role="tab"]'); t && select(t); });
    tablist.addEventListener('keydown', e => {
      const i = tabs.indexOf(d.activeElement); if (i < 0) return;
      const n = e.key === 'ArrowRight' ? (i + 1) % tabs.length : e.key === 'ArrowLeft' ? (i - 1 + tabs.length) % tabs.length : -1;
      if (n > -1) { e.preventDefault(); tabs[n].focus(); select(tabs[n]); }
    });
  }
  const lb = $('#lightbox');
  if (lb) {
    const tiles = () => $$('.masonry button:not([hidden])');
    let idx = 0, opener;
    const show = i => {
      const list = tiles(); idx = (i + list.length) % list.length;
      const src = list[idx].querySelector('img');
      const im = $('.lb-stage img', lb); im.src = src.currentSrc || src.src; im.alt = src.alt;
      $('[data-lb-count]', lb).textContent = `${idx + 1} of ${list.length}`;
    };
    d.addEventListener('click', e => {
      const t = e.target.closest('.masonry button'); if (!t) return;
      opener = t; show(tiles().indexOf(t)); lb.showModal();
    });
    $('[data-lb-prev]', lb).addEventListener('click', () => show(idx - 1));
    $('[data-lb-next]', lb).addEventListener('click', () => show(idx + 1));
    $('[data-close]', lb).addEventListener('click', () => lb.close());
    lb.addEventListener('keydown', e => { if (e.key === 'ArrowRight') show(idx + 1); if (e.key === 'ArrowLeft') show(idx - 1); });
    lb.addEventListener('close', () => opener && opener.focus());
    let x0 = null;
    $('.lb-stage', lb).addEventListener('pointerdown', e => x0 = e.clientX);
    $('.lb-stage', lb).addEventListener('pointerup', e => { if (x0 === null) return; const dx = e.clientX - x0; if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1)); x0 = null; });
  }

  /* ---------- Brands A–Z preview ---------- */
  const azPrev = $('.az-preview');
  if (azPrev) {
    const img = $('img', azPrev), cap = $('figcaption', azPrev);
    $$('.az-list li').forEach(li => {
      const act = () => {
        if (!li.dataset.img) return;
        $$('.az-list li').forEach(x => x.classList.toggle('is-active', x === li));
        if (img.getAttribute('src') !== li.dataset.img) { img.style.opacity = 0; setTimeout(() => { img.src = li.dataset.img; img.style.opacity = 1; }, reduce ? 0 : 180); }
        cap.textContent = li.dataset.name;
      };
      li.addEventListener('mouseenter', act); li.addEventListener('focusin', act);
    });
  }

  /* ---------- Island map: link pins and cards ---------- */
  $$('[data-island]').forEach(sec => {
    const pins = $$('.pin', sec), cards = $$('.store-card', sec);
    const activate = key => {
      pins.forEach(p => p.classList.toggle('is-active', p.dataset.store === key));
      cards.forEach(c => c.classList.toggle('is-active', c.dataset.store === key));
    };
    cards.forEach(c => { c.addEventListener('mouseenter', () => activate(c.dataset.store)); c.addEventListener('focusin', () => activate(c.dataset.store)); });
    pins.forEach(p => {
      const go = () => { activate(p.dataset.store); const c = cards.find(c => c.dataset.store === p.dataset.store); c && c.querySelector('a').focus({ preventScroll: true }); c && c.scrollIntoView({ block: 'nearest', behavior: reduce ? 'auto' : 'smooth' }); };
      p.addEventListener('click', go); p.addEventListener('mouseenter', () => activate(p.dataset.store));
      p.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
    });
  });

  /* ---------- Newsletter ---------- */
  $$('[data-signup]').forEach(form => {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const email = form.elements.email, err = $('[data-email-error]', form);
      const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
      email.setAttribute('aria-invalid', !ok); err.hidden = ok;
      if (!ok) { err.textContent = 'Enter an email address like name@example.com.'; email.focus(); return; }
      const first = form.elements.first.value.trim();
      form.innerHTML = `<p class="form-done" role="status">You're on the list${first ? ', ' + first.replace(/[<>&"]/g, '') : ''}. We'll email you when new arrivals land.</p>`;
    });
  });

  /* ---------- Bracelet builder ---------- */
  const bf = $('#builder');
  if (bf) {
    const svg = $('#bracelet');
    const beadsG = $('#beads', svg), cord = $('#cord', svg), charmG = $('#charm', svg), knot = $('#knot', svg);
    const PALETTES = {
      lagoon: ['#3CC8B4', '#F4F6F3', '#8FE0D3', '#0C766B'],
      flamingo: ['#F27BA6', '#FCE6EE', '#F6C343', '#F4F6F3'],
      sunset: ['#F6C343', '#F2905A', '#F27BA6', '#B83467'],
      reef: ['#0E2A3B', '#3CC8B4', '#F4F6F3', '#5B8FA8'],
      salt: ['#F4F6F3', '#E9DCC8', '#D4AF6A', '#FFFFFF']
    };
    const CHARMS = {
      none: '',
      star: '<path d="M0-15 4.4-4.8 15.6-4.6 6.8 2.4 10 13.2 0 6.9-10 13.2-6.8 2.4-15.6-4.6-4.4-4.8Z"/>',
      shell: '<path d="M0 14C-9 14-15 6-15-2-15-9-8-15 0-15S15-9 15-2C15 6 9 14 0 14Z"/><path d="M0 14V-13M0 14-8-11M0 14 8-11M0 14-13-4M0 14 13-4" fill="none" stroke="rgba(0,0,0,.25)" stroke-width="1.3"/>',
      sun: '<circle r="8"/><g stroke-width="2.6" stroke-linecap="round">' + Array.from({ length: 8 }, (_, i) => { const a = i * Math.PI / 4; return `<line x1="${(Math.cos(a) * 11).toFixed(1)}" y1="${(Math.sin(a) * 11).toFixed(1)}" x2="${(Math.cos(a) * 16).toFixed(1)}" y2="${(Math.sin(a) * 16).toFixed(1)}"/>`; }).join('') + '</g>',
      wave: '<path d="M-15 6C-15-4-7-12 2-12 10-12 15-6 12 0 9 5 2 3 3-2 4-6 9-5 9-2" fill="none" stroke-width="4.2" stroke-linecap="round"/><path d="M-15 6H15" stroke-width="3.4" stroke-linecap="round"/>',
      donkey: '<path d="M-12 10V-1C-12-6-8-8-3-8H6L8-14 10-8C14-7 15-3 15 0L11 2V10H8V3H-6V10Z"/>'
    };
    const metal = { gold: '#D4AF37', silver: '#C9CED3' };
    const cx = 260, cy = 250, rx = 200, ry = 150;
    const render = () => {
      const f = new FormData(bf);
      const cordCol = f.get('cord'), pal = PALETTES[f.get('palette')], size = +f.get('size'), charm = f.get('charm'), m = metal[f.get('metal')];
      const count = Math.round(size * 2.1);
      cord.setAttribute('stroke', cordCol);
      let html = '';
      for (let i = 0; i < count; i++) {
        const t = Math.PI / 2 + (i + .5) / count * Math.PI * 2 * 0.86 + Math.PI * 0.07;
        const x = cx + Math.cos(t) * rx, y = cy + Math.sin(t) * ry;
        const depth = (Math.sin(t) + 1) / 2;
        const r = 9 + depth * 5;
        const c = pal[i % pal.length];
        html += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r.toFixed(1)}" fill="${c}" stroke="rgba(14,42,59,.18)" stroke-width="1"/><circle cx="${(x - r * .35).toFixed(1)}" cy="${(y - r * .35).toFixed(1)}" r="${(r * .28).toFixed(1)}" fill="#fff" opacity=".55"/>`;
      }
      beadsG.innerHTML = html;
      knot.setAttribute('fill', cordCol);
      charmG.innerHTML = CHARMS[charm] ? `<line x1="0" y1="-24" x2="0" y2="-12" stroke="${m}" stroke-width="2.4"/><circle cy="-26" r="4" fill="none" stroke="${m}" stroke-width="2.2"/><g fill="${m}" stroke="${m}">${CHARMS[charm]}</g>` : '';
      const labels = { cord: $(`input[name=cord]:checked`, bf).dataset.label, palette: $(`input[name=palette]:checked`, bf).dataset.label, charm: $(`input[name=charm]:checked`, bf).dataset.label, metal: $(`input[name=metal]:checked`, bf).dataset.label };
      const line = `${labels.cord} cord, ${labels.palette.toLowerCase()} beads, ${charm === 'none' ? 'no charm' : labels.metal.toLowerCase() + ' ' + labels.charm.toLowerCase() + ' charm'}, ${size} cm`;
      $('[data-size-out]').textContent = size + ' cm';
      $('[data-summary]').textContent = line;
      $('#bracelet-desc').textContent = 'Preview: ' + line;
      $('[data-builder-wa]').href = `https://wa.me/${WA}?text=${encodeURIComponent('Hi Beachvibes! I designed a bracelet on your site: ' + line + '. Can you make it for me?')}`;
    };
    bf.addEventListener('input', render); render();
  }

  /* ---------- Year ---------- */
  $$('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
})();

/* brand band: slow auto-slide, pauses on hover/touch so visitors can scroll it themselves */
(() => {
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.brand-band').forEach(band => {
    const dir = band.classList.contains('brand-band--rev') ? -1 : 1;
    let paused = false, drag = null, pos = 0, last = 0;
    const half = () => band.scrollWidth / 2;
    const wrap = () => { const h = half(); if (band.scrollLeft >= h) band.scrollLeft -= h; else if (band.scrollLeft <= 0) band.scrollLeft += h; };
    band.addEventListener('mouseenter', () => paused = true);
    band.addEventListener('mouseleave', () => { paused = false; drag = null; band.classList.remove('is-dragging'); });
    band.addEventListener('focusin', () => paused = true);
    band.addEventListener('focusout', () => paused = false);
    band.addEventListener('touchstart', () => paused = true, { passive: true });
    band.addEventListener('touchend', () => setTimeout(() => paused = false, 2500), { passive: true });
    band.addEventListener('wheel', e => { if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) { band.scrollLeft += e.deltaY; e.preventDefault(); } wrap(); }, { passive: false });
    band.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; drag = { x: e.clientX, s: band.scrollLeft, moved: false }; band.classList.add('is-dragging'); });
    addEventListener('pointermove', e => { if (!drag) return; const dx = e.clientX - drag.x; if (Math.abs(dx) > 4) drag.moved = true; band.scrollLeft = drag.s - dx; wrap(); });
    addEventListener('pointerup', () => { if (drag) { band.classList.remove('is-dragging'); setTimeout(() => drag = null, 0); } });
    band.addEventListener('click', e => { if (drag && drag.moved) e.preventDefault(); }, true);
    band.addEventListener('scroll', () => { if (paused) wrap(); }, { passive: true });
    if (dir < 0) band.scrollLeft = half();
    pos = band.scrollLeft;
    const tick = t => {
      const dt = last ? Math.min(64, t - last) : 16; last = t;
      if (paused || still || drag) { pos = band.scrollLeft; }
      else {
        const h = half();
        pos += dir * dt * 0.04; // own float position: scrollLeft rounds tiny steps away
        if (pos >= h) pos -= h; else if (pos <= 0) pos += h;
        band.scrollLeft = pos;
      }
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });
})();
