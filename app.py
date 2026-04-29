from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secreto_super_seguro"

def calcular_totales(carrito):
    total = 0
    for item in carrito:
        item['subtotal'] = item['precio'] * item['cantidad']
        total += item['subtotal']
    return total

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    cantidad = int(request.form['cantidad'])

    if 'carrito' not in session:
        session['carrito'] = []

    carrito = session['carrito']

    for item in carrito:
        if item['nombre'] == nombre:
            item['cantidad'] += cantidad
            break
    else:
        carrito.append({
            'nombre': nombre,
            'precio': precio,
            'cantidad': cantidad
        })

    session['carrito'] = carrito
    return redirect(url_for('ver_carrito'))

@app.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', [])
    total = calcular_totales(carrito)
    session['carrito'] = carrito
    return render_template('carrito.html', carrito=carrito, total=total)

@app.route('/eliminar/<int:index>')
def eliminar(index):
    carrito = session.get('carrito', [])
    if 0 <= index < len(carrito):
        carrito.pop(index)
    session['carrito'] = carrito
    return redirect(url_for('ver_carrito'))

@app.route('/vaciar')
def vaciar():
    session.pop('carrito', None)
    return redirect(url_for('ver_carrito'))

if __name__ == '__main__':
    app.run(debug=True)