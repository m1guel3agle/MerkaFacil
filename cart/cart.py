class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")

        # If cart is a list (old format) or doesn't exist, reset it
        if not cart or not isinstance(cart, dict):
            cart = self.session["cart"] = {}

        self.cart = cart

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True

    def add(self, product):
        pid = str(product.id)
        if pid not in self.cart:
            self.cart[pid] = {
                "product_id": product.id,
                "name": product.name,
                "price": float(product.price),
                "quantity": 1,
                "image": product.image.url if product.image else "",
            }
        else:
            self.cart[pid]["quantity"] += 1
        self.save()

    def remove_one(self, product):
        pid = str(product.id)
        if pid in self.cart:
            if self.cart[pid]["quantity"] > 1:
                self.cart[pid]["quantity"] -= 1
            else:
                del self.cart[pid]
        self.save()

    def remove(self, product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
        self.save()

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True

    def total(self):
        return sum(
            item["price"] * item["quantity"]
            for item in self.cart.values()
        )

    def total_items(self):
        return sum(item["quantity"] for item in self.cart.values())

    def __iter__(self):
        for item in self.cart.values():
            item["subtotal"] = item["price"] * item["quantity"]
            yield item