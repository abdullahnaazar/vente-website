from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "vente_secret_key_2026"
DB = "vente.db"


# ── DATABASE 

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur  = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT    NOT NULL,
            price     REAL    NOT NULL,
            category  TEXT    NOT NULL,
            size      TEXT    NOT NULL,
            stock     INTEGER NOT NULL DEFAULT 0,
            image_url TEXT
        );

        CREATE TABLE IF NOT EXISTS orders (
            id            INTEGER  PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT     NOT NULL,
            email         TEXT     NOT NULL,
            phone         TEXT     NOT NULL,
            address       TEXT     NOT NULL,
            total         REAL     NOT NULL,
            status        TEXT     NOT NULL DEFAULT 'pending',
            created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id     INTEGER NOT NULL REFERENCES orders(id),
            product_id   INTEGER NOT NULL REFERENCES products(id),
            product_name TEXT    NOT NULL,
            price        REAL    NOT NULL,
            quantity     INTEGER NOT NULL,
            size         TEXT
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id         INTEGER  PRIMARY KEY AUTOINCREMENT,
            name       TEXT     NOT NULL,
            email      TEXT     NOT NULL,
            message    TEXT     NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS contact (
            id         INTEGER  PRIMARY KEY AUTOINCREMENT,
            name       TEXT     NOT NULL,
            email      TEXT     NOT NULL,
            phone      TEXT,
            message    TEXT     NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Seed products only once
    if cur.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        seed = [
            ("Classic Black Hoodie",    3599, "Hoodies",  "S,M,L,XL,XXL", 30,
             "https://pk-live-21.slatic.net/kf/Sd263403da536434f8e305c1f47667b42j.jpg"),
            ("Green & White Combo",     3999, "Sets",     "S,M,L,XL",     20,
             "https://assets.ajio.com/medias/sys_master/root/20231006/uGY7/65200a08afa4cf41f52e0fd0/-473Wx593H-466679697-green-MODEL.jpg"),
            ("Blue White Shade Hoodie", 2999, "Hoodies",  "S,M,L,XL,XXL", 25,
             "https://ae-pic-a1.aliexpress-media.com/kf/Sff361cba0fd44c0bb449b088d921ce9fs.jpg"),
            ("Classic Women's Outfit",  4999, "Sets",     "S,M,L,XL",     15,
             "https://i.pinimg.com/236x/88/02/03/88020364137ab869a02319c3b3bcc7a9.jpg"),
            ("Simple White Hoodie",     3599, "Hoodies",  "S,M,L,XL,XXL", 40,
             "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlubZU2IGyWo7U9POdfIDxIv7oDmTqC8K8Ww&s"),
            ("White Hoodie for Girls",  4999, "Hoodies",  "S,M,L,XL",     18,
             "https://pk-live-21.slatic.net/kf/Sd87bae498388405a9d34105633c43423n.jpg"),
            ("Modern Shirt",            3500, "Shirts",   "S,M,L,XL",     35,
             "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRixijHdx70vXWp3Hxy4_1iO1hCD3PBT97zlg&s"),
            ("Hoodie for Girls",        3699, "Hoodies",  "S,M,L,XL",     22,
             "https://rukmini1.flixcart.com/image/1500/1500/xif0q/sweatshirt/v/o/i/l-newlyshweatshirt21-draxstar-original-imahhe9mubsqwxdv.jpeg?q=70"),
            ("Brown Polo Neck Shirt",   2999, "Shirts",   "S,M,L,XL",     30,
             "https://5.imimg.com/data5/SELLER/Default/2026/2/583757184/MG/GU/RD/38646945/polo-neck-printed-t-shirts-220-gsm.jpg"),
            ("Simple Brown T-Shirt",    3299, "T-Shirts", "S,M,L,XL",     50,
             "https://xcdn.next.co.uk/common/items/default/default/itemimages/3_4Ratio/product/lge/Y16812s13.jpg?im=Resize,width=750"),
            ("Plain Black Shirt",       2799, "Shirts",   "S,M,L,XL",     45,
             "https://bluestoneclothing.pk/cdn/shop/files/Black_91aabf0b-386d-4837-8808-865948468104_1200x.jpg?v=1751530847"),
            ("Plain Blue Shirt",        2999, "Shirts",   "S,M,L,XL",     38,
             "https://xcdn.next.co.uk/common/items/default/default/itemimages/3_4Ratio/product/lge/F90841s5.jpg"),
            ("Pink Top with Blue Pant", 4599, "Sets",     "S,M,L,XL",     12,
             "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2xeEyTMbXjaC9nE0SgNw7L2nwY8uJg5OmYw&s"),
            ("White Classic Top",       3199, "T-Shirts", "S,M,L,XL",     28,
             "https://shopmicas.com/cdn/shop/files/b2dd2bb8-a505-4b87-9524-dc2c80873b94_1024x1024.jpg?v=1777453557"),
            ("Blue Hoodie for Women",   3799, "Hoodies",  "S,M,L,XL",     20,
             "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtZZQOoC1Bc3PO5paR_thJWDThnD_JgOiMew&s"),
            ("Premium Pleated Palazzo", 3399, "Bottoms",  "S,M,L,XL",     17,
             "https://i.pinimg.com/474x/fb/0a/8f/fb0a8f25259e884e0a72c4fc7f55ae73.jpg"),
            ("Top for Women",           3700, "T-Shirts", "S,M,L,XL",     25,
             "https://i.pinimg.com/236x/38/a5/49/38a5495e95aa8285e4e977bae6a2ebe4.jpg"),
            ("Plain Green Hoodie",      2999, "Hoodies",  "S,M,L,XL,XXL", 33,
             "https://renebassett.com/cdn/shop/files/SweatVerde1_2385ae39-abd7-4af6-9625-e19d7f17a6e7.jpg?v=1698157010"),
            ("Green White Jacket",      4200, "Outerwear","S,M,L,XL",     10,
             "https://i.pinimg.com/736x/58/0a/0e/580a0e916a2db478e08ea549da42426f.jpg"),
            ("Crop Top & Wide Leg",     4299, "Sets",     "S,M,L,XL",     14,
             "https://i.pinimg.com/236x/9f/e4/14/9fe414097a72d47a1473582b72a2153e.jpg"),
        ]
        cur.executemany(
            "INSERT INTO products (name, price, category, size, stock, image_url) VALUES (?,?,?,?,?,?)",
            seed
        )

    conn.commit()
    conn.close()


# ── CART HELPERS

def get_cart():
    return session.get("cart", {})

def cart_count():
    return sum(item["qty"] for item in get_cart().values())

def cart_total():
    return sum(item["price"] * item["qty"] for item in get_cart().values())

app.jinja_env.globals["cart_count"] = cart_count


# ── PAGES ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/products")
def products():
    category = request.args.get("category", "")
    conn = get_db()

    if category:
        rows = conn.execute(
            "SELECT * FROM products WHERE category = ? ORDER BY name", (category,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM products ORDER BY category, name"
        ).fetchall()

    categories = conn.execute(
        "SELECT DISTINCT category FROM products ORDER BY category"
    ).fetchall()

    conn.close()
    return render_template("products.html", products=rows, categories=categories, active_cat=category)


@app.route("/cart")
def cart():
    return render_template("cart.html", cart=get_cart(), total=cart_total())


@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    conn    = get_db()
    product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()

    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("products"))

    size = request.form.get("size", "")
    qty  = int(request.form.get("qty", 1))
    key  = f"{product_id}_{size}"
    cart = get_cart()

    if key in cart:
        cart[key]["qty"] += qty
    else:
        cart[key] = {
            "product_id": product_id,
            "name":       product["name"],
            "price":      product["price"],
            "size":       size,
            "qty":        qty,
            "image_url":  product["image_url"],
        }

    session["cart"] = cart
    flash(f'"{product["name"]}" added to cart.', "success")
    return redirect(url_for("products"))


@app.route("/cart/remove/<string:key>", methods=["POST"])
def remove_from_cart(key):
    cart = get_cart()
    cart.pop(key, None)
    session["cart"] = cart
    flash("Item removed from cart.", "success")
    return redirect(url_for("cart"))


@app.route("/cart/update", methods=["POST"])
def update_cart():
    cart = get_cart()

    for key in list(cart.keys()):
        qty = int(request.form.get(f"qty_{key}", 0))
        if qty <= 0:
            cart.pop(key)
        else:
            cart[key]["qty"] = qty

    session["cart"] = cart
    flash("Cart updated.", "success")
    return redirect(url_for("cart"))


# ── CHECKOUT / ORDER PLACEMENT ────────────────────────────────────────────────

@app.route("/checkout", methods=["POST"])
def checkout():
    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip()
    phone   = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()
    city    = request.form.get("city", "").strip()

    if not all([name, phone, address, city]):
        flash("Please fill in all required delivery fields.", "error")
        return redirect(url_for("cart"))

    cart = get_cart()
    if not cart:
        flash("Your cart is empty.", "error")
        return redirect(url_for("products"))

    # Calculate total (shipping flat 200 PKR)
    subtotal = cart_total()
    shipping = 200
    total    = subtotal + shipping

    full_address = f"{address}, {city}"

    conn = get_db()
    cur  = conn.cursor()

    # Insert order
    cur.execute(
        "INSERT INTO orders (customer_name, email, phone, address, total) VALUES (?,?,?,?,?)",
        (name, email, phone, full_address, total)
    )
    order_id = cur.lastrowid

    # Insert order items
    for item in cart.values():
        cur.execute(
            "INSERT INTO order_items (order_id, product_id, product_name, price, quantity, size) VALUES (?,?,?,?,?,?)",
            (order_id, item["product_id"], item["name"], item["price"], item["qty"], item["size"])
        )

    conn.commit()
    conn.close()

    # Clear cart
    session.pop("cart", None)
    flash(f"Order #{order_id} placed successfully! We'll contact you shortly.", "success")
    return redirect(url_for("order_success", order_id=order_id))


@app.route("/order/success/<int:order_id>")
def order_success(order_id):
    conn  = get_db()
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    conn.close()
    if not order:
        return redirect(url_for("index"))
    return render_template("order_success.html", order=order)


# ── FORMS ────────────────────────────────────────────────────────────────────

@app.route("/feedback", methods=["POST"])
def feedback():
    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not all([name, email, message]):
        flash("Please fill in all feedback fields.", "error")
        return redirect(url_for("index") + "#feedback")

    conn = get_db()
    conn.execute("INSERT INTO feedback (name, email, message) VALUES (?,?,?)", (name, email, message))
    conn.commit()
    conn.close()

    flash("Thank you for your feedback!", "success")
    return redirect(url_for("index") + "#feedback")


@app.route("/contact", methods=["POST"])
def contact():
    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip()
    phone   = request.form.get("phone", "").strip()
    message = request.form.get("message", "").strip()

    if not all([name, email, message]):
        flash("Please fill in all required contact fields.", "error")
        return redirect(url_for("index") + "#contact")

    conn = get_db()
    conn.execute("INSERT INTO contact (name, email, phone, message) VALUES (?,?,?,?)", (name, email, phone, message))
    conn.commit()
    conn.close()

    flash("Message received! We'll get back to you soon.", "success")
    return redirect(url_for("index") + "#contact")


# ── RUN 

if __name__ == "__main__":
    init_db()
    app.run(debug=True)