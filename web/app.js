/* Local-only reading enhancements; all chapter content is already in the HTML. */
(() => {
  'use strict';
  const copy = window.STUDY_COPY;
  const searchDialog = document.querySelector('#search-dialog');
  const imageDialog = document.querySelector('#image-dialog');
  const searchInput = document.querySelector('#study-search');
  const resultList = document.querySelector('#search-results');
  const searchStatus = document.querySelector('#search-status');
  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#chapter-nav');
  const bodyContent = document.querySelector('.site-body');
  const dialogOrigins = new WeakMap();

  function setMenu(open, restore = false) {
    document.body.classList.toggle('menu-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    bodyContent.inert = open;
    if (open) navigation.querySelector('a')?.focus();
    else if (restore) menuButton.focus();
  }

  menuButton.addEventListener('click', () => setMenu(!document.body.classList.contains('menu-open'), true));
  document.querySelector('[data-close-menu]').addEventListener('click', () => setMenu(false, true));
  navigation.addEventListener('click', event => { if (event.target.closest('a')) setMenu(false); });
  window.matchMedia('(min-width: 921px)').addEventListener('change', event => { if (event.matches) setMenu(false); });

  function openDialog(dialog, origin) {
    setMenu(false);
    dialogOrigins.set(dialog, origin || document.activeElement);
    dialog.showModal();
    document.documentElement.classList.add('dialog-open');
  }
  for (const dialog of [searchDialog, imageDialog]) {
    dialog.querySelector('[data-close-dialog]').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    });
    dialog.addEventListener('close', () => {
      document.documentElement.classList.remove('dialog-open');
      dialogOrigins.get(dialog)?.focus();
    });
  }

  function openSearch(origin) {
    if (imageDialog.open) imageDialog.close();
    if (!searchDialog.open) openDialog(searchDialog, origin);
    searchInput.focus();
    searchInput.select();
  }
  document.querySelectorAll('[data-open-search]').forEach(button => button.addEventListener('click', () => openSearch(button)));

  function plainSnippet(text, terms) {
    const lower = text.toLocaleLowerCase();
    const positions = terms.map(term => lower.indexOf(term)).filter(index => index >= 0);
    const start = positions.length ? Math.max(0, Math.min(...positions) - 40) : 0;
    return (start ? '…' : '') + text.slice(start, start + 160) + (text.length > start + 160 ? '…' : '');
  }

  function search() {
    const terms = searchInput.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    resultList.replaceChildren();
    if (!terms.length) { searchStatus.textContent = searchInput.placeholder; return; }
    const matches = (window.STUDY_SEARCH || []).map(record => {
      const title = `${record.title} ${record.chapter}`.toLocaleLowerCase();
      const haystack = `${title} ${record.text}`.toLocaleLowerCase();
      return { record, match: terms.every(term => haystack.includes(term)), score: terms.filter(term => title.includes(term)).length };
    }).filter(item => item.match).sort((a, b) => b.score - a.score);
    searchStatus.textContent = matches.length ? `${matches.length} ${copy.results}` : copy.noResults;
    for (const { record } of matches.slice(0, 40)) {
      const link = document.createElement('a');
      link.className = 'search-result';
      link.href = record.href;
      const chapter = document.createElement('small');
      chapter.textContent = record.chapter;
      const title = document.createElement('strong');
      title.textContent = record.title;
      const snippet = document.createElement('p');
      snippet.textContent = plainSnippet(record.text, terms);
      link.append(chapter, title, snippet);
      link.addEventListener('click', () => searchDialog.close());
      resultList.append(link);
    }
  }
  searchInput.addEventListener('input', search);
  searchInput.addEventListener('keydown', event => {
    if (event.key === 'ArrowDown') { event.preventDefault(); resultList.querySelector('a')?.focus(); }
  });

  document.addEventListener('click', event => {
    const button = event.target.closest('[data-zoom]');
    if (!button) return;
    const source = button.querySelector('img');
    const image = document.querySelector('#enlarged-image');
    image.src = source.currentSrc || source.src;
    image.alt = source.alt;
    document.querySelector('#image-caption').textContent = source.alt;
    document.querySelector('#original-image').href = image.src;
    openDialog(imageDialog, button);
  });

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && (imageDialog.open || searchDialog.open)) {
      event.preventDefault();
      (imageDialog.open ? imageDialog : searchDialog).close();
      return;
    }
    const editing = event.target.matches('input, textarea, select, [contenteditable="true"]');
    if ((event.key === '/' && !editing) || ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k')) {
      event.preventDefault();
      openSearch(document.activeElement);
    }
    if (!document.body.classList.contains('menu-open')) return;
    if (event.key === 'Escape') { setMenu(false, true); return; }
    if (event.key === 'Tab') {
      const items = [menuButton, ...navigation.querySelectorAll('a')];
      const first = items[0], last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
  });

  document.querySelectorAll('[data-compare]').forEach(select => {
    select.addEventListener('change', () => {
      select.closest('.compare-panel').querySelectorAll('[data-sample]').forEach(panel => { panel.hidden = panel.dataset.sample !== select.value; });
    });
  });
  document.querySelectorAll('[data-filter]').forEach(button => {
    button.addEventListener('click', () => {
      const filter = button.dataset.filter;
      document.querySelectorAll('[data-filter]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      let count = 0;
      document.querySelectorAll('[data-pattern-group]').forEach(card => {
        card.hidden = filter !== 'all' && card.dataset.patternGroup !== filter;
        if (!card.hidden) count++;
      });
      document.querySelector('.pattern-count').textContent = `${count} ${copy.patterns}`;
    });
  });
  document.querySelectorAll('[data-copy-color]').forEach(button => {
    button.addEventListener('click', async () => {
      const value = button.dataset.copyColor;
      const status = document.querySelector('#copy-status');
      try {
        await navigator.clipboard.writeText(value);
        status.textContent = `${copy.copied}: ${value}`;
      } catch {
        status.textContent = `${value} — ${copy.copyFailed}`;
      }
    });
  });

  let originalDetails = [];
  let originalCards = [];
  window.addEventListener('beforeprint', () => {
    originalDetails = [...document.querySelectorAll('details')].map(item => [item, item.open]);
    originalDetails.forEach(([item]) => { item.open = true; });
    originalCards = [...document.querySelectorAll('[data-pattern-group]')].map(item => [item, item.hidden]);
    originalCards.forEach(([item]) => { item.hidden = false; });
  });
  window.addEventListener('afterprint', () => {
    originalDetails.forEach(([item, open]) => { item.open = open; });
    originalCards.forEach(([item, hidden]) => { item.hidden = hidden; });
  });
  document.querySelector('[data-print]').addEventListener('click', () => window.print());

  const progress = document.querySelector('.reading-progress span');
  let scheduled = false;
  function updateProgress() {
    const distance = document.documentElement.scrollHeight - innerHeight;
    progress.style.width = `${distance > 0 ? Math.min(100, scrollY / distance * 100) : 0}%`;
    scheduled = false;
  }
  window.addEventListener('scroll', () => {
    if (!scheduled) { scheduled = true; requestAnimationFrame(updateProgress); }
  }, { passive: true });
  window.addEventListener('resize', updateProgress);
  updateProgress();
  const sections = [...document.querySelectorAll('.prose h2[id], .prose h3[id]')];
  if ('IntersectionObserver' in window && sections.length) {
    const observer = new IntersectionObserver(entries => {
      const visible = entries.find(entry => entry.isIntersecting);
      if (!visible) return;
      document.querySelectorAll('.page-toc a').forEach(link => {
        if (decodeURIComponent(link.hash.slice(1)) === visible.target.id) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }, { rootMargin: '-90px 0px -60% 0px' });
    sections.forEach(section => observer.observe(section));
  }
})();
