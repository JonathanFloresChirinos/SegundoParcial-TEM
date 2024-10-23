from flask import Flask,render_template,redirect,session,url_for,request

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'

def id():
    if 'gestion' in session and len(session['gestion']) > 0:
        return max(indice['id'] for indice in session['gestion']) + 1
    else:
        return 1

@app.route("/")
def index():
    if 'gestion' not in session:
        session['gestion'] = []

    productos = session.get('gestion',[])
    return render_template('index.html',productos=productos)

@app.route("/nuevo", methods=['GET','POST'])
def nuevo():
    if request.method == 'POST':
        
        nombre = request.form["nombre"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]
        fechaven = request.form["fechaven"]
        categoria = request.form["categoria"]

        nuevoProducto = {
            'id':id(),
            'nombre':nombre,
            'cantidad':cantidad,
            'precio':precio,
            'fechaven':fechaven,
            'categoria':categoria
        }

        if 'gestion' not in session:
            session['gestion'] = []

        session['gestion'].append(nuevoProducto)
        session.modified = True
        return redirect(url_for('index'))

    return render_template('nuevo.html')

@app.route("/editar/<int:id>",methods=['GET','POST'])
def editar(id):
    productos = session.get('gestion',[])
    producto = next((prod for prod in productos if prod['id'] == id), None)
    if not producto:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = request.form['cantidad']
        producto['precio'] = request.form['precio']
        producto['fechaven'] = request.form['fechaven']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('editar.html',producto=producto)
    
@app.route("/elimina/<int:id>", methods=['POST'])
def elimina(id):
    productos = session.get('gestion',[])
    producto = next((prod for prod in productos if prod['id'] == id),None)
    if producto:
        session['gestion'].remove(producto)
        session.modified = True
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)