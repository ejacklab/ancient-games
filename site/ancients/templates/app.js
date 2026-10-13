/* The reading state: what the reader chose, who they are on, how far each person is read.
   Settings, the current person and every panel's scroll offset live in localStorage (in try/catch,
   because a private window or blocked site data must not stop the page). Defaults are baked in by
   build.py; the reader's own choices win over them. */

(function () {
  "use strict";

  var KEY_PREFS = "ancients:prefs";
  var KEY_PERSON = "ancients:person";
  var KEY_SCROLL = "ancients:scroll:";
  var SWIPE = 40;

  var DEFAULTS = __DEFAULTS__;
  var FONTS = {
    literata: "'Literata', 'Noto Serif TC', 'Songti TC', 'PMingLiU', Georgia, serif",
    georgia: "Georgia, 'Noto Serif TC', 'Songti TC', 'PMingLiU', serif",
    sans: "system-ui, -apple-system, 'Segoe UI', 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', sans-serif",
    hyper: "'Atkinson Hyperlegible', 'Noto Sans TC', 'PingFang TC', sans-serif"
  };
  var LEADINGS = { compact: 1.35, normal: 1.6, loose: 1.9 };
  var MARGINS = { narrow: "3%", normal: "8%", wide: "14%" };
  var ALIGNS = { justify: "justify", left: "left" };

  function load(key) {
    try {
      var raw = localStorage.getItem(key);
      return raw === null ? null : JSON.parse(raw);
    } catch (e) { return null; }
  }
  function save(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) {}
  }

  var prefs = Object.assign({}, DEFAULTS, load(KEY_PREFS) || {});
  var row = document.getElementById("people");
  var panels = Array.prototype.slice.call(row.querySelectorAll("section.person"));
  var dots = Array.prototype.slice.call(document.querySelectorAll("#dots button"));
  var menu = document.getElementById("menu");
  var aa = document.getElementById("aa");
  var nameEl = document.getElementById("person-name");
  var posEl = document.getElementById("person-pos");
  var names = panels.map(function (panel) { return panel.querySelector(".person-name").textContent.trim(); });
  var current = 0, rowFrame = 0, panelFrames = [];
  var wantedPerson = load(KEY_PERSON);
  var wantedOffsets = panels.map(function (panel) {
    var saved = load(KEY_SCROLL + panel.getAttribute("data-person"));
    return typeof saved === "number" ? saved : null;
  });

  function indexOf() {
    var width = row.clientWidth || 1;
    return Math.max(0, Math.min(panels.length - 1, Math.round(row.scrollLeft / width)));
  }
  function scrollRoom(panel) { return panel.scrollHeight - panel.clientHeight; }
  function readFraction(panel) {
    var room = scrollRoom(panel);
    return room > 0 ? Math.min(1, Math.max(0, panel.scrollTop / room)) : 0;
  }
  function seekFraction(panel, fraction) {
    var room = scrollRoom(panel);
    panel.scrollTop = room > 0 ? fraction * room : 0;
  }
  function showPct(panel) {
    var el = panel.querySelector(".pct");
    if (el) el.textContent = Math.round(readFraction(panel) * 100) + "%";
  }

  function paintChoices() {
    menu.querySelectorAll("button[data-setting]").forEach(function (button) {
      var chosen = String(prefs[button.getAttribute("data-setting")]);
      button.classList.toggle("on", chosen === button.getAttribute("data-value"));
    });
  }

  function applySettings() {
    var where = panels.map(readFraction);
    var s = document.documentElement.style;
    s.setProperty("--font", FONTS[prefs.font] || FONTS[DEFAULTS.font]);
    s.setProperty("--size", (Number(prefs.size) || DEFAULTS.size) + "px");
    s.setProperty("--leading", LEADINGS[prefs.leading] || LEADINGS[DEFAULTS.leading]);
    s.setProperty("--margin", MARGINS[prefs.margin] || MARGINS[DEFAULTS.margin]);
    s.setProperty("--align", ALIGNS[prefs.align] || ALIGNS[DEFAULTS.align]);
    document.documentElement.setAttribute("data-theme", prefs.theme || DEFAULTS.theme);
    paintChoices();
    save(KEY_PREFS, prefs);
    panels.forEach(function (panel, i) { seekFraction(panel, where[i]); showPct(panel); });
  }

  function paintHeader() {
    current = indexOf();
    nameEl.textContent = names[current];
    posEl.textContent = (current + 1) + " / " + panels.length;
    dots.forEach(function (dot, i) {
      dot.classList.toggle("on", i === current);
      if (i === current) dot.setAttribute("aria-current", "true"); else dot.removeAttribute("aria-current");
    });
  }

  function goTo(i) {
    var target = Math.max(0, Math.min(panels.length - 1, i));
    row.scrollLeft = target * row.clientWidth;
    paintHeader();
    save(KEY_PERSON, target);
  }

  function openMenu(on) {
    menu.classList.toggle("open", on);
    menu.setAttribute("aria-hidden", on ? "false" : "true");
    aa.setAttribute("aria-expanded", on ? "true" : "false");
  }

  function restore() {
    applySettings();
    if (typeof wantedPerson === "number") goTo(wantedPerson); else paintHeader();
    panels.forEach(function (panel, i) {
      if (wantedOffsets[i] !== null) panel.scrollTop = Math.max(0, wantedOffsets[i]);
      showPct(panel);
    });
  }

  menu.addEventListener("click", function (event) {
    var button = event.target.closest ? event.target.closest("button[data-setting]") : null;
    if (!button) return;
    var setting = button.getAttribute("data-setting");
    var value = button.getAttribute("data-value");
    prefs[setting] = setting === "size" ? Number(value) : value;
    applySettings();
  });
  document.getElementById("done").addEventListener("click", function () { openMenu(false); });
  aa.addEventListener("click", function () { openMenu(!menu.classList.contains("open")); });
  document.addEventListener("click", function (event) {
    if (!menu.classList.contains("open")) return;
    if (menu.contains(event.target) || aa.contains(event.target)) return;
    openMenu(false);
  });
  dots.forEach(function (dot) {
    dot.addEventListener("click", function () { goTo(Number(dot.getAttribute("data-goto"))); });
  });

  row.addEventListener("scroll", function () {
    if (rowFrame) return;
    rowFrame = requestAnimationFrame(function () { rowFrame = 0; paintHeader(); save(KEY_PERSON, current); });
  }, { passive: true });
  panels.forEach(function (panel, i) {
    panelFrames[i] = 0;
    panel.addEventListener("scroll", function () {
      if (panelFrames[i]) return;
      panelFrames[i] = requestAnimationFrame(function () {
        panelFrames[i] = 0;
        showPct(panel);
        save(KEY_SCROLL + panel.getAttribute("data-person"), Math.round(panel.scrollTop));
      });
    }, { passive: true });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") return openMenu(false);
    if (menu.classList.contains("open")) return;
    if (event.key === "ArrowRight" || event.key === "PageDown") { event.preventDefault(); goTo(current + 1); }
    if (event.key === "ArrowLeft" || event.key === "PageUp") { event.preventDefault(); goTo(current - 1); }
    if (event.key === "Home") goTo(0);
    if (event.key === "End") goTo(panels.length - 1);
  });

  var resizeTimer;
  window.addEventListener("resize", function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () { goTo(current); }, 150);
  });

  function panelOf(node) {
    return node && node.closest ? node.closest("section.person") : null;
  }

  // A swipe turns the seat, the kindle-page way: from where the finger went down to where it came up.
  // Only when the browser did not scroll the gesture itself — a real phone scrolls and snaps, and then
  // this stands aside; a browser or webview that gives touch gestures no scrolling gets the same turn.
  var swipe = null;
  document.addEventListener("touchstart", function (event) {
    var panel = panelOf(event.target);
    if (!panel || menu.contains(event.target)) { swipe = null; return; }
    var touch = event.changedTouches[0];
    swipe = { x: touch.clientX, y: touch.clientY, panel: panel,
              rowLeft: row.scrollLeft, panelTop: panel.scrollTop };
  }, { passive: true });
  document.addEventListener("touchend", function (event) {
    if (!swipe) return;
    var start = swipe;
    swipe = null;
    var touch = event.changedTouches[0];
    var dx = touch.clientX - start.x, dy = touch.clientY - start.y;
    if (Math.abs(dx) > SWIPE && Math.abs(dx) > Math.abs(dy) && row.scrollLeft === start.rowLeft) {
      goTo(current + (dx < 0 ? 1 : -1));
    } else if (Math.abs(dy) > SWIPE && Math.abs(dy) > Math.abs(dx) && start.panel.scrollTop === start.panelTop) {
      start.panel.scrollTop = start.panelTop - dy;
      showPct(start.panel);
    }
  }, { passive: true });

  restore();
  panels.forEach(showPct);
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () { restore(); panels.forEach(showPct); });
  }
  setTimeout(function () { panels.forEach(showPct); }, 800);
})();