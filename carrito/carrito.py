class Carrito:

    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get("carrito")

        # Si el carrito es una lista (formato viejo) o no existe, lo reinicia
        if not carrito or not isinstance(carrito, dict):
            carrito = self.session["carrito"] = {}

        self.carrito = carrito

    def guardar(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def agregar(self, producto):
        id = str(producto.id)
        if id not in self.carrito:
            self.carrito[id] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "precio": float(producto.precio),
                "cantidad": 1,
                "imagen": producto.imagen.url if producto.imagen else "",
            }
        else:
            self.carrito[id]["cantidad"] += 1
        self.guardar()

    def restar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            if self.carrito[id]["cantidad"] > 1:
                self.carrito[id]["cantidad"] -= 1
            else:
                del self.carrito[id]
        self.guardar()

    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
        self.guardar()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

    def total(self):
        return sum(
            item["precio"] * item["cantidad"]
            for item in self.carrito.values()
        )

    def total_items(self):
        return sum(item["cantidad"] for item in self.carrito.values())

    def __iter__(self):
        for item in self.carrito.values():
            item["subtotal"] = item["precio"] * item["cantidad"]
            yield item