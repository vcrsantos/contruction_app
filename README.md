# Construction Expense Manager

A simple web application built with Flask to record and manage construction expenses.

## 📋 Description

This project is a web application that allows users to record and manage expense values in construction projects through an interactive, user-friendly interface. It supports multiple properties, expense categorization, and complete CRUD operations.

## 🚀 Features

- ✅ Multiple houses/properties management
- ✅ Complete expense CRUD operations
- ✅ Expense categorization (Material, Pedreiro, IPTU, Engineer, etc.)
- ✅ Expense association with properties
- ✅ Automatic date assignment (customizable)
- ✅ Responsive web interface
- ✅ Data persistence with SQLite

## 🛠️ Technologies Used

- **Python 3.7+** - Programming language
- **Flask** - Web framework
- **SQLite** - Local database
- **Jinja2** - Template engine
- **HTML5/CSS3** - Interface

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

1. **Create House**: Go to "Houses" → fill "House name" → "Save"
2. **Record Expense**: Click "New Expense" → fill the form → "Save Expense"
   - Value (R$)
   - Category (Material, Pedreiro, IPTU, etc.)
   - Date (default: today)
   - Associated house
3. **View Expenses**: Access "Expenses" to see the complete list
4. **Edit**: Click the ✏️ next to the expense
5. **Remove**: Click the ❌ to delete

## 📂 Project Structure

```
construcao/
├── app.py                    # Main Flask application
├── database.py               # Database configuration and initialization
├── templates/
│   ├── base.html            # Base template with navigation
│   ├── new-expense.html     # New expense form
│   ├── edit-expense.html    # Edit expense form
│   ├── expenses.html        # Expenses listing
│   ├── houses.html          # Houses management
│   ├── remove-house.html    # Remove house confirmation
│   └── index.html           # Legacy template
├── construction.db          # SQLite database
├── venv/                    # Virtual environment
└── README.md                # This file
```

## 🗂️ Database

**`houses` table:**
- `id` - Primary key
- `name` - House name

**`expenses` table:**
- `id` - Primary key
- `value` - Expense value (R$)
- `category` - Expense category
- `date` - Expense date
- `house_id` - Foreign key to houses

## 📊 Expense Categories

Material, Pedreiro, IPTU, Escritório, Terreno, Cartório, Desmembramento, Limpeza do terreno, Engenheiro, Container, Poste, Consumo Água, Consumo Luz

## 📄 License

This project is free to use.

## 👨‍💻 Author

Victor Santos