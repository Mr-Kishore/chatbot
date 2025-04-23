chatbot_app/
│
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── auth.py       # Login/Logout endpoints
│   │   ├── employee.py   # Employee chatbot routes
│   │   └── admin.py      # Admin-only endpoints
│   ├── models/
│   │   └── db.py         # SQLite database models & setup
│   ├── services/
│   │   ├── auth_service.py
│   │   └── nlp_service.py
│   └── config.py         # Config vars
│
├── run.py                # Flask app runner
└── requirements.txt
