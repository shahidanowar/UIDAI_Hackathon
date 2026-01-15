# UIDAI Aadhaar Data Intelligence Dashboard

A Flask-based web dashboard for exploring and validating Aadhaar-related records. Built for the UIDAI Hackathon.

## Features

- 📊 **Dashboard** - India map with state-level drilldown, summary cards
- 📈 **Analysis** - Anomaly detection, correlation warnings, distribution charts
- 🎯 **Prediction** - ML-powered risk assessment with confidence scores
- 🛡️ **Policies** - Data-driven recommendations for anomaly resolution
- ✅ **To-Do** - Task management for verification workflows

## Quick Start

```bash
# Navigate to project
cd aadhaar-dashboard

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

Open http://localhost:5000 in your browser.

## Project Structure

```
aadhaar-dashboard/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py             # Configuration
│   ├── extensions.py         # Flask extensions
│   ├── models.py             # Database models
│   ├── routes/               # Blueprints
│   │   ├── dashboard.py
│   │   ├── analysis.py
│   │   ├── prediction.py
│   │   ├── policies.py
│   │   └── todo.py
│   ├── services/             # Business logic
│   │   ├── mock_data.py
│   │   └── analytics_service.py
│   ├── ml/                   # ML models
│   │   └── model.py
│   ├── templates/            # Jinja templates
│   └── static/               # CSS, JS
├── instance/                 # SQLite database
├── run.py
├── requirements.txt
└── README.md
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dashboard/summary` | GET | Dashboard statistics |
| `/api/dashboard/state?state=<name>` | GET | State-specific data |
| `/analysis/api/report` | GET | Full analysis report |
| `/prediction/api/predict` | POST | ML risk prediction |
| `/policies/api/recommendations` | GET | Policy recommendations |
| `/todo/api/tasks` | GET/POST | Task management |
| `/todo/api/tasks/<id>` | PATCH/DELETE | Update/delete task |

## Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **Charts**: Chart.js
- **Maps**: Leaflet.js + GeoJSON
- **ML**: scikit-learn (with rule-based fallback)
- **Database**: SQLite (PostgreSQL ready)

## Screenshot Preview

The dashboard features:
- Dark theme with Indian government color palette
- Interactive India map with state hover/click
- Real-time summary cards
- Responsive design

## License

Built for UIDAI Hackathon - Prototype Demo
