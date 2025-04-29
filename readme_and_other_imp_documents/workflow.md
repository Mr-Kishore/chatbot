chatbot_app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/  # optional, empty for now
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── employee.py
│   │   └── admin.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── nlp_service.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   └── chat.html
├── data/
│   └── monitor_log.txt
├── monitor_folder.py
├── view_data.py
├── run.py
└── requirements.txt