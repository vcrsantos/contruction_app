# Construction

A simple web application built with Flask to record and manage construction expenses.

## 📋 Description

This project is a web application that allows users to record expense values in construction projects through an interactive form.

## 🚀 Features

- Simple and intuitive web interface
- Expense value recording
- Data processing via POST form

## 🛠️ Technologies Used

- **Python** - Programming language
- **Flask** - Web framework
- **HTML** - Interface markup

## 📦 Requirements

- Python 3.7+
- Flask

## 💻 Installation

1. Clone or access the repository:
```bash
cd construcao
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install flask
```

## ▶️ How to Run

1. Activate the virtual environment (if not already activated):
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Run the application:
```bash
python app.py
```

3. Access in your browser:
```
http://localhost:5000
```

## 📝 Usage

1. Open your browser and go to `http://localhost:5000`
2. Enter the expense value in the "Valor do gasto" field
3. Click "Salvar"
4. The value will be processed and displayed on the screen

## 📂 Project Structure

```
construcao/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # Main page HTML template
└── README.md           # This file
```

## 🔄 Future Improvements

- Data persistence with database
- Input validation
- Improved UI with CSS
- Historical expenses listing
- User authentication

## 📄 License

This project is free to use.

## 👨‍💻 Author

Victor

---

**Last updated:** January 2026
