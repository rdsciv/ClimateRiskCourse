(function () {
  const path = location.pathname.replace(/\/$/, "") || "/";
  document.querySelectorAll(".nav-links a[data-nav]").forEach((a) => {
    const key = a.getAttribute("data-nav");
    if (!key) return;
    if (path.endsWith(key) || (key === "index.html" && (path.endsWith("/docs") || path.endsWith("/")))) {
      a.classList.add("active");
    }
  });
})();
