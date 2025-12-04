/**
 * Wiki Search Functionality
 * Provides real-time filtering of wiki terms as user types
 */

(function () {
    'use strict';

    const STORAGE_KEY = 'wiki-search-query';

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function () {
        const searchInput = document.getElementById('wiki-search-input');
        const clearButton = document.getElementById('wiki-search-clear');
        const wikiList = document.querySelector('.wiki-list');
        const resultCount = document.getElementById('wiki-search-count');

        if (!searchInput || !wikiList) {
            return; // Not on wiki page
        }

        // Load saved search query
        loadSearchQuery();

        // Add event listeners
        searchInput.addEventListener('input', handleSearch);
        searchInput.addEventListener('keyup', function (e) {
            if (e.key === 'Escape') {
                clearSearch();
            }
        });

        if (clearButton) {
            clearButton.addEventListener('click', clearSearch);
        }

        // Perform initial search if there's a saved query
        if (searchInput.value) {
            handleSearch();
        }
    });

    /**
     * Handle search input
     */
    function handleSearch() {
        const searchInput = document.getElementById('wiki-search-input');
        const clearButton = document.getElementById('wiki-search-clear');
        const wikiList = document.querySelector('.wiki-list');
        const resultCount = document.getElementById('wiki-search-count');

        if (!searchInput || !wikiList) {
            return;
        }

        const query = searchInput.value.toLowerCase().trim();
        const items = wikiList.querySelectorAll('li');
        let visibleCount = 0;

        // Show/hide clear button
        if (clearButton) {
            clearButton.style.display = query ? 'inline-block' : 'none';
        }

        // Filter items
        items.forEach(function (item) {
            const title = (item.dataset.title || '').toLowerCase();
            const description = (item.querySelector('p')?.textContent || '').toLowerCase();
            const matches = title.includes(query) || description.includes(query);

            if (matches || !query) {
                item.style.display = '';
                visibleCount++;
            } else {
                item.style.display = 'none';
            }
        });

        // Update result count
        if (resultCount) {
            if (query) {
                resultCount.textContent = `Showing ${visibleCount} of ${items.length} terms`;
                resultCount.style.display = 'block';
            } else {
                resultCount.style.display = 'none';
            }
        }

        // Save search query
        saveSearchQuery(query);
    }

    /**
     * Clear search
     */
    function clearSearch() {
        const searchInput = document.getElementById('wiki-search-input');
        const clearButton = document.getElementById('wiki-search-clear');
        const wikiList = document.querySelector('.wiki-list');
        const resultCount = document.getElementById('wiki-search-count');

        if (searchInput) {
            searchInput.value = '';
            searchInput.focus();
        }

        if (clearButton) {
            clearButton.style.display = 'none';
        }

        if (wikiList) {
            const items = wikiList.querySelectorAll('li');
            items.forEach(function (item) {
                item.style.display = '';
            });
        }

        if (resultCount) {
            resultCount.style.display = 'none';
        }

        saveSearchQuery('');
    }

    /**
     * Save search query to localStorage
     */
    function saveSearchQuery(query) {
        try {
            if (query) {
                localStorage.setItem(STORAGE_KEY, query);
            } else {
                localStorage.removeItem(STORAGE_KEY);
            }
        } catch (e) {
            console.warn('Could not save wiki search query:', e);
        }
    }

    /**
     * Load search query from localStorage
     */
    function loadSearchQuery() {
        const searchInput = document.getElementById('wiki-search-input');

        if (!searchInput) {
            return;
        }

        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            if (saved) {
                searchInput.value = saved;
            }
        } catch (e) {
            console.warn('Could not load wiki search query:', e);
        }
    }
})();
