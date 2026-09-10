window.MathJax = {
  tex: {
    inlineMath: [
      ["\\(", "\\)"],
      ["$", "$"],
    ],
    displayMath: [
      ["\\[", "\\]"],
      ["$$", "$$"],
    ],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
  },
};

let mathJaxLoadPromise;

function loadMathJax() {
  if (window.MathJax.typesetPromise) {
    return Promise.resolve(window.MathJax);
  }

  if (!mathJaxLoadPromise) {
    mathJaxLoadPromise = new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = "https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js";
      script.async = true;
      script.onload = () => resolve(window.MathJax);
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  return mathJaxLoadPromise;
}

function typesetMath() {
  if (!document.querySelector(".arithmatex")) {
    return;
  }

  loadMathJax()
    .then(() => {
      window.MathJax.startup.output.clearCache();
      window.MathJax.typesetClear();
      window.MathJax.texReset();
      return window.MathJax.typesetPromise();
    })
    .catch((error) => console.error("MathJax failed to load", error));
}

document$.subscribe(typesetMath);
