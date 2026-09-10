let tablesortLoadPromise;

function loadTablesort() {
  if (window.Tablesort) {
    return Promise.resolve(window.Tablesort);
  }

  if (!tablesortLoadPromise) {
    tablesortLoadPromise = new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = "https://unpkg.com/tablesort@5.3.0/dist/tablesort.min.js";
      script.async = true;
      script.onload = () => resolve(window.Tablesort);
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  return tablesortLoadPromise;
}

function initTablesort() {
  const tables = Array.from(document.querySelectorAll("article table:not([class])")).filter((table) => !table.dataset.tablesortInitialized);

  if (!tables.length) {
    return;
  }

  loadTablesort()
    .then(() => {
      tables.forEach((table) => {
        new window.Tablesort(table);
        table.dataset.tablesortInitialized = "true";
      });
    })
    .catch((error) => console.error("Tablesort failed to load", error));
}

document$.subscribe(initTablesort);
