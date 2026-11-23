from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supplychain-secret-key"

DATABASE = "supplychain.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_id TEXT UNIQUE NOT NULL,
            customer TEXT NOT NULL,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            status TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def dashboard():
    conn = get_db()

    total = conn.execute(
        "SELECT COUNT(*) FROM shipments"
    ).fetchone()[0]

    pending = conn.execute(
        "SELECT COUNT(*) FROM shipments WHERE status='Pending'"
    ).fetchone()[0]

    in_transit = conn.execute(
        "SELECT COUNT(*) FROM shipments WHERE status='In Transit'"
    ).fetchone()[0]

    delivered = conn.execute(
        "SELECT COUNT(*) FROM shipments WHERE status='Delivered'"
    ).fetchone()[0]

    delayed = conn.execute(
        "SELECT COUNT(*) FROM shipments WHERE status='Delayed'"
    ).fetchone()[0]

    inventory_total = conn.execute(
        "SELECT COALESCE(SUM(quantity), 0) FROM inventory"
    ).fetchone()[0]

    low_stock = conn.execute(
        "SELECT COUNT(*) FROM inventory WHERE status='Low Stock'"
    ).fetchone()[0]

    recent_shipments = conn.execute("""
        SELECT *
        FROM shipments
        ORDER BY id DESC
        LIMIT 6
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        total=total,
        pending=pending,
        in_transit=in_transit,
        delivered=delivered,
        delayed=delayed,
        inventory_total=inventory_total,
        low_stock=low_stock,
        recent_shipments=recent_shipments
    )


@app.route("/shipments")
def shipments():
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()

    conn = get_db()

    query = """
        SELECT *
        FROM shipments
        WHERE 1=1
    """

    params = []

    if search:
        query += """
            AND (
                tracking_id LIKE ?
                OR customer LIKE ?
                OR origin LIKE ?
                OR destination LIKE ?
            )
        """

        search_value = f"%{search}%"

        params.extend([
            search_value,
            search_value,
            search_value,
            search_value
        ])

    if status:
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY id DESC"

    shipments_data = conn.execute(
        query,
        params
    ).fetchall()

    conn.close()

    return render_template(
        "shipments.html",
        shipments=shipments_data,
        search=search,
        selected_status=status
    )


@app.route("/add-shipment", methods=["POST"])
def add_shipment():

    tracking_id = request.form.get("tracking_id", "").strip().upper()
    customer = request.form.get("customer", "").strip()
    origin = request.form.get("origin", "").strip()
    destination = request.form.get("destination", "").strip()
    status = request.form.get("status", "").strip()
    date = request.form.get("date", "").strip()

    if not all([
        tracking_id,
        customer,
        origin,
        destination,
        status,
        date
    ]):
        flash("Please fill in all shipment fields.", "error")
        return redirect(url_for("shipments"))

    conn = get_db()

    try:
        conn.execute("""
            INSERT INTO shipments
            (
                tracking_id,
                customer,
                origin,
                destination,
                status,
                date
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            tracking_id,
            customer,
            origin,
            destination,
            status,
            date
        ))

        conn.commit()
        flash("Shipment added successfully.", "success")

    except sqlite3.IntegrityError:
        flash("Tracking ID already exists.", "error")

    finally:
        conn.close()

    return redirect(url_for("shipments"))


@app.route("/update-shipment/<int:shipment_id>", methods=["POST"])
def update_shipment(shipment_id):

    status = request.form.get("status", "").strip()

    allowed_statuses = [
        "Pending",
        "In Transit",
        "Delivered",
        "Delayed"
    ]

    if status not in allowed_statuses:
        flash("Invalid shipment status.", "error")
        return redirect(url_for("shipments"))

    conn = get_db()

    conn.execute("""
        UPDATE shipments
        SET status = ?
        WHERE id = ?
    """, (status, shipment_id))

    conn.commit()
    conn.close()

    flash("Shipment status updated.", "success")

    return redirect(url_for("shipments"))


@app.route("/delete-shipment/<int:shipment_id>", methods=["POST"])
def delete_shipment(shipment_id):

    conn = get_db()

    conn.execute("""
        DELETE FROM shipments
        WHERE id = ?
    """, (shipment_id,))

    conn.commit()
    conn.close()

    flash("Shipment deleted successfully.", "success")

    return redirect(url_for("shipments"))


@app.route("/track", methods=["GET", "POST"])
def track():

    shipment = None
    searched_id = ""

    if request.method == "POST":

        searched_id = request.form.get(
            "tracking_id",
            ""
        ).strip().upper()

        conn = get_db()

        shipment = conn.execute("""
            SELECT *
            FROM shipments
            WHERE UPPER(tracking_id) = ?
        """, (searched_id,)).fetchone()

        conn.close()

    return render_template(
        "track.html",
        shipment=shipment,
        searched_id=searched_id
    )


@app.route("/inventory")
def inventory():

    search = request.args.get(
        "search",
        ""
    ).strip()

    conn = get_db()

    if search:

        inventory_items = conn.execute("""
            SELECT *
            FROM inventory
            WHERE item_name LIKE ?
               OR category LIKE ?
            ORDER BY id DESC
        """, (
            f"%{search}%",
            f"%{search}%"
        )).fetchall()

    else:

        inventory_items = conn.execute("""
            SELECT *
            FROM inventory
            ORDER BY id DESC
        """).fetchall()

    total_items = conn.execute("""
        SELECT COALESCE(SUM(quantity), 0)
        FROM inventory
    """).fetchone()[0]

    low_stock = conn.execute("""
        SELECT COUNT(*)
        FROM inventory
        WHERE status='Low Stock'
    """).fetchone()[0]

    in_stock = conn.execute("""
        SELECT COUNT(*)
        FROM inventory
        WHERE status='In Stock'
    """).fetchone()[0]

    conn.close()

    return render_template(
        "inventory.html",
        inventory_items=inventory_items,
        total_items=total_items,
        low_stock=low_stock,
        in_stock=in_stock,
        search=search
    )


@app.route("/add-inventory", methods=["POST"])
def add_inventory():

    item_name = request.form.get(
        "item_name",
        ""
    ).strip()

    category = request.form.get(
        "category",
        ""
    ).strip()

    quantity_text = request.form.get(
        "quantity",
        ""
    ).strip()

    if not item_name or not category or not quantity_text:
        flash("Please fill in all inventory fields.", "error")
        return redirect(url_for("inventory"))

    try:
        quantity = int(quantity_text)
    except ValueError:
        flash("Quantity must be a valid number.", "error")
        return redirect(url_for("inventory"))

    if quantity <= 0:
        flash("Quantity must be greater than zero.", "error")
        return redirect(url_for("inventory"))

    if quantity <= 10:
        status = "Low Stock"
    else:
        status = "In Stock"

    conn = get_db()

    conn.execute("""
        INSERT INTO inventory
        (
            item_name,
            category,
            quantity,
            status
        )
        VALUES (?, ?, ?, ?)
    """, (
        item_name,
        category,
        quantity,
        status
    ))

    conn.commit()
    conn.close()

    flash("Inventory item added successfully.", "success")

    return redirect(url_for("inventory"))


@app.route("/delete-inventory/<int:item_id>", methods=["POST"])
def delete_inventory(item_id):

    conn = get_db()

    conn.execute("""
        DELETE FROM inventory
        WHERE id = ?
    """, (item_id,))

    conn.commit()
    conn.close()

    flash("Inventory item deleted successfully.", "success")

    return redirect(url_for("inventory"))


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "error.html",
        error_code=404,
        message="Page not found."
    ), 404


if __name__ == "__main__":
    init_db()
    app.run(debug=True)