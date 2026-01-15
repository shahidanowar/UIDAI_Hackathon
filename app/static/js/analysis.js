/**
 * Analysis JavaScript
 * Handles charts and data visualization
 */

let anomalyChart, ageChart, genderChart, stateAnomalyChart;

document.addEventListener('DOMContentLoaded', async () => {
    await loadAnalysisReport();
});

async function loadAnalysisReport() {
    try {
        const response = await fetch('/analysis/api/report');
        const result = await response.json();

        if (result.success) {
            const data = result.data;

            // Header stats
            document.getElementById('totalAnalyzed').textContent = formatNumber(data.total_records_analyzed);
            document.getElementById('analysisDate').textContent = new Date(data.analysis_date).toLocaleDateString();

            // Render charts
            renderAnomalyChart(data.anomaly_frequency);
            renderAgeChart(data.age_distribution);
            renderGenderChart(data.gender_distribution);
            renderStateAnomalyChart(data.state_anomaly_distribution);

            // Render lists
            renderWarnings(data.correlation_warnings);
            renderPatterns(data.suspicious_patterns);
            renderAnomalyTypes(data.anomaly_frequency);
        }
    } catch (error) {
        console.error('Error loading analysis report:', error);
    }
}

function renderAnomalyChart(data) {
    const ctx = document.getElementById('anomalyChart')?.getContext('2d');
    if (!ctx) return;

    if (anomalyChart) anomalyChart.destroy();

    anomalyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.slice(0, 8).map(d => d.type),
            datasets: [{
                label: 'Count',
                data: data.slice(0, 8).map(d => d.count),
                backgroundColor: [
                    'rgba(239, 68, 68, 0.7)', 'rgba(234, 88, 12, 0.7)',
                    'rgba(245, 158, 11, 0.7)', 'rgba(217, 119, 6, 0.7)',
                    'rgba(101, 163, 13, 0.7)', 'rgba(16, 185, 129, 0.7)',
                    'rgba(59, 130, 246, 0.7)', 'rgba(139, 92, 246, 0.7)'
                ],
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: '#94A3B8' }, grid: { color: '#334155' } },
                y: { ticks: { color: '#94A3B8' }, grid: { display: false } }
            }
        }
    });
}

function renderAgeChart(data) {
    const ctx = document.getElementById('ageChart')?.getContext('2d');
    if (!ctx) return;

    if (ageChart) ageChart.destroy();

    ageChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: 'Population',
                data: Object.values(data),
                backgroundColor: 'rgba(255, 153, 51, 0.7)',
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { ticks: { color: '#94A3B8', callback: v => formatNumber(v) }, grid: { color: '#334155' } },
                x: { ticks: { color: '#94A3B8' }, grid: { display: false } }
            }
        }
    });
}

function renderGenderChart(data) {
    const ctx = document.getElementById('genderChart')?.getContext('2d');
    if (!ctx) return;

    if (genderChart) genderChart.destroy();

    genderChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data),
                backgroundColor: ['#3B82F6', '#EC4899', '#8B5CF6', '#6B7280']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#94A3B8' } }
            }
        }
    });
}

function renderStateAnomalyChart(data) {
    const ctx = document.getElementById('stateAnomalyChart')?.getContext('2d');
    if (!ctx) return;

    if (stateAnomalyChart) stateAnomalyChart.destroy();

    stateAnomalyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.state),
            datasets: [{
                label: 'Anomalies',
                data: data.map(d => d.anomalies),
                backgroundColor: 'rgba(239, 68, 68, 0.7)',
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { ticks: { color: '#94A3B8', callback: v => formatNumber(v) }, grid: { color: '#334155' } },
                x: { ticks: { color: '#94A3B8' }, grid: { display: false } }
            }
        }
    });
}

function renderWarnings(warnings) {
    const container = document.getElementById('warningsList');
    if (!container) return;

    container.innerHTML = warnings.map(w => `
        <div class="warning-item ${w.severity}">
            <svg class="warning-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
            </svg>
            <div class="warning-content">
                <p class="warning-text">${w.warning}</p>
                <span class="warning-correlation">Correlation: ${(w.correlation * 100).toFixed(0)}%</span>
            </div>
        </div>
    `).join('');
}

function renderPatterns(patterns) {
    const container = document.getElementById('patternsList');
    if (!container) return;

    container.innerHTML = patterns.map(p => `
        <div class="pattern-item">
            <div class="pattern-header">
                <span class="pattern-risk ${p.risk_level}">${p.risk_level}</span>
            </div>
            <p class="pattern-text">${p.pattern}</p>
            <p class="pattern-affected">Affected records: <span>${formatNumber(p.affected_records)}</span></p>
        </div>
    `).join('');
}

function renderAnomalyTypes(anomalies) {
    const container = document.getElementById('anomalyTypes');
    if (!container) return;

    const icons = ['⚠️', '📍', '📅', '📱', '👤', '🗺️', '🔄', '🔍', '📝', '❓'];

    container.innerHTML = anomalies.map((a, i) => `
        <div class="anomaly-type-card">
            <div class="anomaly-type-icon">${icons[i % icons.length]}</div>
            <div class="anomaly-type-info">
                <div class="anomaly-type-name">${a.type}</div>
                <div class="anomaly-type-count"><span>${formatNumber(a.count)}</span> cases detected</div>
            </div>
        </div>
    `).join('');
}

function formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num?.toLocaleString() || '--';
}
