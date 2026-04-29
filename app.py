from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secreto"

# Catálogo de productos
productos = [
    {"id": 1, "nombre": "Laptop", "precio": 800},
    {"id": 2, "nombre": "Mouse", "precio": 20},
    {"id": 3, "nombre": "Teclado", "precio": 50},
    {"id": 4, "nombre": "Monitor", "precio": 200},
]

@app.route('/')
def index():
    return render_template('index.html', productos=productos)

@app.route('/adicionar/<int:id>')
def adicionar(id):
    if 'carrito' not in session:
        session['carrito'] = []

    # Buscar producto por id
    producto = next((p for p in productos if p["id"] == id), None)

    if producto:
        session['carrito'].append(producto)
        session.modified = True

    return redirect('/carrito')

@app.route('/carrito')
def carrito():
    if 'carrito' not in session:
        session['carrito'] = []

    total = sum(p["precio"] for p in session['carrito'])

    return render_template('adicionar.html', carrito=session['carrito'], total=total)

@app.route('/eliminar/<int:index>')
def eliminar(index):
    if 'carrito' in session:
        try:
            session['carrito'].pop(index)
            session.modified = True
        except:
            pass

    return redirect('/carrito')

if __name__ == '__main__':
    app.run(debug=True)