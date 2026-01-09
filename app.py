from flask import Flask, render_template, request, redirect, url_for
from datetime import date
import database

# Initialize Flask app
app = Flask(__name__)

# Initialize the database
database.init_db()

# Define routes
@app.route("/", methods=["GET", "POST"])
def home():
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

    # Fetch expenses with associated house names
    expenses = cursor.execute("""
        SELECT g.id, g.value, g.category, g.date, c.name
        FROM expenses g
        JOIN houses c ON g.house_id = c.id
        ORDER BY g.date DESC
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        houses=houses, 
        expenses=expenses,
        hoje=str(date.today()),
        sucesso=request.args.get("sucesso")
    )

# Route to add a new house
@app.route("/new_house", methods=["POST"])
def new_house():
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

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)