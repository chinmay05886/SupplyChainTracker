from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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

    shipments = conn.execute(
        "SELECT * FROM shipments ORDER BY id DESC LIMIT 5"
    ).fetchall()

    total = conn.execute(
        "SELECT COUNT(*) FROM shipments"
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

    conn.close()

    return render_template(
        "index.html",
        shipments=shipments,
        total=total,
        in_transit=in_transit,
        delivered=delivered,
        delayed=delayed
    )


@app.route("/shipments")
def shipments():
    conn = get_db()

    shipments = conn.execute(
        "SELECT * FROM shipments ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "shipments.html",
        shipments=shipments
    )


@app.route("/add-shipment", methods=["POST"])
def add_shipment():
    tracking_id = request.form["tracking_id"]
    customer = request.form["customer"]
    origin = request.form["origin"]
    destination = request.form["destination"]
    status = request.form["status"]
    date = request.form["date"]

    conn = get_db()

    try:
        conn.execute("""
            INSERT INTO shipments
            (tracking_id, customer, origin, destination, status, date)
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

    except sqlite3.IntegrityError:
        pass

    conn.close()

    return redirect(url_for("shipments"))


@app.route("/track", methods=["GET", "POST"])
def track():
    shipment = None

    if request.method == "POST":
        tracking_id = request.form["tracking_id"]
        tracking_id = tracking_id.replace(" ", "").strip().upper()

        conn = get_db()

        shipment = conn.execute("""
            SELECT *
            FROM shipments
            WHERE REPLACE(UPPER(tracking_id), ' ', '') = ?
        """, (tracking_id,)).fetchone()

        conn.close()

    return render_template(
        "track.html",
        shipment=shipment
    )


@app.route("/inventory")
def inventory():
    conn = get_db()

    inventory_items = conn.execute(
        "SELECT * FROM inventory ORDER BY id DESC"
    ).fetchall()

    total_items = conn.execute(
        "SELECT COALESCE(SUM(quantity), 0) FROM inventory"
    ).fetchone()[0]

    low_stock = conn.execute(
        "SELECT COUNT(*) FROM inventory WHERE status='Low Stock'"
    ).fetchone()[0]

    in_stock = conn.execute(
        "SELECT COUNT(*) FROM inventory WHERE status='In Stock'"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "inventory.html",
        inventory_items=inventory_items,
        total_items=total_items,
        low_stock=low_stock,
        in_stock=in_stock
    )


@app.route("/add-inventory", methods=["POST"])
def add_inventory():
    item_name = request.form["item_name"]
    category = request.form["category"]
    quantity = int(request.form["quantity"])

    if quantity <= 0:
        status = "Low Stock"
    elif quantity <= 10:
        status = "Low Stock"
    else:
        status = "In Stock"

    conn = get_db()

    conn.execute("""
        INSERT INTO inventory
        (item_name, category, quantity, status)
        VALUES (?, ?, ?, ?)
    """, (
        item_name,
        category,
        quantity,
        status
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("inventory"))


@app.route("/settings")
def settings():
    return render_template("settings.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)