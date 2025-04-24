chatbot_app/
├── app/
│   ├── __init__.py         # Sets up Flask app
│   ├── config.py           # Secret keys, session config
│   ├── models/
│   │   └── db.py           # SQLite DB for users & employee data
│   ├── routes/
│   │   ├── auth.py         # Login/logout (session-based)
│   │   ├── employee.py     # Chat endpoint for employees
│   │   └── admin.py        # Admin panel routes
│   └── services/
│       └── nlp_service.py  # Handles query understanding
├── templates/              # HTML templates (login.html, chat.html, etc.)
├── static/                 # JS/CSS assets
├── run.py
└── requirements.txt
