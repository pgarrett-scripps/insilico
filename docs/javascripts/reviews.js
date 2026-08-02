/* Filter and sort the review index.
 *
 * Progressive enhancement: the toolbar is built here rather than emitted by
 * build_index.py, so a reader without JavaScript sees the full list of
 * reviews with no dead controls above it. Everything works off the cards'
 * own data attributes — there is no second copy of the corpus to fetch, and
 * therefore no way for the list and the filters to disagree.
 */
(function () {
  "use strict";

  // Ordered worst-to-best deliberately: a reader scanning verdicts is usually
  // looking for the critical ones, and "Accept" leading the row implies a
  // ranking of quality that these buttons are not.
  var VERDICTS = [
    { key: "reject", label: "Reject" },
    { key: "major", label: "Major revision" },
    { key: "minor", label: "Minor revision" },
    { key: "accept", label: "Accept" },
    { key: "desk", label: "Desk reject" },
  ];

  var SORTS = [
    { key: "newest", label: "Newest" },
    { key: "oldest", label: "Oldest" },
    { key: "score-desc", label: "Highest score" },
    { key: "score-asc", label: "Lowest score" },
    { key: "title", label: "Title A–Z" },
  ];

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function scoreOf(card) {
    var raw = card.getAttribute("data-score");
    return raw === "" || raw == null ? null : parseFloat(raw);
  }

  function init(grid) {
    var cards = Array.prototype.slice.call(grid.querySelectorAll(".ins-card"));
    // One card is not a corpus; controls would be noise.
    if (cards.length < 2) return;

    var present = {};
    cards.forEach(function (c) {
      present[c.getAttribute("data-verdict")] = true;
    });

    var bar = el("div", "ins-filters");
    var active = "all";

    var chips = [{ key: "all", label: "All", count: cards.length }];
    VERDICTS.forEach(function (v) {
      if (!present[v.key]) return; // never offer a filter that yields nothing
      var n = cards.filter(function (c) {
        return c.getAttribute("data-verdict") === v.key;
      }).length;
      chips.push({ key: v.key, label: v.label, count: n });
    });

    // A single verdict across the whole corpus makes filtering meaningless,
    // but sorting is still useful — so fall through to the sort control.
    var buttons = [];
    if (chips.length > 2) {
      chips.forEach(function (c) {
        var b = el("button", "ins-filter", c.label);
        b.type = "button";
        b.setAttribute("data-key", c.key);
        b.setAttribute("aria-pressed", c.key === "all" ? "true" : "false");
        b.appendChild(el("span", "ins-filter__count", c.count));
        if (c.key !== "all") b.classList.add("ins-filter--" + c.key);
        b.addEventListener("click", function () {
          active = c.key;
          buttons.forEach(function (other) {
            other.setAttribute(
              "aria-pressed",
              other === b ? "true" : "false"
            );
          });
          apply();
        });
        buttons.push(b);
        bar.appendChild(b);
      });
    }

    var sortWrap = el("label", "ins-sort");
    sortWrap.appendChild(el("span", "ins-sort__label", "Sort"));
    var select = el("select", "ins-sort__select");
    SORTS.forEach(function (s) {
      var o = document.createElement("option");
      o.value = s.key;
      o.textContent = s.label;
      select.appendChild(o);
    });
    select.addEventListener("change", apply);
    sortWrap.appendChild(select);
    bar.appendChild(sortWrap);

    // No empty state: chips are generated only for verdicts that are actually
    // present, so no selection can return zero cards.
    function apply() {
      cards.forEach(function (c) {
        c.hidden =
          !(active === "all" || c.getAttribute("data-verdict") === active);
      });

      var mode = select.value;
      var order = cards.slice().sort(function (a, b) {
        if (mode === "title") {
          return (a.getAttribute("data-title") || "").localeCompare(
            b.getAttribute("data-title") || ""
          );
        }
        if (mode === "score-desc" || mode === "score-asc") {
          var sa = scoreOf(a);
          var sb = scoreOf(b);
          // Unscored reviews (desk rejects) sort last either way rather than
          // pretending to a score of zero.
          if (sa === null && sb === null) return 0;
          if (sa === null) return 1;
          if (sb === null) return -1;
          return mode === "score-desc" ? sb - sa : sa - sb;
        }
        var da = a.getAttribute("data-date") || "";
        var db = b.getAttribute("data-date") || "";
        return mode === "oldest" ? da.localeCompare(db) : db.localeCompare(da);
      });
      order.forEach(function (c) {
        grid.appendChild(c);
      });
    }

    grid.parentNode.insertBefore(bar, grid);
    apply();
  }

  function boot() {
    document.querySelectorAll(".ins-cards").forEach(init);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
