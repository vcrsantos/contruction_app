from flask import Flask, render_template, request, redirect, url_for
from datetime import date
import database

# Initialize Flask app
app = Flask(__name__)

# Initialize the database
database.init_db()
database.seed_categories()

# Define routes
@app.route("/")
def home():
    return redirect("/expenses")

@app.route("/expenses", methods=["GET", "POST"])
def expenses():
    conn = database.get_connection()
    cursor = conn.cursor()

    # Handle form submission
    if request.method == "POST":
        # Get category name from category_id
        category_id = request.form["category_id"]
        category_name = cursor.execute(
            "SELECT name FROM categories WHERE id = ?",
            (category_id,)
        ).fetchone()[0]
        
        cursor.execute(
            """
            INSERT INTO expenses (value, category, date, house_id, observations)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                request.form["value"],
                category_name,
                request.form["date"] or str(date.today()),
                request.form["house_id"],
                request.form.get("observations", "")
            )
        )
        conn.commit()
        conn.close()
        return redirect("/expenses")
    
    categories = cursor.execute(
        "SELECT id, name FROM categories ORDER BY name"
    ).fetchall()
    
    # Fetch houses for the form
    houses = cursor.execute("SELECT id, name FROM houses").fetchall()

    # Fetch all expenses with associated house names
    expenses = cursor.execute("""
        SELECT g.id, g.value, g.category, g.date, c.name, g.observations
        FROM expenses g
        JOIN houses c ON g.house_id = c.id
        ORDER BY g.date DESC
    """).fetchall()
    
    conn.close()

    return render_template(
        "expenses.html",
        houses=houses,
        categories=categories,
        expenses=expenses,
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
            SET value = ?, category = ?, date = ?, house_id = ?, observations = ?
            WHERE id = ?
            """,
            (
                request.form["value"],
                request.form["category"],
                request.form["date"],
                request.form["house_id"],
                request.form.get("observations", ""),
                expense_id
            )
        )
        conn.commit()
        conn.close()
        return redirect("/expenses")

    expense = cursor.execute(
        "SELECT id, value, category, date, house_id, observations FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()

    categories = cursor.execute("SELECT id, name FROM categories ORDER BY name").fetchall()

    houses = cursor.execute("SELECT id, name FROM houses").fetchall()
    conn.close()

    return render_template("edit-expense.html", expense=expense, houses=houses, categories=categories)


@app.route("/remove-expense/<int:expense_id>")
def remove_expense(expense_id):
    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

    return redirect("/expenses")

@app.route("/houses")
def houses():  
    conn = database.get_connection()
    cursor = conn.cursor()

    # Fetch all houses
    houses = cursor.execute("""
        SELECT
            h.id,
            h.name,
            h.selling_price,
            h.observations,
            IFNULL(SUM(e.value), 0)
        FROM houses h 
        LEFT JOIN expenses e ON h.id = e.house_id
        GROUP BY h.id""").fetchall()
    conn.close()

    return render_template("houses.html", houses=houses)

@app.route("/new-house", methods=["GET", "POST"])
def new_house():
    if request.method == "POST":
        name = request.form["name"]
        selling_price = request.form.get("selling_price")
        observations = request.form.get("observations")
        conn = database.get_connection()
        cursor = conn.cursor()

        # Insert new house into the database
        cursor.execute(
            "INSERT INTO houses (name, selling_price, observations) VALUES (?, ?, ?)",
            (name, selling_price, observations)
        )

        conn.commit()
        conn.close()

    return redirect("/houses")


@app.route("/edit-house/<int:house_id>", methods=["GET", "POST"])
def edit_house(house_id):
    conn = database.get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        selling_price = request.form.get("selling_price")
        observations = request.form.get("observations")

        cursor.execute(
            "UPDATE houses SET name = ?, selling_price = ?, observations = ? WHERE id = ?",
            (name, selling_price, observations, house_id)
        )
        conn.commit()
        conn.close()
        return redirect("/houses")

    house = cursor.execute(
        "SELECT id, name, selling_price, observations FROM houses WHERE id = ?",
        (house_id,)
    ).fetchone()
    conn.close()

    return render_template("edit-house.html", house=house)

@app.route("/remove-house/<int:house_id>")
def remove_house(house_id):
    conn = database.get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM houses WHERE id = ?", (house_id,))
    conn.commit()
    conn.close()

    return redirect("/houses")


@app.route("/categories")
def categories():  
    conn = database.get_connection()
    cursor = conn.cursor()

    # Fetch all categories
    categories = cursor.execute("SELECT id, name FROM categories ORDER BY name").fetchall()
    conn.close()

    return render_template("categories.html", categories=categories)

@app.route("/new-category", methods=["GET", "POST"])
def new_category():
    if request.method == "POST":
        name = request.form["name"]
        conn = database.get_connection()
        cursor = conn.cursor()

        # Insert new category into the database
        cursor.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (name,)
        )

        conn.commit()
        conn.close()

    return redirect("/categories")

@app.route("/remove-category/<int:category_id>")
def remove_category(category_id):
    conn = database.get_connection()
    cursor = conn.cursor()

    using = cursor.execute(
        "SELECT COUNT(*) FROM expenses WHERE category = (SELECT name FROM categories WHERE id = ?)",
        (category_id,)
    ).fetchone()[0]

    if using > 0:
        conn.close()
        return "Categoria em uso. Não pode remover.", 400

    cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    conn.commit()
    conn.close()

    return redirect("/categories")

@app.route("/edit-category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    conn = database.get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]

        cursor.execute(
            "UPDATE categories SET name = ? WHERE id = ?",
            (name, category_id)
        )

        conn.commit()
        conn.close()

        return redirect("/categories")

    category = cursor.execute(
        "SELECT id, name FROM categories WHERE id = ?",
        (category_id,)
    ).fetchone()

    conn.close()

    return render_template("edit-category.html", category=category)

if __name__ == "__main__":
    app.run(debug=True)