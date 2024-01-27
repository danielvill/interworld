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

#*
@app.route('/',methods=['GET','POST'])
def principal():
    return render_template('index.html')

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
#*Este es para mostrar a los clientes
@app.route('/tecnicos/cliente')
def cliente():
    cliente = db['cliente'].find()
    return render_template('tecnicos/cliente.html',cliente=cliente)    

#*Editar cliente
@app.route('/edit_cli/<string:client_nombre>', methods=['GET', 'POST'])
def edit_cli(client_nombre):
    cliente =db['cliente']
    user= request.form["user"]
    contraseña = request.form["contraseña"]
    correo= request.form["correo"]

    if user and contraseña and correo:
        cliente.update_one({'user':client_nombre},{'set':{'user':user,'contraseña':contraseña,"correo":correo}})
        return redirect(url_for('cliente'))
    else:
        return render_template('tecnicos/cliente.html')

#*Eliminar cliente
@app.route('/delete_cli/<string:client_nombre>')
def elitcl(client_nombre):
    cliente =db['cliente']
    cliente.delete_one({'user':client_nombre})
    return redirect(url_for('cliente'))


#*Vista de las citas de los clientes que agendaron 
#todo : este apartado tiene que enviar notificaciones a los correos de los tecnicos
@app.route('/tecnicos/vistagenda')
def vistagenda():
    agenda =db["agendar"]
    return render_template('tecnicos/vistagenda.html',agendar=agenda)
    

#*Agregar Tecnico
@app.route('/tecnicos/agtecnico', methods=['GET','POST'])
def agtecnico():
    if request.method == 'POST':
        tecnicos =db["admin"]
        user = request.form['user']
        contraseña = request.form['contraseña']
        correo = request.form['correo']
        if user and contraseña and correo:
            tecnicos= Admin(user, contraseña, correo)
            tecnicos.insert_one(tecnicos.AdminDBCollection())
            return redirect(url_for('agtecnico'))
    else:
        return render_template('tecnicos/agtecnico.html')



#*Vista de los tecnicos para editarlos
@app.route('/tecnicos/vistecni')
def vitecni():
    tecnicos =db["admin"].find()
    return render_template('tecnicos/vistecni.html',admin=tecnicos)


#*Edicion de los tecnicos
@app.route('/edit_tec/<string:tecnico>', methods=['GET', 'POST'])
def edit_tec(tecnico):
    tecnicos =db["admin"]
    user= request.form["user"]
    contraseña = request.form["contraseña"]
    correo= request.form["correo"]
    if user and contraseña and correo:
        tecnicos.update_one({'user':tecnico},{'set':{'user':user,'contraseña':contraseña,"correo":correo}})
        return redirect(url_for('vitecni'))
    else:
        return render_template('tecnicos/vistecni.html')

#* Eliminar Tecnicos
@app.route('/delete_tec/<string:tecnico>')
def delete_tec(tecnico):
    tecnicos =db["admin"]
    tecnicos.delete_one({'user':tecnico})
    return redirect(url_for('vistecni'))


#* lLenar los datos para enviar a vistacompleta osea reporte
@app.route('/tecnicos/vistenvi')
def vistenvi():
    enviar = db["agendar"].find()#todo: lo que tendrias que mostrar seria nombre,fecha,direccion,canton lo demas son input que debes agregar
    return render_template('tecnicos/vistenvi.html',enviar=enviar)

#*Apartado de enviar y eliminar los registros de agendar
@app.route('/tecnicos/vistenvi', methods=['GET', 'POST'])
def vistenvi2():
    if request.method == 'POST':
        enviar=db["reporte"]
        agendar=db["agendar"]
        codigo=request.form["codigo"]
        cliente=request.form["cliente"]
        fecha=request.form["fecha"]
        direccion=request.form["direccion"]
        canton=request.form["canton"]
        comentario=request.form["comentario"]
        estado=request.form["estado"]
        if codigo and cliente and fecha and direccion and canton and comentario and estado:
            enviar= Reporte(codigo,cliente, fecha, direccion, canton, comentario, estado)
            enviar.insert_one(enviar.ReporteDBCollection())
            # * Aquí eliminamos el documento de la colección "agendar"
            agendar.delete_one({'cliente': cliente, 'fecha': fecha, 'direccion': direccion, 'canton': canton})
            return redirect(url_for('vistaagenda'))
    else:
        return render_template('tecnicos/vistenvi.html')


#*Vista de los reportes que tiene es para visualizar todo lo que hay en ella
@app.route('/tecnicos/vistacompleta')
def vistacompleta():
    reporte=db['reporte'].find()
    return render_template('tecnicos/vistacompleta.html',reporte=reporte)


#* ------------- Modulo Cliente -----------------------------------

@app.route('/clientes/agenda', methods=['GET', 'POST'])
def agenda():
    if request.method == 'POST':
        agenda =db["agendar"]
        codigo=request.form["codigo"]
        cliente=request.form["cliente"]
        hora=request.form["hora"]
        fecha=request.form["fecha"]
        direccion=request.form["direccion"]
        canton=request.form["canton"]
        comentario=request.form["comentario"]
        estado=request.form["estado"]
        if codigo and cliente and hora  and fecha and direccion and canton and comentario and estado:
            agenda= Agendar(codigo,cliente, hora,fecha, direccion, canton, comentario, estado)
            agenda.insert_one(agenda.AgendarDBCollection())
            return redirect(url_for('agenda'))
    else:
        return render_template('clientes/agenda.html')

        

@app.route('/clientes/vistaagenda')
def vistaagenda():
    agenda =db["agendar"]
    return render_template('clientes/vistaagenda.html',agendar=agenda)



if __name__ == '__main__':
    app.run(debug=True, port=5000)