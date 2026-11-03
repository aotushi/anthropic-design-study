/* Browsing interactions adapted from the public Academy experience. */
(() => {
  'use strict';
  const copy = window.STUDY_COPY;
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const menus = [...document.querySelectorAll('.header-disclosure')];
  const timers = new WeakMap();
  function closeMenus(except) {
    menus.forEach(menu => {
      clearTimeout(timers.get(menu));
      if (menu !== except) menu.open = false;
    });
  }
  menus.forEach(menu => {
    const trigger = menu.querySelector('summary');
    menu.addEventListener('toggle', () => { if (menu.open) closeMenus(menu); });
    menu.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'mouse' || !matchMedia('(hover: hover)').matches) return;
      clearTimeout(timers.get(menu));
      timers.set(menu, setTimeout(() => { closeMenus(menu); menu.open = true; }, 120));
    });
    menu.addEventListener('pointerleave', () => {
      clearTimeout(timers.get(menu));
      timers.set(menu, setTimeout(() => { if (!menu.contains(document.activeElement)) menu.open = false; }, 180));
    });
    trigger.addEventListener('keydown', event => {
      if (event.key === 'ArrowDown') {
        event.preventDefault();
        closeMenus(menu);
        menu.open = true;
        menu.querySelector('a').focus();
      }
    });
    menu.addEventListener('focusout', () => queueMicrotask(() => {
      if (!menu.contains(document.activeElement)) menu.open = false;
    }));
  });
  document.addEventListener('pointerdown', event => {
    if (!menus.some(menu => menu.contains(event.target))) closeMenus();
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    const opened = menus.find(menu => menu.open);
    if (opened) { event.preventDefault(); closeMenus(); opened.querySelector('summary').focus(); }
    const outline = document.querySelector('.chapter-switcher[open]');
    if (outline && outline.contains(event.target)) { outline.open = false; outline.querySelector('summary').focus(); }
  });
  document.addEventListener('study-dialog-open', () => closeMenus());

  const themeButton = document.querySelector('[data-theme-toggle]');
  function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    const label = theme === 'dark' ? copy.lightTheme : copy.darkTheme;
    themeButton.setAttribute('aria-label', label);
    themeButton.title = label;
  }
  applyTheme(document.documentElement.dataset.theme || 'light');
  themeButton.addEventListener('click', () => {
    const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    applyTheme(theme);
    try { localStorage.setItem('anthropic-study-theme', theme); } catch { /* The current page can still change theme. */ }
  });
  window.addEventListener('storage', event => {
    if (event.key === 'anthropic-study-theme' && ['light', 'dark'].includes(event.newValue)) applyTheme(event.newValue);
  });

  document.querySelectorAll('[data-compare-view]').forEach(input => {
    input.addEventListener('change', () => { input.closest('.compare-panel').dataset.view = input.value; });
  });

  const cards = [...document.querySelectorAll('[data-chapter-topic]')];
  if (!cards.length) return;
  const tabs = [...document.querySelectorAll('[data-topic-filter]')];
  const search = document.querySelector('#chapter-search');
  const count = document.querySelector('#chapter-count');
  const grid = document.querySelector('#chapter-grid');
  const empty = document.querySelector('.catalog-empty');
  const clearButtons = [...document.querySelectorAll('[data-clear-chapters]')];
  let topic = 'all';
  function cancelMotion() { cards.forEach(card => card.getAnimations().forEach(animation => animation.cancel())); }
  function updateLanguageLink() {
    const link = document.querySelector('.language-switch');
    const destination = new URL(link.href);
    destination.search = location.search;
    destination.hash = location.hash;
    link.href = destination.href;
  }
  function updateUrl(push, anchor) {
    const url = new URL(location.href);
    if (topic === 'all') url.searchParams.delete('topic');
    else url.searchParams.set('topic', topic);
    if (search.value.trim()) url.searchParams.set('q', search.value.trim());
    else url.searchParams.delete('q');
    if (anchor) url.hash = anchor;
    try {
      if (url.href !== location.href) history[push ? 'pushState' : 'replaceState'](null, '', url);
    } catch { /* Filtering remains available when file URLs restrict history. */ }
    updateLanguageLink();
  }
  function filter({animate = true, writeUrl = true, push = false, anchor = ''} = {}) {
    cancelMotion();
    const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    cards.forEach(card => {
      const match = (topic === 'all' || card.dataset.chapterTopic === topic)
        && terms.every(term => card.dataset.chapterSearch.toLocaleLowerCase().includes(term));
      card.hidden = !match;
      if (match) {
        if (animate && !reducedMotion.matches) card.animate(
          [{opacity: .35, transform: 'translateY(7px)'}, {opacity: 1, transform: 'none'}],
          {duration: 180, delay: Math.min(visible, 4) * 16, easing: 'ease-out'});
        visible++;
      }
    });
    tabs.forEach(tab => {
      const selected = tab.dataset.topicFilter === topic;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      if (selected) grid.setAttribute('aria-labelledby', tab.id);
    });
    count.textContent = `${visible} ${visible === 1 ? copy.chapterUnitSingular : copy.chapterUnit}`;
    empty.hidden = visible !== 0;
    clearButtons.forEach(button => { button.disabled = topic === 'all' && !terms.length; });
    if (writeUrl) updateUrl(push, anchor);
  }
  function readUrl() {
    const params = new URL(location.href).searchParams;
    topic = tabs.some(tab => tab.dataset.topicFilter === params.get('topic')) ? params.get('topic') : 'all';
    search.value = params.get('q') || '';
    filter({animate: false, writeUrl: false});
    updateLanguageLink();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => { topic = tab.dataset.topicFilter; filter({push: true}); });
    tab.addEventListener('keydown', event => {
      const last = tabs.length - 1;
      const next = event.key === 'ArrowRight' ? (index + 1) % tabs.length
        : event.key === 'ArrowLeft' ? (index + last) % tabs.length
        : event.key === 'Home' ? 0 : event.key === 'End' ? last : null;
      if (next === null) return;
      event.preventDefault();
      topic = tabs[next].dataset.topicFilter;
      tabs[next].focus();
      filter({push: true});
    });
  });
  search.addEventListener('input', () => filter());
  clearButtons.forEach(button => button.addEventListener('click', () => {
    topic = 'all'; search.value = ''; filter({push: true}); search.focus();
  }));
  document.querySelectorAll('[data-path-topic]').forEach(link => link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); topic = link.dataset.pathTopic; search.value = '';
    filter({push: true, anchor: 'chapters'});
    const activeTab = tabs.find(tab => tab.dataset.topicFilter === topic);
    activeTab.focus({preventScroll: true});
    document.querySelector('#chapters').scrollIntoView({behavior: reducedMotion.matches ? 'instant' : 'smooth'});
  }));
  window.addEventListener('popstate', readUrl);
  reducedMotion.addEventListener('change', event => { if (event.matches) cancelMotion(); });
  let printState;
  window.addEventListener('beforeprint', () => {
    cancelMotion();
    printState = {cards: cards.map(card => [card, card.hidden]), count: count.textContent};
    cards.forEach(card => { card.hidden = false; });
    count.textContent = `${cards.length} ${copy.chapterUnit}`;
  });
  window.addEventListener('afterprint', () => {
    if (!printState) return;
    printState.cards.forEach(([card, hidden]) => { card.hidden = hidden; });
    count.textContent = printState.count;
  });
  readUrl();
})();
