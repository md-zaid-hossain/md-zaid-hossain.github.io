/* site.js · small helpers for the static site (the pages work without it).
   1. theme picker (light, dark, auto × red, blue, green), remembered in this browser
   2. live Dhaka clock on Home and in the footer, working hours from Fajr to Asr
   3. keyboard: Esc closes any open viewer, arrow keys move through a slideshow
   4. video player plays when opened and pauses when closed
   5. COPY email and CITE buttons */
(function () {
  "use strict";
  var root = document.documentElement;
  var store = {
    get: function (k, d) { try { return localStorage.getItem(k) || d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* ---------- 1. theme ---------- */
  // a few pieces (backdrop photos, the hero gear, the footer factory) change pictures or colours per theme:
  // the build lists, for each piece, which attribute values a theme changes (window.ZH_SWAP)
  var swapCache = {};
  function swapPictures(theme) {
    var map = window.ZH_SWAP || {};
    Object.keys(map).forEach(function (k) {
      document.querySelectorAll('[data-zs="' + k + '"]').forEach(function (rootEl, n) {
        var key = k + ":" + n, list = swapCache[key];
        if (!list) {
          list = swapCache[key] = [];
          [rootEl].concat(Array.prototype.slice.call(rootEl.querySelectorAll("*"))).forEach(function (el) {
            Array.prototype.forEach.call(el.attributes, function (a) {
              if (a.name !== "data-zs") list.push([el, a.name, a.value]);
            });
          });
        }
        var m = map[k][theme] || {};
        list.forEach(function (x, j) {
          var v = m.hasOwnProperty(j) ? m[j] : x[2];
          if (x[0].getAttribute(x[1]) !== v) x[0].setAttribute(x[1], v);
        });
      });
    });
  }
  function mark(group, idx) {
    group.querySelectorAll("button").forEach(function (b, i) {
      b.classList.toggle("on", i === idx);
      b.setAttribute("aria-checked", i === idx ? "true" : "false");
    });
  }
  function applyTheme() {
    var mode = store.get("zh-mode", "dark"), accent = store.get("zh-accent", "red");
    var m = mode === "auto" ? (matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark") : mode;
    var theme = m + (accent === "red" ? "" : "_" + accent);
    root.setAttribute("data-theme", theme);
    document.querySelectorAll(".tog").forEach(function (g) {
      g.className = "tog at-" + mode[0];
      mark(g, ["light", "dark", "auto"].indexOf(mode));
    });
    document.querySelectorAll(".sw").forEach(function (g) {
      g.className = "sw at-" + accent[0];
      mark(g, ["red", "blue", "green"].indexOf(accent));
    });
    swapPictures(theme);
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".tog button, .sw button");
    if (!b) return;
    var g = b.parentElement.closest(".tog, .sw");
    var i = Array.prototype.indexOf.call(g.querySelectorAll("button"), b);
    if (g.classList.contains("tog")) store.set("zh-mode", ["light", "dark", "auto"][i]);
    else store.set("zh-accent", ["red", "blue", "green"][i]);
    applyTheme();
  });
  matchMedia("(prefers-color-scheme: light)").addEventListener("change", applyTheme);
  applyTheme();

  /* ---------- 2. Dhaka clock (same maths as build/site_src/lib/prayer_hours.py) ---------- */
  var LAT = 23.8103, LON = 90.4125, TZ = 6, R = Math.PI / 180;
  function sun(jd) {
    var d = jd - 2451545.0, g = ((357.529 + 0.98560028 * d) % 360) * R, q = (280.459 + 0.98564736 * d) % 360;
    var L = ((q + 1.915 * Math.sin(g) + 0.020 * Math.sin(2 * g)) % 360) * R, e = (23.439 - 0.00000036 * d) * R;
    var ra = Math.atan2(Math.cos(e) * Math.sin(L), Math.cos(L)) / R / 15;
    var decl = Math.asin(Math.sin(e) * Math.sin(L));
    var eqt = q / 15 - (((ra % 24) + 24) % 24);
    eqt = ((eqt + 12) % 24 + 24) % 24 - 12;
    return [decl, eqt];
  }
  function julian(y, m, d) {
    if (m <= 2) { y -= 1; m += 12; }
    var A = Math.floor(y / 100), B = 2 - A + Math.floor(A / 4);
    return Math.floor(365.25 * (y + 4716)) + Math.floor(30.6001 * (m + 1)) + d + B - 1524.5;
  }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function hm(h) { var mm = Math.round((h % 1) * 60) % 60; return pad(Math.floor(h)) + ":" + pad(mm); }
  function prayer(y, m, d) {
    var s = sun(julian(y, m, d) - LON / 360 + 0.5), decl = s[0], noon = 12 - LON / 15 - s[1] + TZ, lat = LAT * R;
    function ha(alt) { return Math.acos((Math.sin(alt * R) - Math.sin(lat) * Math.sin(decl)) / (Math.cos(lat) * Math.cos(decl))) / R / 15; }
    var asrAlt = Math.atan(1 / (2 + Math.tan(Math.abs(lat - decl)))) / R;
    return { fajr: hm(noon - ha(-18)), asr: hm(noon + ha(asrAlt)) };
  }
  function tick() {
    var now = new Date(), dk = new Date(now.getTime() + TZ * 3600e3);   // Dhaka wall time in the UTC fields
    var t = pad(dk.getUTCHours()) + ":" + pad(dk.getUTCMinutes());
    var p = prayer(dk.getUTCFullYear(), dk.getUTCMonth() + 1, dk.getUTCDate()), on = p.fajr <= t && t < p.asr;
    document.querySelectorAll(".dig b").forEach(function (el) { el.textContent = t; });
    document.querySelectorAll(".ftr .cp .tm").forEach(function (el) { el.textContent = t + " GMT+6"; });
    document.querySelectorAll(".csheet em").forEach(function (el) {
      if (/^· today /.test(el.textContent)) el.textContent = "· today " + p.fajr + " to " + p.asr;
    });
    var tpl = document.getElementById(on ? "zh-on" : "zh-off");
    document.querySelectorAll(".stt").forEach(function (el) { if (tpl && el.innerHTML !== tpl.innerHTML) el.innerHTML = tpl.innerHTML; });
    var mine = pad(now.getHours()) + ":" + pad(now.getMinutes());
    var diff = Math.round((-now.getTimezoneOffset() / 60 - TZ) * 2) / 2;
    var txt = diff === 0 ? "same time as Dhaka" : (Math.abs(diff) + " h " + (diff < 0 ? "behind" : "ahead"));
    document.querySelectorAll(".yt").forEach(function (el) {
      var b = el.querySelector("b"), em = el.querySelector("em");
      if (b) b.textContent = mine;
      if (em) em.textContent = txt + " · from your device";
    });
    // analog hands: the CSS animation started at build time, so shift it by the time since then
    var built = +root.getAttribute("data-built") || 0, since = now.getTime() / 1000 - built;
    document.querySelectorAll("[style*='animation:hHand'],[style*='animation:mHand']").forEach(function (g) {
      var per = g.getAttribute("style").indexOf("hHand") > -1 ? 86400 : 3600;
      g.style.animationDelay = (-(since % per)) + "s";
    });
  }
  if (document.querySelector(".dig, .ftr .cp .tm")) { tick(); setInterval(tick, 30000); }

  /* ---------- 3. keyboard ---------- */
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      document.querySelectorAll("input.elbc:checked, input.vpc:checked, input.rtc:checked, #mnx:checked").forEach(function (c) {
        c.checked = false; c.dispatchEvent(new Event("change", { bubbles: true }));
      });
      document.querySelectorAll("input.ssr:checked").forEach(function (r) {
        var x = document.getElementById(r.name + "-x");
        if (x && x !== r) x.checked = true;
      });
    }
    if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
      var open = Array.prototype.find.call(document.querySelectorAll("input.ssr:checked"), function (r) { return !/-x$/.test(r.id); });
      if (!open) return;
      var slides = open.parentElement.querySelectorAll(".sss"), idx = +open.id.split("-").pop();
      var lab = slides[idx] && slides[idx].querySelector(e.key === "ArrowRight" ? ".ssn" : ".ssp");
      if (lab) { lab.click(); e.preventDefault(); }
    }
  });

  /* ---------- 4. video ---------- */
  document.addEventListener("change", function (e) {
    var c = e.target;
    if (!c.classList || !c.classList.contains("vpc")) return;
    var v = c.nextElementSibling && c.nextElementSibling.querySelector("video");
    if (!v) return;
    if (c.checked) { v.muted = false; var p = v.play(); if (p && p.catch) p.catch(function () {}); }
    else v.pause();
  });

  // moving previews (data-autoplay) play only while they are on screen
  var autoVids = document.querySelectorAll("video[data-autoplay]");
  if (autoVids.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        var v = en.target;
        if (en.isIntersecting) { v.preload = "auto"; var p = v.play(); if (p && p.catch) p.catch(function () {}); }
        else v.pause();
      });
    }, { rootMargin: "200px" });
    autoVids.forEach(function (v) { v.muted = true; io.observe(v); });
  }

  /* ---------- 6. loading helpers ---------- */
  // hero 3D: the first frame (.tt0) shows until the turning sprite has arrived
  var tt0 = document.querySelectorAll(".tt0");
  if (tt0.length) {
    var hide = function () { tt0.forEach(function (e) { e.classList.add("gone"); }); };
    var spriteDone = function (list) { return list.some(function (r) { return /turntable[^\/]*\.(webp|avif)$/.test(r.name) && !/frame0/.test(r.name) && r.responseEnd > 0; }); };
    if (spriteDone(performance.getEntriesByType("resource"))) setTimeout(hide, 150);
    else if ("PerformanceObserver" in window) {
      var po = new PerformanceObserver(function (l) { if (spriteDone(l.getEntries())) { setTimeout(hide, 150); po.disconnect(); } });
      try { po.observe({ type: "resource", buffered: true }); } catch (e) { setTimeout(hide, 4000); }
    } else setTimeout(hide, 4000);
  }
  // slideshow: when a photo opens, fetch it and its neighbours at once
  document.addEventListener("change", function (e) {
    var r = e.target;
    if (!r.classList || !r.classList.contains("ssr") || /-x$/.test(r.id)) return;
    var slides = r.parentElement.querySelectorAll(".sss"), i = +r.id.split("-").pop();
    [i, i + 1, i - 1].forEach(function (k) {
      var sl = slides[(k + slides.length) % slides.length], im = sl && sl.querySelector("img");
      if (im) im.loading = "eager";
    });
  });
  /* ---------- 7. phone: Back closes an open viewer, swipe moves through a slideshow ---------- */
  var OVERLAY = "input.elbc:checked, input.vpc:checked, input.rtc:checked, #mnx:checked";
  function openSlides() {
    return Array.prototype.filter.call(document.querySelectorAll("input.ssr:checked"), function (r) { return !/-x$/.test(r.id); });
  }
  function anyOpen() { return !!document.querySelector(OVERLAY) || openSlides().length > 0; }
  function closeAll() {
    document.querySelectorAll(OVERLAY).forEach(function (c) { c.checked = false; c.dispatchEvent(new Event("change", { bubbles: true })); });
    openSlides().forEach(function (r) { var x = document.getElementById(r.name + "-x"); if (x) { x.checked = true; x.dispatchEvent(new Event("change", { bubbles: true })); } });
  }
  var pushed = false, closingByBack = false;
  document.addEventListener("change", function () {
    setTimeout(function () {
      var open = anyOpen();
      if (open && !pushed) { history.pushState({ zhViewer: 1 }, ""); pushed = true; }
      else if (!open && pushed && !closingByBack) { pushed = false; history.back(); }
    }, 0);
  });
  window.addEventListener("popstate", function () {
    if (!pushed) return;
    pushed = false; closingByBack = true; closeAll();
    setTimeout(function () { closingByBack = false; }, 0);
  });
  var tx = null, ty = 0;
  document.addEventListener("touchstart", function (e) {
    if (!e.target.closest || !e.target.closest(".sss") || e.touches.length !== 1) { tx = null; return; }
    tx = e.touches[0].clientX; ty = e.touches[0].clientY;
  }, { passive: true });
  document.addEventListener("touchend", function (e) {
    if (tx === null) return;
    var t = e.changedTouches[0], dx = t.clientX - tx, dy = t.clientY - ty; tx = null;
    if (Math.abs(dx) < 50 || Math.abs(dx) < Math.abs(dy) * 1.5) return;
    var open = openSlides()[0]; if (!open) return;
    var slides = open.parentElement.querySelectorAll(".sss"), i = +open.id.split("-").pop();
    var lab = slides[i] && slides[i].querySelector(dx < 0 ? ".ssn" : ".ssp");
    if (lab) lab.click();
  }, { passive: true });

  /* ---------- 5. copy buttons ---------- */
  function copy(text, el, label) {
    var done = function () { var o = el.textContent; el.textContent = label; setTimeout(function () { el.textContent = o; }, 1600); };
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () {});
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".cp2");
    if (b) { var em = b.parentElement.querySelector(".em"); if (em) copy(em.textContent.trim(), b, "COPIED"); return; }
    var c = e.target.closest("[data-cite]");
    if (c) { e.preventDefault(); copy(c.getAttribute("data-cite"), c, "COPIED"); }
  });
})();
