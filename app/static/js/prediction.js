/**
 * Prediction JavaScript
 * Handles form submission and results display
 */

const EXAMPLES = {
    low: { state: 'Kerala', records: 50000, anomalies: 800, invalid_pin_rate: 0.02, duplicate_rate: 0.01, missing_dob_rate: 0.01 },
    medium: { state: 'Maharashtra', records: 120000, anomalies: 6000, invalid_pin_rate: 0.08, duplicate_rate: 0.04, missing_dob_rate: 0.03 },
    high: { state: 'Bihar', records: 80000, anomalies: 12000, invalid_pin_rate: 0.18, duplicate_rate: 0.12, missing_dob_rate: 0.08 }
};

document.addEventListener('DOMContentLoaded', async () => {
    await loadStates();

    document.getElementById('predictionForm')?.addEventListener('submit', handleSubmit);

    document.querySelectorAll('.example-btn').forEach(btn => {
        btn.addEventListener('click', () => fillExample(btn.dataset.example));
    });
});

async function loadStates() {
    try {
        const response = await fetch('/prediction/api/states');
        const result = await response.json();

        if (result.success) {
            const select = document.getElementById('state');
            result.data.forEach(state => {
                const option = document.createElement('option');
                option.value = state;
                option.textContent = state;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading states:', error);
    }
}

function fillExample(type) {
    const data = EXAMPLES[type];
    if (!data) return;

    document.getElementById('state').value = data.state;
    document.getElementById('records').value = data.records;
    document.getElementById('anomalies').value = data.anomalies;
    document.getElementById('invalid_pin_rate').value = data.invalid_pin_rate;
    document.getElementById('duplicate_rate').value = data.duplicate_rate;
    document.getElementById('missing_dob_rate').value = data.missing_dob_rate;
}

async function handleSubmit(e) {
    e.preventDefault();

    const btn = document.getElementById('predictBtn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner" style="width:18px;height:18px;border-width:2px;"></span> Predicting...';

    const formData = {
        state: document.getElementById('state').value,
        records: parseInt(document.getElementById('records').value),
        anomalies: parseInt(document.getElementById('anomalies').value),
        invalid_pin_rate: parseFloat(document.getElementById('invalid_pin_rate').value) || 0,
        duplicate_rate: parseFloat(document.getElementById('duplicate_rate').value) || 0,
        missing_dob_rate: parseFloat(document.getElementById('missing_dob_rate').value) || 0
    };

    try {
        const response = await fetch('/prediction/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (result.success) {
            displayResults(result.data);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to get prediction');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5"/></svg> Run Prediction';
    }
}

function displayResults(data) {
    document.getElementById('resultsPlaceholder').style.display = 'none';
    document.getElementById('resultsContent').style.display = 'block';

    // Update gauge
    const score = data.score;
    const gaugeFill = document.getElementById('gaugeFill');
    const gaugeScore = document.getElementById('gaugeScore');

    const dashoffset = 283 - (283 * score);
    gaugeFill.style.strokeDashoffset = dashoffset;
    gaugeScore.textContent = (score * 100).toFixed(0);

    // Set color class
    gaugeFill.classList.remove('low', 'medium', 'high');
    if (score < 0.4) gaugeFill.classList.add('low');
    else if (score < 0.7) gaugeFill.classList.add('medium');
    else gaugeFill.classList.add('high');

    // Result badge
    const badge = document.getElementById('resultBadge');
    badge.textContent = data.prediction;
    badge.classList.remove('low', 'medium', 'high');
    if (data.prediction.includes('Low')) badge.classList.add('low');
    else if (data.prediction.includes('Medium')) badge.classList.add('medium');
    else badge.classList.add('high');

    // Confidence
    document.getElementById('confidenceScore').textContent = `${(data.confidence * 100).toFixed(0)}%`;

    // Action
    document.getElementById('recommendedAction').textContent = data.recommended_action;

    // Features
    const featuresList = document.getElementById('featuresList');
    featuresList.innerHTML = data.top_features.map(f => `
        <div class="feature-item">
            <span class="feature-name">${f.feature}</span>
            <span class="feature-value">${f.value || f.contribution + '%'}</span>
        </div>
    `).join('');
}
