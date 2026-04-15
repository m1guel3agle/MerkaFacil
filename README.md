# MerkaFacil
A simple e-commerce platform for neighborhood stores. It allows customers to browse products and build a shopping cart before visiting the store or requesting home delivery, reducing the workload for employees.

## Technologies
- **Python 3.13**
- **Django 5.2.7**
- **SQLite** — local database
- **HTML**
- **Bootstrap** — styles and UI components

## Features
- Product catalog with images, price and stock
- Session-based shopping cart
- User registration and login
- Admin panel to manage products and store configuration
- Open/closed store status

## How to run

**1. Clone the repository**
```bash
git clone https://github.com/m1guel3agle/MerkaFacil.git
cd MerkaFacil
```

**2. Install dependencies**
```bash
pip install django pillow
```

**3. Create a superuser for the admin panel**
```bash
python manage.py createsuperuser
```

**4. Run the server**
```bash
python manage.py runserver
```

**5. Open in your browser**
```
http://127.0.0.1:8000/
```

The admin panel is available at `http://127.0.0.1:8000/admin/`

**Project structure**
```
MerkaFacil/
├── Merkafacil/                     # Configuración principal del proyecto
│   ├── settings.py                 # Base de datos, apps, media, auth
│   ├── urls.py                     # Enrutador principal
│   ├── wsgi.py
│   └── asgi.py
│
├── core/                           # App: autenticación y páginas generales
│   ├── templates/
│   │   ├── base.html               # Navbar + layout base
│   │   ├── home.html               # Página principal
│   │   ├── login.html              # Inicio de sesión
│   │   ├── signup.html             # Registro de usuario
│   │   ├── about.html              # Acerca de nosotros
│   │   └── productos.html          # Catálogo (aviso tienda abierta/cerrada)
│   ├── models.py                   # ConfigTienda (estado abierta/cerrada)
│   ├── views.py                    # home, about, login, logout, signup
│   ├── urls.py
│   ├── admin.py                    # Registro de ConfigTienda
│   └── migrations/
│
├── products/                       # App: catálogo de productos
│   ├── models.py                   # Producto (nombre, precio, stock, imagen)
│   ├── views.py                    # catalogo
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
│
├── carrito/                        # App: carrito de compras por sesión
│   ├── templates/carrito/
│   │   └── carrito.html            # Vista del carrito
│   ├── carrito.py                  # Clase Carrito (agregar, eliminar, guardar)
│   ├── views.py                    # agregar_producto, ver_carrito
│   ├── urls.py
│   └── migrations/
│
├── media/
│   └── productos/                  # Imágenes subidas desde el admin
│
├── manage.py
└── db.sqlite3
```
