from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date
import database
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))


@app.template_filter('brl')
def brl_filter(value):
    try:
        v = float(value)
        formatted = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {formatted}"
    except (ValueError, TypeError):
        return "R$ 0,00"

database.init_db()
database.seed_categories()


@app.route("/")
def home():
    return redirect("/expenses")


@app.route("/expenses", methods=["GET", "POST"])
def expenses():
    conn = database.get_connection()
    try:
        cursor = conn.cursor()

        if request.method == "POST":
            value = request.form.get("value", "").strip()
            category_id = request.form.get("category_id", "").strip()
            house_id = request.form.get("house_id", "").strip()

            if not value or float(value) <= 0:
                flash("Valor deve ser maior que zero.", "error")
                return redirect("/expenses")
            if not category_id or not house_id:
                flash("Categoria e casa são obrigatórios.", "error")
                return redirect("/expenses")

            category_name = cursor.execute(
                "SELECT name FROM categories WHERE id = ?", (category_id,)
            ).fetchone()[0]

            cursor.execute(
                "INSERT INTO expenses (value, category, date, house_id, observations) VALUES (?, ?, ?, ?, ?)",
                (
                    request.form["value"],
                    category_name,
                    request.form["date"] or str(date.today()),
                    request.form["house_id"],
                    request.form.get("observations", ""),
                ),
            )
            conn.commit()
            flash("Gasto salvo com sucesso!", "success")
            return redirect("/expenses")

        categories = cursor.execute("SELECT id, name FROM categories ORDER BY name").fetchall()
        houses = cursor.execute("SELECT id, name FROM houses").fetchall()

        # Build filtered query
        query = """
            SELECT g.id, g.value, g.category, g.date, c.name, g.observations
            FROM expenses g
            JOIN houses c ON g.house_id = c.id
            WHERE 1=1
        """
        params = []

        filter_house = request.args.get("house_id", "")
        filter_category = request.args.get("category_id", "")
        filter_start = request.args.get("start_date", "")
        filter_end = request.args.get("end_date", "")

        if filter_house:
            query += " AND g.house_id = ?"
            params.append(filter_house)
        if filter_category:
            query += " AND g.category = (SELECT name FROM categories WHERE id = ?)"
            params.append(filter_category)
        if filter_start:
            query += " AND g.date >= ?"
            params.append(filter_start)
        if filter_end:
            query += " AND g.date <= ?"
            params.append(filter_end)

        query += " ORDER BY g.date DESC"
        expenses = cursor.execute(query, params).fetchall()

        return render_template("expenses.html", houses=houses, categories=categories, expenses=expenses, today=str(date.today()),
                               filter_house=filter_house, filter_category=filter_category, filter_start=filter_start, filter_end=filter_end)
    finally:
        conn.close()


@app.route("/edit-expense/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    conn = database.get_connection()
    try:
        cursor = conn.cursor()

        if request.method == "POST":
            value = request.form.get("value", "").strip()
            category_id = request.form.get("category_id", "").strip()
            house_id = request.form.get("house_id", "").strip()

            if not value or float(value) <= 0:
                flash("Valor deve ser maior que zero.", "error")
                return redirect(f"/edit-expense/{expense_id}")
            if not category_id or not house_id:
                flash("Categoria e casa são obrigatórios.", "error")
                return redirect(f"/edit-expense/{expense_id}")

            category_name = cursor.execute(
                "SELECT name FROM categories WHERE id = ?", (category_id,)
            ).fetchone()[0]

            cursor.execute(
                "UPDATE expenses SET value = ?, category = ?, date = ?, house_id = ?, observations = ? WHERE id = ?",
                (
                    request.form["value"],
                    category_name,
                    request.form["date"],
                    request.form["house_id"],
                    request.form.get("observations", ""),
                    expense_id,
                ),
            )
            conn.commit()
            flash("Gasto atualizado!", "success")
            return redirect("/expenses")

        expense = cursor.execute(
            "SELECT id, value, category, date, house_id, observations FROM expenses WHERE id = ?", (expense_id,)
        ).fetchone()
        categories = cursor.execute("SELECT id, name FROM categories ORDER BY name").fetchall()
        houses = cursor.execute("SELECT id, name FROM houses").fetchall()

        return render_template("edit-expense.html", expense=expense, houses=houses, categories=categories)
    finally:
        conn.close()


@app.route("/remove-expense/<int:expense_id>", methods=["POST"])
def remove_expense(expense_id):
    conn = database.get_connection()
    try:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        flash("Gasto removido!", "success")
    finally:
        conn.close()
    return redirect("/expenses")


@app.route("/houses")
def houses():
    conn = database.get_connection()
    try:
        houses = conn.execute("""
            SELECT h.id, h.name, h.selling_price, h.observations, IFNULL(SUM(e.value), 0)
            FROM houses h
            LEFT JOIN expenses e ON h.id = e.house_id
            GROUP BY h.id
        """).fetchall()
        return render_template("houses.html", houses=houses)
    finally:
        conn.close()


@app.route("/new-house", methods=["POST"])
def new_house():
    name = request.form.get("name", "").strip()
    if not name:
        flash("Nome da casa é obrigatório.", "error")
        return redirect("/houses")

    conn = database.get_connection()
    try:
        conn.execute(
            "INSERT INTO houses (name, selling_price, observations) VALUES (?, ?, ?)",
            (request.form["name"], request.form.get("selling_price"), request.form.get("observations")),
        )
        conn.commit()
        flash("Casa salva com sucesso!", "success")
    finally:
        conn.close()
    return redirect("/houses")


@app.route("/edit-house/<int:house_id>", methods=["GET", "POST"])
def edit_house(house_id):
    conn = database.get_connection()
    try:
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            if not name:
                flash("Nome da casa é obrigatório.", "error")
                return redirect(f"/edit-house/{house_id}")

            conn.execute(
                "UPDATE houses SET name = ?, selling_price = ?, observations = ? WHERE id = ?",
                (request.form["name"], request.form.get("selling_price"), request.form.get("observations"), house_id),
            )
            conn.commit()
            flash("Casa atualizada!", "success")
            return redirect("/houses")

        house = conn.execute("SELECT id, name, selling_price, observations FROM houses WHERE id = ?", (house_id,)).fetchone()
        return render_template("edit-house.html", house=house)
    finally:
        conn.close()


@app.route("/remove-house/<int:house_id>", methods=["POST"])
def remove_house(house_id):
    conn = database.get_connection()
    try:
        using = conn.execute("SELECT COUNT(*) FROM expenses WHERE house_id = ?", (house_id,)).fetchone()[0]
        if using > 0:
            flash("Casa possui gastos vinculados. Não pode remover.", "error")
            return redirect("/houses")

        conn.execute("DELETE FROM houses WHERE id = ?", (house_id,))
        conn.commit()
        flash("Casa removida!", "success")
    finally:
        conn.close()
    return redirect("/houses")


@app.route("/categories")
def categories():
    conn = database.get_connection()
    try:
        categories = conn.execute("SELECT id, name FROM categories ORDER BY name").fetchall()
        return render_template("categories.html", categories=categories)
    finally:
        conn.close()


@app.route("/new-category", methods=["POST"])
def new_category():
    name = request.form.get("name", "").strip()
    if not name:
        flash("Nome da categoria é obrigatório.", "error")
        return redirect("/categories")

    conn = database.get_connection()
    try:
        conn.execute("INSERT INTO categories (name) VALUES (?)", (request.form["name"],))
        conn.commit()
        flash("Categoria salva com sucesso!", "success")
    finally:
        conn.close()
    return redirect("/categories")


@app.route("/remove-category/<int:category_id>", methods=["POST"])
def remove_category(category_id):
    conn = database.get_connection()
    try:
        using = conn.execute(
            "SELECT COUNT(*) FROM expenses WHERE category = (SELECT name FROM categories WHERE id = ?)",
            (category_id,),
        ).fetchone()[0]

        if using > 0:
            flash("Categoria em uso. Não pode remover.", "error")
            return redirect("/categories")

        conn.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        flash("Categoria removida!", "success")
    finally:
        conn.close()
    return redirect("/categories")


@app.route("/edit-category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    conn = database.get_connection()
    try:
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            if not name:
                flash("Nome da categoria é obrigatório.", "error")
                return redirect(f"/edit-category/{category_id}")

            conn.execute("UPDATE categories SET name = ? WHERE id = ?", (name, category_id))
            conn.commit()
            flash("Categoria atualizada!", "success")
            return redirect("/categories")

        category = conn.execute("SELECT id, name FROM categories WHERE id = ?", (category_id,)).fetchone()
        return render_template("edit-category.html", category=category)
    finally:
        conn.close()


if __name__ == "__main__":
    app.run()
