class Carrito:

    def __init__(self, request):
        self.request = request
        self.session = request.session

        carrito = self.session.get("carrito")

        if not carrito:
            carrito = self.session["carrito"] = {}

        self.carrito = carrito


    def agregar(self, producto):
        id = str(producto.id)

        if id not in self.carrito:
            self.carrito[id] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "precio": float(producto.precio),
                "cantidad": 1
            }
        else:
            self.carrito[id]["cantidad"] += 1

        self.guardar()


    def guardar(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True


    def eliminar(self, producto):
        id = str(producto.id)

        if id in self.carrito:
            del self.carrito[id]
            self.guardar()