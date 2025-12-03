# APP Prediksi

Django-based application for screening and prediction analysis.

## Fitur Utama

- User authentication (login, register)
- Screening form submission
- Machine learning model for predictions
- Admin dashboard
- Result tracking

## Struktur Project

```
webdjango/
├── screening/          # Main application
│   ├── migrations/     # Database migrations
│   ├── ml_models/      # ML models and data
│   ├── static/         # CSS, JS files
│   ├── templates/      # HTML templates
│   ├── models.py       # Database models
│   ├── views.py        # View functions
│   ├── urls.py         # URL routing
│   └── admin.py        # Django admin configuration
├── website/            # Project settings
│   ├── settings.py     # Django settings
│   ├── urls.py         # Main URL configuration
│   └── wsgi.py         # WSGI configuration
├── manage.py           # Django management script
└── db.sqlite3          # SQLite database
```

## Setup Instructions

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd webdjango
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

Access the application at `http://localhost:8000`

## Technology Stack

- **Backend**: Django
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **ML**: scikit-learn (Random Forest model)

## Database Models

- ScreeningSubmission: User screening submissions
- BloodPressure: Blood pressure measurements
- Additional health indicators

## License

MIT License
