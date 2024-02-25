from flask import flash, Flask,session, render_template, request,Response ,jsonify, redirect, url_for
from controllers.database import Conexion as dbase
from modules.admin import Admin
from modules.agendar import Agendar
from modules.cliente import Cliente
from modules.recuperacion import Recuperacion
from modules.reporte import Reporte
from modules.estado import Estado
from datetime import datetime,timedelta
from flask_mail import Mail, Message #todo : Intalar pip install flask-mail
#! Tener Better comments para ver las mejoras en los comentarios

db = dbase()
app = Flask(__name__)
app.secret_key = 'interworld'


#*Esta parte del codigo lo que hace es que se pone un correo principal el cual recibe todo y este se encarga de enviar a los demas tenicos
app.config['MAIL_SERVER'] = 'smtp.office365.com'  # Servidor SMTP de Outlook
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'ejemplo@hotmail.com'  # Tu correo de Outlook
app.config['MAIL_PASSWORD'] = '123' # La contraseña de tu correo de Outlook
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
#* Esta parte termina el codigo de lo que es el correo




#* ------------- Modulo De Ingreso registro y recuperacion -----------------------------------

@app.route('/',methods=['GET','POST'])
def principal():
    return render_template('index.html')

@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        username = request.form['user']
        contraseña = request.form['contraseña']
        user_admin = db.admin.find_one({"user":username, "contraseña":contraseña})
        user_cliente = db.cliente.find_one({"user":username,"contraseña":contraseña})
        if user_admin:
            session['user'] = username
            return redirect(url_for('cliente'))
        elif user_cliente:
            session['user'] = username
            return redirect(url_for('agenda',user=username)) #TODO: No te olvides de agregar que solo tiene 5 oportunidades de agregar usuario o contraseña sino se bloquea la pagina
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

        if user and contraseña and correo:

            # Verificar si el usuario ya existe
            if registrar.find_one({"user": user}):
                # Si el usuario ya existe, mostrar un mensaje de error
                flash("El usuario ya existe ingrese nuevo usuario")
                return redirect(url_for('login'))
            
            # Verificar si el correo ya existe
            elif registrar.find_one({"correo": correo}):
                # Si el correo ya existe, mostrar un mensaje de error
                flash("El correo ya existe ingresa otro correo para registrarlo")
                return redirect(url_for('login'))
            else:
                # Si el usuario no existe, proceder con el registro
                registra= Cliente(user, contraseña, correo)
                registrar.insert_one(registra.ClienDBCollection())
                return redirect(url_for('index'))
    else:
        return render_template('login.html')    



@app.route('/recuperacion',methods=['GET','POST'])
def recuperacion():
    if request.method == 'POST':
        clie = db ['cliente']
        recu =db["recuperacion"]
        user = request.form['user']
        correo =request.form['correo']
        if user and correo:
            # todo: No te olvides de enviar un mensaje de que sepa la persona que va a recibir un correo para la recuperacion 
            #Verificar si el usuario o correo ya se registraron
            if not clie.find_one({'user':user}):
                flash("El Usuario no existe profavor ingrese nombre de usuario correcto")
                return redirect(url_for('index'))
            elif recu.find_one({'user':user}):
                flash("El usuario ya se registro espere a que se le envie un correo para que se le notifique de su recuperacion de clave")
                return redirect(url_for('index'))
            else:
                recupe= Recuperacion(user, correo)
                recu.insert_one(recupe.RecuDBCollection())
                flash("Gracias por enviar tus datos muy pronto recibiras un mensaje a tu correo para que puedas ingresar de nuevo con tus credenciales actualizadas ")
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
def editcli(client_nombre):
    cliente =db['cliente']
    user= request.form["user"]
    contraseña = request.form["contraseña"]
    correo= request.form["correo"]

    if user and contraseña and correo:
        cliente.update_one({'user':client_nombre},{'$set':{'user':user,'contraseña':contraseña,"correo":correo}})
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
    agenda =db["agendar"].find().sort("fecha",-1).limit(5)
    return render_template('tecnicos/vistagenda.html',agendar=agenda)



#* Enviar de agenda a estado
@app.route('/tecnicos/vistagenda', methods=['GET','POST'])
def envitagenda():
    if request.method == 'POST':
        envi =db['estado']
        codigo = request.form['codigo']
        cliente = request.form['cliente']
        fecha = request.form['fecha']
        direccion = request.form['direccion']
        canton = request.form['canton']
        if codigo and cliente and fecha and direccion and canton :
            envia= Estado(codigo,cliente,fecha,direccion,canton)
            envi.insert_one(envia.EsDBCollection())

            return redirect(url_for('vistenvi2'))
    else:
        return render_template('tecnicos/vistagenda.html')

# * Eliminar de Agenda
@app.route('/delete_age/<string:age_name>')
def elitage(age_name):
    agenda =db['agendar']
    agenda.delete_one({'codigo':age_name})
    return redirect(url_for('envitagenda'))   


#*Agregar Tecnico
@app.route('/tecnicos/agtecnico', methods=['GET','POST'])
def agtecnico():
    if request.method == 'POST':
        tecnicos =db["admin"]
        user = request.form['user']
        contraseña = request.form['contraseña']
        correo = request.form['correo']
        if user and contraseña and correo:
            tecnico = Admin(user, contraseña, correo)
            tecnicos.insert_one(tecnico.AdminDBCollection())
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
        tecnicos.update_one({'user':tecnico},{'$set':{'user':user,'contraseña':contraseña,"correo":correo}})
        return redirect(url_for('vitecni'))
    else:
        return render_template('tecnicos/vistecni.html')

#* Eliminar Tecnicos
@app.route('/delete_tec/<string:tecnico>')
def delete_tec(tecnico):
    tecnicos =db["admin"]
    tecnicos.delete_one({'user':tecnico})
    return redirect(url_for('vitecni'))


#*Apartado de enviar y eliminar los registros de agendar
@app.route('/tecnicos/vistenvi', methods=['GET', 'POST'])
def vistenvi2():
    if request.method == 'POST':
        enviar=db["reporte"]
        agendar=db["agendar"]
        estador=db["estado"]
        codigo=request.form["codigo"]
        cliente=request.form["cliente"]
        fecha=request.form["fecha"]
        direccion=request.form["direccion"]
        canton=request.form["canton"]
        comentario=request.form["comentario"]
        estado=request.form["estado"]
        if codigo and cliente and fecha and direccion and canton and comentario and estado:
            enviare= Reporte(codigo,cliente, fecha, direccion, canton, comentario, estado)
            enviar.insert_one(enviare.RepoDBCollection())
            # * Aquí eliminamos el documento de la colección "agendar"
            agendar.delete_one({'cliente': cliente, 'fecha': fecha, 'direccion': direccion, 'canton': canton})
            estador.delete_one({'cliente': cliente, 'fecha': fecha, 'direccion': direccion, 'canton': canton})
            return redirect(url_for('vistacompleta'))
    else:
        estado=db['estado'].find()
        return render_template('tecnicos/vistenvi.html',estado=estado)


#*Vista de los reportes que tiene es para visualizar todo lo que hay en ella
@app.route('/tecnicos/vistacompleta')
def vistacompleta():
    reporte=db['reporte'].find()
    return render_template('tecnicos/vistacompleta.html',reporte=reporte)


#* Tecnico Recuperacion 
@app.route('/tecnicos/vistarecu')
def vistarecu():
    recuperacion=db['recuperacion'].find()
    return render_template('tecnicos/vistarecu.html',recuperacion=recuperacion)


# * Tecnico  Eliminar Recuperacion

#* Eliminar Tecnicos
@app.route('/delete_rec/<string:recuperacion>')
def delete_rec(recuperacion):
    recu =db["recuperacion"]
    recu.delete_one({'user':recuperacion})
    return redirect(url_for('vistarecu'))




#* ------------- Modulo Cliente -----------------------------------

@app.route('/clientes/agenda', methods=['GET', 'POST'])
def agenda():     
    if 'user' in session:
        if request.method == 'POST':
            agenda =db["agendar"]
            codigo=request.form["codigo"]
            cliente=request.form["cliente"]
            hora=request.form["hora"]
            fecha=request.form["fecha"]
            telefono=request.form["telefono"]
            direccion=request.form["direccion"]
            canton=request.form["canton"]
            estado=request.form["estado"]
            #if codigo and cliente and hora  and fecha and telefono and direccion and canton and  estado:
            #    agend= Agendar(codigo,cliente, hora,fecha, telefono,direccion, canton,  estado)
            #    agenda.insert_one(agend.AgeDBCollection())
                
    
    
            # Obtiene la fecha y hora actual
            fecha_actual = datetime.now()
            fecha_str = fecha_actual.strftime("%Y-%m-%d")  # Convierte la fecha a una cadena de texto
            # Verifica si el cliente ya tiene dos ingresos en la fecha actual
            if agenda.count_documents({'cliente': cliente, 'fecha': fecha_str}) < 2:
                agend = Agendar(codigo, cliente, hora, fecha, telefono, direccion, canton, estado)
                agenda.insert_one(agend.AgeDBCollection())
                return redirect(url_for('agenda'))
                
            #Obtén la colección 'admin'
            admin = db["admin"]

            #Busca todos los documentos en la colección 'admin'
            docs = admin.find({})

            for doc in docs:
            # Comprueba si el documento tiene un campo 'correo'
                if 'correo' in doc:
                    tecnico_email = doc['correo']

                    # Envía la notificación por correo electrónico
                    msg = Message('Nueva Agenda Registrada', sender='ejemplo@hotmail.com', recipients=[tecnico_email])
                    msg.body = f'Se ha registrado una nueva agenda con el código {codigo} para el cliente {cliente}.'
                    mail.send(msg)
                
            else:
                # Aquí puedes manejar el caso cuando el cliente ya tiene dos ingresos.
                # Por ejemplo, puedes mostrar un mensaje de error.
                mensaje ="Ingresastes dos citas este dia regresa mañana para que registres otro dia"
                flash(mensaje)
                return  redirect(url_for('agenda'))
        else:
            return render_template('clientes/agenda.html',user=session['user'])
    else:
        return render_template('clientes/agenda.html')

@app.route('/clientes/vistaagenda')
def vistaagenda():
    agenda = db["agendar"].find().sort("fecha", -1).limit(5)#*Muestra los registros de forma descendente y solo muestra 5 registros
    return render_template('clientes/vistaagenda.html', agendar=agenda)



if __name__ == '__main__':
    app.run(debug=True, port=5000)