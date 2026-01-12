from flask import Flask, render_template, request, redirect, url_for
from datetime import date
import database

# Initialize Flask app
app = Flask(__name__)

# Initialize the database
database.init_db()

# Define routes
@app.route("/")
def home():
    return redirect("/new-expense")


@app.route("/new-expense", methods=["GET", "POST"])
def new_expense():
    conn = database.get_connection()
    cursor = conn.cursor()

    # Handle form submission
    if request.method == "POST":
        cursor.execute(
            """
            INSERT INTO expenses (value, category, date, house_id)
            VALUES (?, ?, ?, ?)
            """,
            (
                request.form["value"],
                request.form["category"],
                request.form["date"] or str(date.today()),
                request.form["house_id"]
            )
        )
        conn.commit()
        conn.close()
        return redirect(url_for("home", success=1))
    
    # Fetch houses and expenses for display
    houses = cursor.execute("SELECT id, name FROM houses").fetchall()

    conn.close()

    return render_template(
        "new-expense.html",
        houses=houses,
        today=str(date.today())
    )


@app.route("/edit-expense/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    conn = database.get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        cursor.execute(
            """
            UPDATE expenses
            SET value = ?, category = ?, date = ?, house_id = ?
            WHERE id = ?
            """,
            (
                request.form["value"],
                request.form["category"],
                request.form["date"],
                request.form["house_id"],
                expense_id
            )
        )
        conn.commit()
        conn.close()
        return redirect("/expenses")

    expense = cursor.execute(
        "SELECT id, value, category, date, house_id FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()

    houses = cursor.execute("SELECT id, name FROM houses").fetchall()
    conn.close()

    return render_template("edit-expense.html", expense=expense, houses=houses)


@app.route("/remove-expense/<int:expense_id>")
def remove_expense(expense_id):
    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

    return redirect("/expenses")


@app.route("/expenses")
def expenses():
    conn = database.get_connection()
    cursor = conn.cursor()

    # Fetch all expenses with associated house names
    expenses = cursor.execute("""
        SELECT g.id, g.value, g.category, g.date, c.name
        FROM expenses g
        JOIN houses c ON g.house_id = c.id
        ORDER BY g.date DESC
    """).fetchall()
    conn.close()

    return render_template("expenses.html", expenses=expenses)

@app.route("/houses")
def houses():  
    conn = database.get_connection()
    cursor = conn.cursor()

    # Fetch all houses
    houses = cursor.execute("SELECT id, name FROM houses").fetchall()
    conn.close()

    return render_template("houses.html", houses=houses)

@app.route("/new-house", methods=["GET", "POST"])
def new_house():
    if request.method == "POST":
        name = request.form["name"]
        conn = database.get_connection()
        cursor = conn.cursor()

        # Insert new house into the database
        cursor.execute(
            "INSERT INTO houses (name) VALUES (?)",
            (name,)
        )

        conn.commit()
        conn.close()

    return redirect("/houses")


@app.route("/remove-house/<int:house_id>")
def remove_house(house_id):
    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM houses WHERE id = ?", (house_id,))
    conn.commit()
    conn.close()

    return redirect("/houses")

if __name__ == "__main__":
    app.run(debug=True)