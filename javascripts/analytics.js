const cloudflareAnalytics = document.createElement("script");

cloudflareAnalytics.type = "module";
cloudflareAnalytics.src = "https://static.cloudflareinsights.com/beacon.min.js";
cloudflareAnalytics.dataset.cfBeacon = JSON.stringify({
  token: "87ea21549503443193aafe1fcfc43b93",
});

document.head.appendChild(cloudflareAnalytics);
