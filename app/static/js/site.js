/* Portfolio - interactions douces : thème, menu, révélations au scroll, compteurs,
   frise animée, effets de lumière. Tout est désactivé si prefers-reduced-motion. */
(function () {
  "use strict";
  var doc = document, root = doc.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (sel, ctx) { return (ctx || doc).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); };

  /* ----- Thème clair / sombre ----- */
  var toggle = $(".theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var dark = root.classList.toggle("dark");
      try { localStorage.setItem("theme", dark ? "dark" : "light"); } catch (e) {}
    });
  }

  /* ----- Menu mobile ----- */
  var header = $(".site-header"), menuBtn = $(".menu-btn");
  if (header && menuBtn) {
    menuBtn.addEventListener("click", function () {
      var open = header.classList.toggle("menu-open");
      menuBtn.setAttribute("aria-expanded", String(open));
    });
    $$(".mobile-menu a").forEach(function (a) {
      a.addEventListener("click", function () {
        header.classList.remove("menu-open");
        menuBtn.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ----- Formulaire de contact (Formspree) ----- */
  $$("form[data-formspree]").forEach(function (form) {
    var status = $(".form-status", form), button = $("button[type=submit]", form);
    form.addEventListener("submit", function (e) {
      if (!window.fetch) return; // sans JS moderne : envoi classique vers Formspree
      e.preventDefault();
      button.disabled = true;
      status.className = "form-status";
      status.textContent = form.getAttribute("data-sending");
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function (res) {
          if (!res.ok) throw new Error("http " + res.status);
          form.reset();
          status.classList.add("ok");
          status.textContent = form.getAttribute("data-success");
        })
        .catch(function () {
          status.classList.add("err");
          status.textContent = form.getAttribute("data-error");
        })
        .then(function () { button.disabled = false; });
    });
  });

  /* ----- Barre de progression, en-tête, frise ----- */
  var bar = $(".scroll-progress"), timeline = $(".timeline"), ticking = false;
  var links = $$(".nav-links a, .mobile-menu a");
  var sections = $$("main section[id]");
  function onScroll() {
    ticking = false;
    var max = root.scrollHeight - window.innerHeight;
    if (bar) bar.style.transform = "scaleX(" + (max > 0 ? Math.min(window.scrollY / max, 1) : 0) + ")";
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 24);
    if (sections.length) {
      var current = "";
      for (var i = 0; i < sections.length; i++) {
        if (sections[i].getBoundingClientRect().top <= window.innerHeight * 0.4) current = sections[i].id;
      }
      links.forEach(function (a) {
        var on = current && a.getAttribute("href").split("#")[1] === current;
        if (on) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
      });
    }
    if (timeline) {
      var r = timeline.getBoundingClientRect();
      var p = (window.innerHeight * 0.55 - r.top) / r.height;
      timeline.style.setProperty("--progress", (Math.max(0, Math.min(1, p)) * 100).toFixed(2));
    }
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();

  /* ----- Révélations au scroll ----- */
  var reveals = $$(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.14, rootMargin: "0px 0px -6% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ----- Compteurs ----- */
  function countUp(el) {
    var target = parseInt(el.getAttribute("data-count"), 10) || 0;
    var suffix = el.getAttribute("data-suffix") || "";
    if (reduce) { el.textContent = target + suffix; return; }
    var start = null, dur = 1600;
    function step(ts) {
      if (start === null) start = ts;
      var t = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - t, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (t < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var counters = $$("[data-count]");
  if ("IntersectionObserver" in window && !reduce) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { countUp(e.target); cio.unobserve(e.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { el.textContent = "0" + (el.getAttribute("data-suffix") || ""); cio.observe(el); });
  } else {
    counters.forEach(countUp);
  }

  if (reduce) return;

  /* ----- Lumière qui suit le curseur sur les cartes ----- */
  doc.addEventListener("pointermove", function (e) {
    var card = e.target.closest && e.target.closest(".glass");
    if (!card) return;
    var r = card.getBoundingClientRect();
    card.style.setProperty("--mx", (e.clientX - r.left) + "px");
    card.style.setProperty("--my", (e.clientY - r.top) + "px");
  }, { passive: true });

  /* ----- Parallaxe douce de l'aurore ----- */
  var ambient = $(".ambient");
  if (ambient && window.matchMedia("(pointer: fine)").matches) {
    var raf = 0, tx = 0, ty = 0;
    doc.addEventListener("pointermove", function (e) {
      tx = (e.clientX / window.innerWidth - 0.5) * 36;
      ty = (e.clientY / window.innerHeight - 0.5) * 36;
      if (!raf) raf = requestAnimationFrame(function () {
        raf = 0;
        ambient.style.setProperty("--px", tx.toFixed(1) + "px");
        ambient.style.setProperty("--py", ty.toFixed(1) + "px");
      });
    }, { passive: true });
  }
})();
