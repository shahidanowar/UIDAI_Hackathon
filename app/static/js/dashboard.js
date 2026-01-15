/**
 * Dashboard JavaScript
 * Handles India map, summary cards, and state drill-down
 */

// GeoJSON URL for India states
const GEOJSON_URL = 'https://raw.githubusercontent.com/geohacker/india/master/state/india_state.geojson';

let map;
let statesLayer;
let statesData = [];
let districtChart;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', async () => {
    await loadSummary();
    await loadStatesData();
    initMap();

    // Refresh button
    document.getElementById('refreshBtn')?.addEventListener('click', async () => {
        await loadSummary();
        await loadStatesData();
    });

    // Close panel button
    document.getElementById('closePanelBtn')?.addEventListener('click', () => {
        hideStatePanel();
    });
});

// Load summary data
async function loadSummary() {
    try {
        const response = await fetch('/api/dashboard/summary');
        const result = await response.json();

        if (result.success) {
            const data = result.data;

            document.getElementById('totalRecords').textContent = formatNumber(data.total_records);
            document.getElementById('totalAnomalies').textContent = formatNumber(data.total_anomalies);
            document.getElementById('anomalyRate').textContent = `${data.anomaly_rate}%`;
            document.getElementById('verifiedFixed').textContent = formatNumber(data.verified_fixed);
            document.getElementById('pendingVerification').textContent = formatNumber(data.pending_verification);
            document.getElementById('lastUpdated').textContent = new Date().toLocaleTimeString();

            // Progress bar
            const progressBar = document.getElementById('fixProgress');
            if (progressBar) {
                const progress = (data.verified_fixed / data.total_anomalies) * 100;
                progressBar.style.width = `${progress}%`;
            }

            // Most affected states
            renderAffectedStates(data.most_affected_states);
        }
    } catch (error) {
        console.error('Error loading summary:', error);
    }
}

// Load all states data
async function loadStatesData() {
    try {
        const response = await fetch('/api/dashboard/states');
        const result = await response.json();

        if (result.success) {
            statesData = result.data;
            updateMapColors();
        }
    } catch (error) {
        console.error('Error loading states:', error);
    }
}

// Initialize Leaflet map
function initMap() {
    map = L.map('indiaMap', {
        center: [22.5937, 78.9629],
        zoom: 5,
        minZoom: 4,
        maxZoom: 8,
        zoomControl: true,
        attributionControl: false
    });

    // Dark tile layer
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Load GeoJSON
    loadGeoJSON();
}

async function loadGeoJSON() {
    try {
        const response = await fetch(GEOJSON_URL);
        const geojson = await response.json();

        statesLayer = L.geoJSON(geojson, {
            style: getStateStyle,
            onEachFeature: onEachState
        }).addTo(map);

    } catch (error) {
        console.error('Error loading GeoJSON:', error);
    }
}

function getStateStyle(feature) {
    const stateName = feature.properties.NAME_1 || feature.properties.name;
    const stateData = statesData.find(s =>
        s.state.toLowerCase() === stateName?.toLowerCase()
    );

    let fillColor = '#3B82F6'; // Default blue

    if (stateData) {
        if (stateData.severity === 'high') fillColor = '#EF4444';
        else if (stateData.severity === 'medium') fillColor = '#F59E0B';
        else fillColor = '#10B981';
    }

    return {
        fillColor: fillColor,
        weight: 1,
        opacity: 0.8,
        color: '#475569',
        fillOpacity: 0.6
    };
}

function onEachState(feature, layer) {
    const stateName = feature.properties.NAME_1 || feature.properties.name;
    const stateData = statesData.find(s =>
        s.state.toLowerCase() === stateName?.toLowerCase()
    );

    // Tooltip
    let tooltipContent = `<div class="state-tooltip">
        <h4>${stateName || 'Unknown'}</h4>`;

    if (stateData) {
        tooltipContent += `
            <p>Records: ${formatNumber(stateData.total_records)}</p>
            <p>Anomalies: ${formatNumber(stateData.total_anomalies)}</p>
            <p>Rate: ${stateData.anomaly_rate}%</p>`;
    }

    tooltipContent += '</div>';

    layer.bindTooltip(tooltipContent, {
        sticky: true,
        className: 'state-tooltip-container'
    });

    // Events
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: (e) => selectState(stateName)
    });
}

function highlightFeature(e) {
    const layer = e.target;
    layer.setStyle({
        weight: 2,
        color: '#FF9933',
        fillOpacity: 0.8
    });
    layer.bringToFront();
}

function resetHighlight(e) {
    statesLayer.resetStyle(e.target);
}

function updateMapColors() {
    if (statesLayer) {
        statesLayer.setStyle(getStateStyle);
    }
}

// Select state and show details
async function selectState(stateName) {
    try {
        const response = await fetch(`/api/dashboard/state?state=${encodeURIComponent(stateName)}`);
        const result = await response.json();

        if (result.success) {
            showStatePanel(result.data);
        }
    } catch (error) {
        console.error('Error loading state data:', error);
    }
}

function showStatePanel(data) {
    document.getElementById('stateName').textContent = data.state;
    document.getElementById('panelContent').style.display = 'none';
    document.getElementById('stateStats').style.display = 'block';
    document.getElementById('closePanelBtn').style.display = 'block';

    document.getElementById('stateRecords').textContent = formatNumber(data.total_records);
    document.getElementById('stateAnomalies').textContent = formatNumber(data.total_anomalies);
    document.getElementById('stateAnomalyRate').textContent = `${data.anomaly_rate}%`;
    document.getElementById('stateInvalidPin').textContent = `${(data.invalid_pin_rate * 100).toFixed(1)}%`;
    document.getElementById('stateDuplicate').textContent = `${(data.duplicate_rate * 100).toFixed(1)}%`;

    // Anomaly list
    const anomalyList = document.getElementById('anomalyList');
    anomalyList.innerHTML = data.top_anomaly_types.map(a => `
        <div class="anomaly-item">
            <span class="anomaly-type">${a.type}</span>
            <span class="anomaly-count">${formatNumber(a.count)}</span>
        </div>
    `).join('');

    // District chart
    renderDistrictChart(data.district_distribution);
}

function hideStatePanel() {
    document.getElementById('stateName').textContent = 'Click a state to view details';
    document.getElementById('panelContent').style.display = 'block';
    document.getElementById('stateStats').style.display = 'none';
    document.getElementById('closePanelBtn').style.display = 'none';
}

function renderDistrictChart(districts) {
    const ctx = document.getElementById('districtChart')?.getContext('2d');
    if (!ctx) return;

    if (districtChart) districtChart.destroy();

    districtChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: districts.map(d => d.district),
            datasets: [{
                label: 'Records',
                data: districts.map(d => d.records),
                backgroundColor: 'rgba(255, 153, 51, 0.6)',
                borderColor: 'rgba(255, 153, 51, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { ticks: { color: '#94A3B8' }, grid: { color: '#334155' } },
                x: { ticks: { color: '#94A3B8' }, grid: { display: false } }
            }
        }
    });
}

function renderAffectedStates(states) {
    const container = document.getElementById('affectedStates');
    if (!container) return;

    container.innerHTML = states.map((s, i) => `
        <div class="affected-state-card" onclick="selectState('${s.state}')">
            <div class="state-rank">${i + 1}</div>
            <div class="state-info">
                <div class="state-name">${s.state}</div>
                <div class="state-anomaly-count">${formatNumber(s.anomaly_count)} anomalies</div>
            </div>
        </div>
    `).join('');
}

function formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num?.toLocaleString() || '--';
}
