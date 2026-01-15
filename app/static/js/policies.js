/**
 * Policies JavaScript
 * Handles policy cards and modal
 */

let currentPolicies = [];
let currentPolicy = null;

document.addEventListener('DOMContentLoaded', async () => {
    await loadPolicies();

    document.getElementById('severityFilter')?.addEventListener('change', filterPolicies);
    document.getElementById('closeModal')?.addEventListener('click', closeModal);
    document.getElementById('closeModalBtn')?.addEventListener('click', closeModal);
    document.getElementById('createTaskBtn')?.addEventListener('click', createTask);
});

async function loadPolicies() {
    const loadingState = document.getElementById('loadingState');
    const policiesGrid = document.getElementById('policiesGrid');
    const emptyState = document.getElementById('emptyState');

    loadingState.style.display = 'flex';
    policiesGrid.innerHTML = '';

    try {
        const response = await fetch('/policies/api/recommendations');
        const result = await response.json();

        if (result.success) {
            currentPolicies = result.data.recommendations;
            renderPolicies(currentPolicies);
            updateStats(currentPolicies);
        }
    } catch (error) {
        console.error('Error loading policies:', error);
    } finally {
        loadingState.style.display = 'none';
    }
}

function filterPolicies() {
    const severity = document.getElementById('severityFilter').value;
    const filtered = severity
        ? currentPolicies.filter(p => p.severity === severity)
        : currentPolicies;
    renderPolicies(filtered);
}

function renderPolicies(policies) {
    const grid = document.getElementById('policiesGrid');
    const emptyState = document.getElementById('emptyState');

    if (policies.length === 0) {
        grid.innerHTML = '';
        emptyState.style.display = 'flex';
        return;
    }

    emptyState.style.display = 'none';

    grid.innerHTML = policies.map(p => `
        <div class="policy-card ${p.severity}" onclick="openPolicy(${p.id})">
            <div class="policy-header">
                <h3 class="policy-title">${p.title}</h3>
                <span class="severity-badge ${p.severity}">${p.severity}</span>
            </div>
            <p class="policy-reason">${p.reason}</p>
            <div class="policy-meta">
                <span><strong>Executor:</strong> ${p.executor}</span>
                <span><strong>Impact:</strong> ${formatNumber(p.estimated_impact)} records</span>
            </div>
        </div>
    `).join('');
}

function updateStats(policies) {
    document.getElementById('totalPolicies').textContent = policies.length;
    document.getElementById('criticalCount').textContent = policies.filter(p => p.severity === 'critical').length;
    document.getElementById('highCount').textContent = policies.filter(p => p.severity === 'high').length;
    document.getElementById('mediumCount').textContent = policies.filter(p => p.severity === 'medium').length;
}

function openPolicy(id) {
    currentPolicy = currentPolicies.find(p => p.id === id);
    if (!currentPolicy) return;

    document.getElementById('modalTitle').textContent = currentPolicy.title;
    document.getElementById('modalBody').innerHTML = `
        <div class="policy-detail-section">
            <h4>Reason</h4>
            <p>${currentPolicy.reason}</p>
        </div>
        <div class="policy-detail-section">
            <h4>Implementation Steps</h4>
            <ol class="steps-list">
                ${currentPolicy.steps.map(s => `<li>${s}</li>`).join('')}
            </ol>
        </div>
        <div class="policy-detail-section">
            <h4>Details</h4>
            <p><strong>Executor:</strong> ${currentPolicy.executor}</p>
            <p><strong>Expected Outcome:</strong> ${currentPolicy.expected_outcome}</p>
            <p><strong>Estimated Impact:</strong> ${formatNumber(currentPolicy.estimated_impact)} records</p>
        </div>
    `;

    document.getElementById('policyModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('policyModal').style.display = 'none';
    currentPolicy = null;
}

function createTask() {
    if (currentPolicy) {
        window.location.href = `/todo?title=${encodeURIComponent('Implement: ' + currentPolicy.title)}&description=${encodeURIComponent(currentPolicy.reason)}`;
    }
    closeModal();
}

function formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num?.toLocaleString() || '--';
}
