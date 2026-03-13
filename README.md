# Construction Expense Manager

Web application built with Flask to track and manage construction project expenses.

## 🚀 Features

- Manage multiple houses/properties (name, selling price, notes)
- Full CRUD for expenses with categories and notes
- Customizable categories with default seed data
- Expense filters by house, category and date range
- Brazilian currency formatting (R$)
- Flash feedback messages with fade-out animation
- Backend data validation
- Deletion confirmation dialogs
- Responsive UI with automatic dark mode
- SQLite persistence

## 🛠️ Tech Stack

- Python 3.7+
- Flask
- SQLite
- Jinja2
- HTML5/CSS3

## 💻 Installation

```bash
git clone git@github.com:vcrsantos/contruction_app.git
cd contruction_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Running

```bash
source venv/bin/activate
python app.py
```

Open: http://localhost:5000

## 📂 Structure

```
contruction_app/
├── app.py              # Flask application and routes
├── database.py         # Database setup and initialization
├── backup.py           # Database backup utility
├── wsgi.py             # WSGI entry point for deployment (PythonAnywhere)
├── requirements.txt    # Dependencies
├── templates/
│   ├── base.html           # Base template with navigation
│   ├── expenses.html       # Expense listing and creation
│   ├── edit-expense.html   # Expense editing
│   ├── houses.html         # House listing and creation
│   ├── edit-house.html     # House editing
│   ├── categories.html     # Category listing and creation
│   └── edit-category.html  # Category editing
└── static/
    └── style.css           # Styles with dark mode
```

## 🗂️ Database

**houses**: id, name, selling_price, observations

**categories**: id, name (unique)

**expenses**: id, value, category, date, observations, house_id (FK → houses)

## 🌐 Deploy (PythonAnywhere)

1. Clone the repo on PythonAnywhere: `git clone ...`
2. Set up the Web App pointing WSGI to `wsgi.py`
3. Add static files: URL `/static/` → directory `static/`
4. Reload

## 👨‍💻 Author

Victor Santos
