from flask import flash, Flask, render_template, request,Response ,jsonify, redirect, url_for
from controllers.database import Conexion as dbase
from modules.admin import Admin
from modules.agendar import Agendar
from modules.cliente import Cliente
from modules.recuperacion import Recuperacion
from modules.reporte import Reporte

#! Tener Better comments para ver las mejoras en los comentarios

db = dbase()

app = Flask(__name__)
app.secret_key = 'interworld'

#* ------------- Modulo De Ingreso registro y recuperacion -----------------------------------


@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        user = request.form['user']
        contraseña = request.form['contraseña']
        user = db.admin.find_one({"user":user, "contraseña":contraseña})
        user2 = db.cliente.find_one({"user":user,"contraseña":contraseña})
        if user:
            return redirect(url_for('cliente'))
        elif user2:
            return redirect(url_for('agenda'))     #TODO: No te olvides de agregar que solo tiene 5 oportunidades de agregar usuario o contraseña sino se bloquea la pagina
        else:
            flash("Usuario o contraseña incorrectos")
            return redirect(url_for('index'))
    else:
        return render_template('index.html')    


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        registrar = db["cliente"]
        user = request.form['user']
        contraseña = request.form['contraseña'] 
        correo = request.form['correo']
# todo: Manda un mensaje que se guardo el cliente con exito con javascripts
        if user and contraseña and correo:
            registra= Cliente(user, contraseña, correo)
            registrar.insert_one(registra.ClienDBCollection())
            return redirect(url_for('index'))
    else:
        return render_template('login.html')    



@app.route('/recuperacion',methods=['GET','POST'])
def recuperacion():
    if request.method == 'POST':
        recu =db["recuperacion"]
        user = request.form['user']
        correo =request.form['correo']
        if user and correo:  # todo: No te olvides de enviar un mensaje de que sepa la persona que va a recibir un correo para la recuperacion 
            recu= Recuperacion(user, correo)
            recu.insert_one(recu.RecuDBCollection())
            return redirect(url_for('index'))
    else:
        return render_template('recuperacion.html')    


# * ------------- Modulo Tecnico -----------------------------------



@app.route('/tecnicos/cliente')
def cliente():
    return render_template('tecnicos/cliente.html')    


@app.route('/tecnicos/vistagenda')
def vistagenda():
    return render_template('tecnicos/vistagenda.html')    

@app.route('/tecnicos/agtecnico')
def agtecnico():
    return render_template('tecnicos/agtecnico.html')

@app.route('/tecnicos/vitecni')
def vitecni():
    return render_template('tecnicos/vitecni.html')

@app.route('/tecnicos/vistenvi')
def vistenvi():
    return render_template('tecnicos/vistenvi.html')

@app.route('/tecnicos/vistacompleta')
def vistacompleta():
    return render_template('tecnicos/vistacompleta.html')


#* ------------- Modulo Cliente -----------------------------------

@app.route('/clientes/agenda')
def agenda():
    return render_template('clientes/agenda.html')    

@app.route('/clientes/vistaagenda')
def vistaagenda():
    return render_template('clientes/vistaagenda.html')



if __name__ == '__main__':
    app.run(debug=True, port=5000)