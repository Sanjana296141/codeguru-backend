# CodeGuru Backend

Backend API for **CodeGuru**, an AI-powered Python code review platform. The backend handles user authentication, file uploads, static code analysis, AI review generation, report exports, and dashboard analytics.

---

## Features

- 🔐 JWT Authentication
- 👤 User Registration & Login
- 📂 Upload Python (.py) Files
- 🤖 AI Code Review (Ollama - Local)
- 📊 Static Analysis
  - Pylint
  - Bandit
  - Radon
- 📈 Dashboard Analytics
- 📜 Review History
- 📄 Export Reports
  - PDF
  - HTML
  - Markdown
- 📝 AI Documentation Generation
- 🗄 PostgreSQL Database
- 🔄 Alembic Database Migrations

---

## 🛠 Tech Stack

- Python
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- PostgreSQL
- SQLAlchemy
- Alembic
- Pylint
- Bandit
- Radon
- Ollama (Qwen 2.5)
- ReportLab

---

## 📁 Project Structure

backend/
├── models/
├── routes/
├── services/
├── utils/
├── migrations/
├── uploads/
├── reports/
├── app.py
├── config.py
└── requirements.txt

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Sanjana296141/codeguru-backend.git
```

Move to project

```bash
cd codeguru-backend
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create `.env`

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
```

Run database migrations

```bash
flask db upgrade
```

Run server

```bash
python app.py
```

Backend runs on

```
http://127.0.0.1:5000
```

---

## 🤖 AI Support

### Local Development

Uses **Ollama (Qwen 2.5)** for AI-powered code review and documentation generation.

### Production

If Ollama is unavailable, the application gracefully falls back to static analysis using:

- Pylint
- Bandit
- Radon

This ensures uninterrupted functionality in deployment environments.

---

## 📌 API Modules

- Authentication
- Upload
- Reviews
- Dashboard
- History
- Export
- AI Review
- Documentation

---

## 📄 License

This project is developed for educational and portfolio purposes.
