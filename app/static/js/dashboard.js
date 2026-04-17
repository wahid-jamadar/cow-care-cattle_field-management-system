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
        await fetch("/api/health-data/simulate", { method: "POST" });

        const res = await fetch("/api/dashboard/summary");
        const data = await res.json();

        document.getElementById("totalCattle").textContent = data.total_cattle;
        document.getElementById("attachedDevices").textContent = data.attached_devices;
        document.getElementById("healthyCount").textContent = data.healthy;
        document.getElementById("alertsCount").textContent = data.alerts;
        document.getElementById("atRiskCount").textContent = data.at_risk;
        document.getElementById("lastSync").innerHTML = formatDateTime12(data.last_sync);

        const labels = data.trend.map(x => x.label);
        const temps = data.trend.map(x => x.temp);
        renderTrendChart(labels, temps);

        const alertsBox = document.getElementById("latestAlerts");
        alertsBox.innerHTML = "";
        data.alerts_list.forEach(a => {
            const div = document.createElement("div");
            div.className = `alert-item severity-${a.severity.toLowerCase()}`;
            div.innerHTML = `
                <div class="fw-semibold">${a.message}</div>
                <small class="text-muted">Cattle #${a.cattle_id} · ${new Date(a.timestamp).toLocaleString()}</small>
            `;
            alertsBox.appendChild(div);
        });
    } catch (error) {
        console.error("Dashboard refresh failed:", error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const initial = window.dashboardInitial;
    if (initial) {
        renderTrendChart(initial.trend.map(x => x.label), initial.trend.map(x => x.temp));
    }

    refreshDashboard();
    setInterval(refreshDashboard, 30000);
});