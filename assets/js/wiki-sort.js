/**
 * Wiki List Sorting Functionality
 * Provides client-side sorting for wiki terms by title, date added, or last modified
 */

(function () {
  "use strict";

  const STORAGE_KEY = "wiki-sort-preferences";

  // Initialize sorting when DOM is ready
  document.addEventListener("DOMContentLoaded", function () {
    const wikiList = document.querySelector(".wiki-list");
    const criteriaSelect = document.getElementById("wiki-sort-criteria");
    const orderSelect = document.getElementById("wiki-sort-order");

    if (!wikiList || !criteriaSelect || !orderSelect) {
      return; // Not on wiki page or controls not found
    }

    // Load saved preferences
    loadSortPreference();

    // Add event listeners
    criteriaSelect.addEventListener("change", handleSortChange);
    orderSelect.addEventListener("change", handleSortChange);

    // Apply initial sort
    sortWikiList();
  });

  /**
   * Handle sort control changes
   */
  function handleSortChange() {
    sortWikiList();
    saveSortPreference();
  }

  /**
   * Sort the wiki list based on current criteria and order
   */
  function sortWikiList() {
    const wikiList = document.querySelector(".wiki-list");
    const criteriaSelect = document.getElementById("wiki-sort-criteria");
    const orderSelect = document.getElementById("wiki-sort-order");

    if (!wikiList || !criteriaSelect || !orderSelect) {
      return;
    }

    const criteria = criteriaSelect.value;
    const order = orderSelect.value;

    // Get all list items
    const items = Array.from(wikiList.querySelectorAll("li"));

    // Sort items
    items.sort(function (a, b) {
      let aValue, bValue;

      switch (criteria) {
        case "title":
          aValue = a.dataset.title || "";
          bValue = b.dataset.title || "";
          return compareStrings(aValue, bValue, order);

        case "date":
          aValue = a.dataset.date || "1970-01-01";
          bValue = b.dataset.date || "1970-01-01";
          return compareDates(aValue, bValue, order);

        case "lastmod":
          aValue = a.dataset.lastmod || "1970-01-01";
          bValue = b.dataset.lastmod || "1970-01-01";
          return compareDates(aValue, bValue, order);

        default:
          return 0;
      }
    });

    // Re-append items in sorted order
    items.forEach(function (item) {
      wikiList.appendChild(item);
    });
  }

  /**
   * Compare two strings for sorting
   */
  function compareStrings(a, b, order) {
    const comparison = a.localeCompare(b, undefined, { sensitivity: "base" });
    return order === "asc" ? comparison : -comparison;
  }

  /**
   * Compare two date strings for sorting
   */
  function compareDates(a, b, order) {
    const dateA = new Date(a);
    const dateB = new Date(b);
    const comparison = dateA - dateB;
    return order === "asc" ? comparison : -comparison;
  }

  /**
   * Save sort preferences to localStorage
   */
  function saveSortPreference() {
    const criteriaSelect = document.getElementById("wiki-sort-criteria");
    const orderSelect = document.getElementById("wiki-sort-order");

    if (!criteriaSelect || !orderSelect) {
      return;
    }

    const preferences = {
      criteria: criteriaSelect.value,
      order: orderSelect.value,
    };

    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(preferences));
    } catch (e) {
      // localStorage might be disabled
      console.warn("Could not save wiki sort preferences:", e);
    }
  }

  /**
   * Load sort preferences from localStorage
   */
  function loadSortPreference() {
    const criteriaSelect = document.getElementById("wiki-sort-criteria");
    const orderSelect = document.getElementById("wiki-sort-order");

    if (!criteriaSelect || !orderSelect) {
      return;
    }

    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const preferences = JSON.parse(saved);
        if (preferences.criteria) {
          criteriaSelect.value = preferences.criteria;
        }
        if (preferences.order) {
          orderSelect.value = preferences.order;
        }
      }
    } catch (e) {
      // localStorage might be disabled or data corrupted
      console.warn("Could not load wiki sort preferences:", e);
    }
  }
})();
