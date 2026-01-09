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
            INSERT INTO gastos (valor, categoria, data, casa_id)
            VALUES (?, ?, ?, ?)
            """,
            (
                request.form["valor"],
                request.form["categoria"],
                request.form["data"] or str(date.today()),
                request.form["casa_id"]
            )
        )
        conn.commit()
        conn.close()
        return redirect(url_for("home", sucesso=1))
    
    # Fetch casas and gastos for display
    casas = cursor.execute("SELECT id, nome FROM casas").fetchall()

    # Fetch gastos with associated casa names
    gastos = cursor.execute("""
        SELECT g.id, g.valor, g.categoria, g.data, c.nome
        FROM gastos g
        JOIN casas c ON g.casa_id = c.id
        ORDER BY g.data DESC
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        casas=casas, 
        gastos=gastos,
        hoje=str(date.today()),
        sucesso=request.args.get("sucesso")
    )

# Route to add a new casa
@app.route("/nova_casa", methods=["POST"])
def nova_casa():
    nome = request.form["nome"]
    conn = database.get_connection()
    cursor = conn.cursor()


    # Insert new casa into the database
    cursor.execute(
        "INSERT INTO casas (nome) VALUES (?)",
        (nome,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run()