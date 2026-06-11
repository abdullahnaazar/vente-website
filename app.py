from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "vente_secret_key_2026"

PRODUCTS = [
    {"id": 1,  "name": "Classic Black Hoodie",    "price": 3599, "category": "Hoodies",   "size": "S,M,L,XL,XXL", "stock": 30, "image_url": "https://pk-live-21.slatic.net/kf/Sd263403da536434f8e305c1f47667b42j.jpg"},
    {"id": 2,  "name": "Green & White Combo",     "price": 3999, "category": "Sets",      "size": "S,M,L,XL",     "stock": 20, "image_url": "https://assets.ajio.com/medias/sys_master/root/20231006/uGY7/65200a08afa4cf41f52e0fd0/-473Wx593H-466679697-green-MODEL.jpg"},
    {"id": 3,  "name": "Blue White Shade Hoodie", "price": 2999, "category": "Hoodies",   "size": "S,M,L,XL,XXL", "stock": 25, "image_url": "https://ae-pic-a1.aliexpress-media.com/kf/Sff361cba0fd44c0bb449b088d921ce9fs.jpg"},
    {"id": 4,  "name": "Classic Women's Outfit",  "price": 4999, "category": "Sets",      "size": "S,M,L,XL",     "stock": 15, "image_url": "https://i.pinimg.com/236x/88/02/03/88020364137ab869a02319c3b3bcc7a9.jpg"},
    {"id": 5,  "name": "Simple White Hoodie",     "price": 3599, "category": "Hoodies",   "size": "S,M,L,XL,XXL", "stock": 40, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlubZU2IGyWo7U9POdfIDxIv7oDmTqC8K8Ww&s"},
    {"id": 6,  "name": "White Hoodie for Girls",  "price": 4999, "category": "Hoodies",   "size": "S,M,L,XL",     "stock": 18, "image_url": "https://pk-live-21.slatic.net/kf/Sd87bae498388405a9d34105633c43423n.jpg"},
    {"id": 7,  "name": "Modern Shirt",            "price": 3500, "category": "Shirts",    "size": "S,M,L,XL",     "stock": 35, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRixijHdx70vXWp3Hxy4_1iO1hCD3PBT97zlg&s"},
    {"id": 8,  "name": "Hoodie for Girls",        "price": 3699, "category": "Hoodies",   "size": "S,M,L,XL",     "stock": 22, "image_url": "https://rukmini1.flixcart.com/image/1500/1500/xif0q/sweatshirt/v/o/i/l-newlyshweatshirt21-draxstar-original-imahhe9mubsqwxdv.jpeg?q=70"},
    {"id": 9,  "name": "Brown Polo Neck Shirt",   "price": 2999, "category": "Shirts",    "size": "S,M,L,XL",     "stock": 30, "image_url": "https://5.imimg.com/data5/SELLER/Default/2026/2/583757184/MG/GU/RD/38646945/polo-neck-printed-t-shirts-220-gsm.jpg"},
    {"id": 10, "name": "Simple Brown T-Shirt",    "price": 3299, "category": "T-Shirts",  "size": "S,M,L,XL",     "stock": 50, "image_url": "https://xcdn.next.co.uk/common/items/default/default/itemimages/3_4Ratio/product/lge/Y16812s13.jpg?im=Resize,width=750"},
    {"id": 11, "name": "Plain Black Shirt",       "price": 2799, "category": "Shirts",    "size": "S,M,L,XL",     "stock": 45, "image_url": "https://bluestoneclothing.pk/cdn/shop/files/Black_91aabf0b-386d-4837-8808-865948468104_1200x.jpg?v=1751530847"},
    {"id": 12, "name": "Plain Blue Shirt",        "price": 2999, "category": "Shirts",    "size": "S,M,L,XL",     "stock": 38, "image_url": "https://xcdn.next.co.uk/common/items/default/default/itemimages/3_4Ratio/product/lge/F90841s5.jpg"},
    {"id": 13, "name": "Pink Top with Blue Pant", "price": 4599, "category": "Sets",      "size": "S,M,L,XL",     "stock": 12, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2xeEyTMbXjaC9nE0SgNw7L2nwY8uJg5OmYw&s"},
    {"id": 14, "name": "White Classic Top",       "price": 3199, "category": "T-Shirts",  "size": "S,M,L,XL",     "stock": 28, "image_url": "https://shopmicas.com/cdn/shop/files/b2dd2bb8-a505-4b87-9524-dc2c80873b94_1024x1024.jpg?v=1777453557"},
    {"id": 15, "name": "Blue Hoodie for Women",   "price": 3799, "category": "Hoodies",   "size": "S,M,L,XL",     "stock": 20, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtZZQOoC1Bc3PO5paR_thJWDThnD_JgOiMew&s"},
    {"id": 16, "name": "Premium Pleated Palazzo", "price": 3399, "category": "Bottoms",   "size": "S,M,L,XL",     "stock": 17, "image_url": "https://i.pinimg.com/474x/fb/0a/8f/fb0a8f25259e884e0a72c4fc7f55ae73.jpg"},
    {"id": 17, "name": "Top for Women",           "price": 3700, "category": "T-Shirts",  "size": "S,M,L,XL",     "stock": 25, "image_url": "https://i.pinimg.com/236x/38/a5/49/38a5495e95aa8285e4e977bae6a2ebe4.jpg"},
    {"id": 18, "name": "Plain Green Hoodie",      "price": 2999, "category": "Hoodies",   "size": "S,M,L,XL,XXL", "stock": 33, "image_url": "https://renebassett.com/cdn/shop/files/SweatVerde1_2385ae39-abd7-4af6-9625-e19d7f17a6e7.jpg?v=1698157010"},
    {"id": 19, "name": "Green White Jacket",      "price": 4200, "category": "Outerwear", "size": "S,M,L,XL",     "stock": 10, "image_url": "https://i.pinimg.com/736x/58/0a/0e/580a0e916a2db478e08ea549da42426f.jpg"},
    {"id": 20, "name": "Crop Top & Wide Leg",     "price": 4299, "category": "Sets",      "size": "S,M,L,XL",     "stock": 14, "image_url": "https://i.pinimg.com/236x/9f/e4/14/9fe414097a72d47a1473582b72a2153e.jpg"},
]

# ── CART HELPERS

def get_cart():
    return session.get("cart", {})

def cart_count():
    return sum(item["qty"] for item in get_cart().values())

def cart_total():
    return sum(item["price"] * item["qty"] for item in get_cart().values())

app.jinja_env.globals["cart_count"] = cart_count

# ── PAGES

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products():
    category = request.args.get("category", "")
    all_categories = sorted(set(p["category"] for p in PRODUCTS))

    if category:
        filtered = [p for p in PRODUCTS if p["category"] == category]
    else:
        filtered = PRODUCTS

    return render_template("products.html", products=filtered, categories=all_categories, active_cat=category)

@app.route("/cart")
def cart():
    return render_template("cart.html", cart=get_cart(), total=cart_total())

@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)

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

    session.pop("cart", None)
    flash(f"Order placed successfully! We'll contact you on {phone} shortly.", "success")
    return redirect(url_for("index"))

@app.route("/feedback", methods=["POST"])
def feedback():
    flash("Thank you for your feedback!", "success")
    return redirect(url_for("index") + "#feedback")

@app.route("/contact", methods=["POST"])
def contact():
    flash("Message received! We'll get back to you soon.", "success")
    return redirect(url_for("index") + "#contact")

if __name__ == "__main__":
    app.run(debug=True)