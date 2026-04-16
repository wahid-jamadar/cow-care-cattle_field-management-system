document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const toggle = document.getElementById("sidebarToggle");

    if (toggle && sidebar) {
        toggle.addEventListener("click", () => sidebar.classList.toggle("show"));
    }

    const searchInput = document.getElementById("searchInput");
    if (searchInput) {
        searchInput.addEventListener("input", () => {
            const query = searchInput.value.toLowerCase();
            document.querySelectorAll(".search-table tbody tr").forEach(row => {
                row.style.display = row.innerText.toLowerCase().includes(query) ? "" : "none";
            });
        });
    }
});