let tempChart;

function renderTrendChart(labels, data) {
    const ctx = document.getElementById("tempTrendChart").getContext("2d");

    if (tempChart) {
        tempChart.destroy();
    }

    tempChart = new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [{
                label: "Temperature (°C)",
                data,
                tension: 0.35,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            },
            scales: {
                y: {
                    min: 35,
                    max: 42
                }
            }
        }
    });
}

function formatDateTime12(dateStr) {
    const date = new Date(dateStr);

    const fullDate = date.toLocaleDateString('en-IN', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    });

    const fullTime = date.toLocaleTimeString('en-IN', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
    });

    return `${fullDate}<br>${fullTime}`;
}

async function refreshDashboard() {
    try {
        const response = await fetch('/api/dashboard/summary');
        const data = await response.json();

        // Update cards
        document.getElementById("totalCattle").innerText = data.total_cattle;
        document.getElementById("healthyCount").innerText = data.healthy;
        document.getElementById("alertsCount").innerText = data.alerts;
        document.getElementById("atRiskCount").innerText = data.at_risk;
        // document.getElementById("lastSync").innerText = data.last_sync;
        document.getElementById("lastSync").innerHTML = formatDateTime12(data.last_sync);

        // Example: update alert list
        console.log(data);

    } catch (error) {
        console.error("Dashboard refresh failed:", error);
    }
}

// Run once when page loads
refreshDashboard();

// Auto refresh every 5 sec
setInterval(() => {
    refreshDashboard();
}, 5000);

document.addEventListener("DOMContentLoaded", () => {
    const initial = window.dashboardInitial;
    if (initial) {
        renderTrendChart(initial.trend.map(x => x.label), initial.trend.map(x => x.temp));
    }

    refreshDashboard();
    setInterval(refreshDashboard, 30000);
});