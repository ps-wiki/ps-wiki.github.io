/**
 * Library Search Functionality
 * Provides quick search access to academic databases
 */

(function () {
  "use strict";

  const SEARCH_ENGINES = {
    "google-scholar": {
      name: "Google Scholar",
      url: "https://scholar.google.com/scholar?q=",
      icon: "fas fa-graduation-cap",
    },
    ieee: {
      name: "IEEE Xplore",
      url: "https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=",
      icon: "fas fa-bolt",
    },
    arxiv: {
      name: "arXiv",
      url: "https://arxiv.org/search/?query=",
      icon: "fas fa-file-alt",
    },
    sciencedirect: {
      name: "ScienceDirect",
      url: "https://www.sciencedirect.com/search?qs=",
      icon: "fas fa-flask",
    },
    pubmed: {
      name: "PubMed",
      url: "https://pubmed.ncbi.nlm.nih.gov/?term=",
      icon: "fas fa-heartbeat",
    },
  };

  // Initialize when DOM is ready
  document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById("library-search-form");
    const searchInput = document.getElementById("library-search-input");
    const engineSelect = document.getElementById("library-search-engine");

    if (!searchForm || !searchInput || !engineSelect) {
      return; // Not on a page with library search
    }

    // Handle form submission
    searchForm.addEventListener("submit", function (e) {
      e.preventDefault();
      performSearch();
    });

    // Handle Enter key in input
    searchInput.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        performSearch();
      }
    });
  });

  /**
   * Perform search in selected library
   */
  function performSearch() {
    const searchInput = document.getElementById("library-search-input");
    const engineSelect = document.getElementById("library-search-engine");

    if (!searchInput || !engineSelect) {
      return;
    }

    const query = searchInput.value.trim();
    const engine = engineSelect.value;

    if (!query) {
      searchInput.focus();
      return;
    }

    const searchEngine = SEARCH_ENGINES[engine];
    if (!searchEngine) {
      console.error("Unknown search engine:", engine);
      return;
    }

    // Encode the query and open in new tab
    const encodedQuery = encodeURIComponent(query);
    const searchUrl = searchEngine.url + encodedQuery;
    window.open(searchUrl, "_blank", "noopener,noreferrer");
  }
})();
