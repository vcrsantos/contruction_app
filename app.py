from flask import Flask, render_template, request, redirect
import database

# Initialize Flask app
app = Flask(__name__)

# Initialize the database
database.init_db()

# Define routes
@app.route("/", methods=["GET", "POST"])
def home():
    # Handle form submission
    if request.method == "POST":
        # Get form data
        valor = request.form["valor"]
        categoria = request.form["categoria"]
        data = request.form["data"]

        # Insert data into the database
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO gastos (valor, categoria, data)
            VALUES (?, ?, ?)
        ''', (valor, categoria, data))
        conn.commit()
        conn.close()

        # Redirect to home page after submission
        return redirect("/")
    
    # Fetch all gastos from the database
    conn = database.get_connection()
    cursor = conn.cursor()
    gastos = cursor.execute("SELECT valor, categoria, data FROM gastos").fetchall()
    conn.close()

    return render_template("index.html", gastos=gastos)


if __name__ == "__main__":
    app.run()