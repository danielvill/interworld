from flask import flash, Flask, send_file,session, render_template, request,Response ,jsonify, redirect, url_for
from bson import json_util
from controllers.database import Conexion as dbase
from modules.admin import Admin
from modules.agendar import Agendar
from modules.cliente import Cliente
from modules.recuperacion import Recuperacion
from modules.reporte import Reporte
from modules.estado import Estado
from modules.tecnico import Tecnico
from datetime import datetime,timedelta
from flask_mail import Mail, Message #todo:Instalar pip install flask-mail
from flask import jsonify
from reportlab.pdfgen import canvas # *pip install reportlab
from reportlab.lib.pagesizes import letter #* pip install reportlab 
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer ,Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet ,ParagraphStyle

#! Tener Better comments para ver las mejoras en los comentarios

db = dbase()
app = Flask(__name__)
app.secret_key = 'interworld'


#*Esta parte del codigo lo que hace es que se pone un correo principal el cual recibe todo y este se encarga de enviar a los demas tenicos
app.config['MAIL_SERVER'] = 'smtp.office365.com'  # Servidor SMTP de Outlook
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'popeye198733@hotmail.com'  # Tu correo de Outlook
app.config['MAIL_PASSWORD'] = 'grumete31' # La contraseña de tu correo de Outlook
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
#* Esta parte termina el codigo de lo que es el correo


#* ------------- Modulo De Ingreso registro y recuperacion -----------------------------------

@app.route('/logout')
def logout():
    # Elimina el usuario de la sesión si está presente
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/tecnicos/home',methods=['GET','POST'])
def home():
    # Verifica si el usuario está en la sesión
    if 'username' in session:
        return render_template('tecnicos/home.html')
    else:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))

@app.route('/',methods=['GET','POST'])
def principal():
    return render_template('index.html')

@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        username = request.form['user']
        contraseña = request.form['contraseña']
        user_admin = db.admin.find_one({"user":username, "contraseña":contraseña})
        user_tecnico = db.tecnico.find_one({"user":username, "contraseña":contraseña})
        user_cliente = db.cliente.find_one({"user":username,"contraseña":contraseña})
        if user_admin:
            session["username"]= user_admin["user"]
            return redirect(url_for('home'))
        elif user_tecnico:
            session["username"]= user_tecnico["user"]
            session['user'] = username
            return redirect(url_for('home3'))
        elif user_cliente:
            session["username"]= user_cliente["user"]
            session['user'] = username
            return redirect(url_for('casa',user=username)) #TODO: No te olvides de agregar que solo tiene 5 oportunidades de agregar usuario o contraseña sino se bloquea la pagina
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
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))    
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
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    agenda =db["agendar"].find().sort("fecha",-1).limit(5)
    return render_template('tecnicos/vistagenda.html',agendar=agenda)



#* Enviar de agenda a estado
@app.route('/tecnicos/vistagenda', methods=['GET','POST'])
def envitagenda():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    if request.method == 'POST':
        envi =db['estado']
        tecnico = request.form['tecnico']
        cliente = request.form['cliente']
        fecha = request.form['fecha']
        direccion = request.form['direccion']
        canton = request.form['canton']
        if tecnico and cliente and fecha and direccion and canton :
            envia= Estado(tecnico,cliente,fecha,direccion,canton)
            envi.insert_one(envia.EsDBCollection())
            
            flash("Se envió al técnico correspondiente.")
            return redirect(url_for('envitagenda'))
    else:
        return render_template('tecnicos/vistagenda.html')

# * Eliminar de Agenda
@app.route('/delete_age/<string:age_name>')
def elitage(age_name):
    agenda =db['agendar']
    agenda.delete_one({'tecnico':age_name})
    return redirect(url_for('envitagenda'))   


#*Agregar Tecnico
@app.route('/tecnicos/agtecnico', methods=['GET','POST'])
def agtecnico():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        tecnicos =db["tecnico"]
        user = request.form['user']
        contraseña = request.form['contraseña']
        correo = request.form['correo']
        
        
        if user  and correo:
            existing_tecnico = tecnicos.find_one({"user": user,"correo": correo})
        
        if existing_tecnico is None:
            tecnico = Tecnico(user, contraseña, correo)
            tecnicos.insert_one(tecnico.TecniDBCollection())
            return redirect(url_for('agtecnico'))
        else:
            # Si existe, muestra un mensaje de error
            flash("Ya existe un Tecnicos con esos datos ingresa otros datos nuevos.")
            return render_template('tecnicos/agtecnico.html')
    else:
        return render_template('tecnicos/agtecnico.html')


#*Vista de los tecnicos para editarlos
@app.route('/tecnicos/vistecni')
def vitecni():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    tecnicos =db["tecnico"].find()
    return render_template('tecnicos/vistecni.html',tecnico=tecnicos)


#*Edicion de los tecnicos
@app.route('/edit_tec/<string:tecnico>', methods=['GET', 'POST'])
def edit_tec(tecnico):
    tecnicos =db["tecnico"]
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
    tecnicos =db["tecnico"]
    tecnicos.delete_one({'user':tecnico})
    return redirect(url_for('vitecni'))


#*Apartado de enviar y eliminar los registros de agendar
@app.route('/tecnicos/vistenvi', methods=['GET', 'POST'])
def vistenvi2():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    if request.method == 'POST':
        enviar=db["reporte"]
        estador=db["estado"]
        tecnico=request.form["tecnico"]
        cliente=request.form["cliente"]
        fecha=request.form["fecha"]
        direccion=request.form["direccion"]
        canton=request.form["canton"]
        comentario=request.form["comentario"]
        estado=request.form["estado"]
        if tecnico and cliente and fecha and direccion and canton and comentario and estado:
            enviare= Reporte(tecnico,cliente, fecha, direccion, canton, comentario, estado)
            enviar.insert_one(enviare.RepoDBCollection())
            # * Aquí eliminamos el documento de la colección "agendar"
            estador.delete_one({'cliente': cliente, 'fecha': fecha, 'direccion': direccion, 'canton': canton})
            return redirect(url_for('vistacompleta'))
    else:
        estado=db['estado'].find()
        return render_template('tecnicos/vistenvi.html',estado=estado)


#*Vista de los reportes que tiene es para visualizar todo lo que hay en ella
@app.route('/tecnicos/vistacompleta')
def vistacompleta():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    reporte=db['reporte'].find()
    return render_template('tecnicos/vistacompleta.html',reporte=reporte)


# * Para sacar pdf de lo que es vistacompleta

def generar_pdf_vistacompleta(datos):
    doc = SimpleDocTemplate("reporte.pdf", pagesize=letter)
    story = []

    # Define un estilo con texto centrado
    styles = getSampleStyleSheet()
    left_aligned_style = styles['Heading3']
    left_aligned_style.alignment = 0  # 0 = TA_LEFT


    
    # Agrega la imagen
    imagen = Image('static/img/inter.png', width=150, height=100)
    imagen.hAlign = 'CENTER'
    story.append(imagen)
    #story.append(Spacer(1, 12))

    from datetime import datetime
    fecha_hora = datetime.now().strftime("Documento generado %H:%M")
    fecha_hora_parrafo = Paragraph(fecha_hora , left_aligned_style)
    fecha_hora_parrafo.alignment = 1  # 2 = TA_RIGHT
    story.append(fecha_hora_parrafo)
    # Agrega un salto de línea
    #story.append(Spacer(1, 12))
    
    # Agrega el título
    title = Paragraph("<h3>Interworld</h3>", left_aligned_style)
    story.append(title)

    # Agrega un salto de línea
    #story.append(Spacer(1, 12))

    title2 = Paragraph("<h1>Reporte de citas realizadas</h1>", left_aligned_style)
    story.append(title2)

    
    title3 = Paragraph("<h3>El Oro Machala</h3>", left_aligned_style)
    story.append(title3)
    story.append(Spacer(1, 12))
    
    # Prepara los datos para la tabla
    data = [["tecnico", "cliente", "fecha", "comentario","estado"]]  # Encabezados

    for dato in datos:
        row = [dato['tecnico'], dato['cliente'], dato['fecha'], dato['comentario'],dato ['estado'] ]
        data.append(row)

    # Crea la tabla
    table = Table(data, colWidths=[100, 100, 100, 100]) 

    # Formatea la tabla
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))

    # Agrega la tabla al documento
    story.append(table)

    doc.build(story)

@app.route('/admin/reporte/re_vistacompleta', methods=['GET'])
def re_vistacompleta():
    doc = SimpleDocTemplate("reporte.pdf", pagesize=letter)
    story = []

    # Define un estilo con texto centrado
    styles = getSampleStyleSheet()
    left_aligned_style = styles['Heading3']
    left_aligned_style.alignment = 0  # 1 = TA_CENTER

    # Agrega la imagen
    imagen = Image('static/img/inter.png', width=100, height=150)
    imagen.hAlign = 'CENTER'
    story.append(imagen)
    story.append(Spacer(1, 12))

    from datetime import datetime
    fecha_hora = datetime.now().strftime("Documento generado %H:%M")
    fecha_hora_parrafo = Paragraph(fecha_hora , left_aligned_style)
    fecha_hora_parrafo.alignment = 1  # 2 = TA_RIGHT
    story.append(fecha_hora_parrafo)
    # Agrega un salto de línea
    
    
    
    # Agrega el título
    title = Paragraph("<h3>Interworld</h3>", left_aligned_style)
    story.append(title)

    # Agrega un salto de línea
    

    title2 = Paragraph("<h1>Reporte por tecnicos</h1>", left_aligned_style)
    #story.append(title2)

    # Agrega otro salto de línea
    

    title3 = Paragraph("<h3>El Oro Machala</h3>", left_aligned_style)
    story.append(title3)
    story.append(Spacer(1, 12))

    # Prepara los datos no como tabla
    client = request.args.get('tecnico', default=None, type=str)
    
    
    if client is not None:
        clie = db['reporte'].find({'tecnico': client})
    else:
        clie = db['reporte'].find()
    
    generar_pdf_vistacompleta(clie)
    
    return send_file('reporte.pdf', as_attachment=True)









#* Tecnico Recuperacion 
@app.route('/tecnicos/vistarecu')
def vistarecu():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
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

@app.route('/clientes/home',methods=['GET','POST'])
def casa():
    # Verifica si el usuario está en la sesión
    if 'username' in session:
        return render_template('clientes/home.html')
    else:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))


@app.route('/clientes/agenda', methods=['GET', 'POST'])
def agenda():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    if 'user' in session:
        if request.method == 'POST':
            agenda =db["agendar"]
            tecnico = request.form.get("tecnico", "")
            cliente=request.form["cliente"]
            hora=request.form["hora"]
            fecha=request.form["fecha"]
            telefono=request.form["telefono"]
            direccion=request.form["direccion"]
            canton=request.form["canton"]
            estado=request.form["estado"]
            
                
            # Verifica si la fecha y hora ya están ocupadas
            if agenda.count_documents({'fecha': fecha, 'hora': hora}) > 0:
                flash("La fecha y hora seleccionadas ya están ocupadas. Por favor, elige otra.")
                return redirect(url_for('agenda'))
    
            # Obtiene la fecha y hora actual
            fecha_actual = datetime.now()
            fecha_str = fecha_actual.strftime("%Y-%m-%d")  # Convierte la fecha a una cadena de texto
            
            # Verifica si el cliente ya tiene dos ingresos en la fecha actual
            if agenda.count_documents({'cliente': cliente, 'fecha': fecha_str}) < 1:
                agend = Agendar(tecnico, cliente, hora, fecha, telefono, direccion, canton, estado)
                agenda.insert_one(agend.AgeDBCollection())
                
            else:
                # Aquí puedes manejar el caso cuando el cliente ya tiene dos ingresos.
                # Por ejemplo, puedes mostrar un mensaje de error.
                mensaje ="Ya ingresastes una cita, espera que los técnicos pronto se comunicaran contigo."
                flash(mensaje)
                return  redirect(url_for('agenda'))
            
            #Obtén la colección 'tecnico'
            tecnico = db["tecnico"]
            
            #Busca todos los documentos en la colección 'tecnico'
            docs = tecnico.find({})
            
            for doc in docs:
                # Comprueba si el documento tiene un campo 'correo'
                if 'correo' in doc:
                    tecnico_email = doc['correo']
            
                    # Envía la notificación por correo electrónico
                    msg = Message('Nueva Agenda Registrada', sender='popeye198733@hotmail.com', recipients=[tecnico_email])
                    msg.body = f'Se ha registrado una nueva agenda con los siguientes datos {telefono},{direccion},{canton} para el cliente {cliente}.'
                    mail.send(msg)
                    flash("Su cita se guardo exitosamente")
                    # Redirect to the agenda page or render a template with a success message
                    return redirect(url_for('agenda'))  
            
        else:
            return render_template('clientes/agenda.html',user=session['user'])
    else:
        return render_template('clientes/agenda.html')


@app.route('/clientes/disponibilidad', methods=['GET'])
def disponibilidad():
    agenda = db["agendar"]
    
    # Obtiene la fecha actual
    fecha_actual = datetime.now()
    
    # Convierte la fecha a una cadena de texto en el formato que usas en tu base de datos
    fecha_str = fecha_actual.strftime("%Y-%m-%d")
    
    # Filtra las citas para que solo se muestren las que están programadas para la fecha actual o fechas futuras
    citas = agenda.find({'fecha': {'$gte': fecha_str}}, {"fecha": 1, "hora": 1})
    
    return render_template('clientes/disponibilidad.html', citas=citas)

# Clientes 
@app.route('/clientes/vistaagenda')
def vistaagenda():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    agenda = db["agendar"].find().sort("fecha", -1).limit(5)#*Muestra los registros de forma descendente y solo muestra 5 registros
    return render_template('clientes/vistaagenda.html', agendar=agenda)


# * Tecni  Vista de los tecnicos para el sistema 
#*Apartado de enviar y eliminar los registros de agendar
@app.route('/tecni/vistenvi', methods=['GET', 'POST'])
def vistencni2():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    if 'user' in session:
        tecnico = db['estado'].find_one({'tecnico': session['user']})
        if tecnico is None:
            return render_template('tecni/vistenvi.html')
        else:
            if request.method == 'POST':
                enviar=db["reporte"]
                agendar=db["agendar"]
                estador=db["estado"]
                cliente=request.form["cliente"]
                fecha=request.form["fecha"]
                direccion=request.form["direccion"]
                canton=request.form["canton"]
                comentario=request.form["comentario"]
                estado=request.form["estado"]
                if cliente and fecha and direccion and canton and comentario and estado:
                    enviare= Reporte(tecnico['tecnico'],cliente, fecha, direccion, canton, comentario, estado)
                    enviar.insert_one(enviare.RepoDBCollection())
                    # * Aquí eliminamos el documento de la colección "agendar"
                    agendar.delete_one({'cliente': cliente, 'fecha': fecha, 'direccion': direccion, 'canton': canton})
                    estador.delete_one({'cliente': cliente, 'fecha': fecha, 'direccion': direccion, 'canton': canton})
                    return redirect(url_for('vistecnicompleta'))
            else:
                estado=db['estado'].find()
                return render_template('tecni/vistenvi.html',estado=estado,user=session['user'],vistenviw2=tecnico)
    else:
        return render_template('tecni/vistenvi.html')
    

#*Vista de los reportes que tiene es para visualizar todo lo que hay en ella
@app.route('/tecni/vistacompleta')
def vistecnicompleta():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    if 'user' in session:
        count = db['reporte'].count_documents({'tecnico': session['user']})
        if count == 0:
            return render_template('tecni/vistenvi.html')
        else:
            reporte = db['reporte'].find({'tecnico': session['user']})
            return render_template('tecni/vistacompleta.html',reporte=reporte)
    else:
        return render_template('tecni/vistenvi.html')


@app.route('/tecni/home',methods=['GET','POST'])
def home3():
    # Verifica si el usuario está en la sesión
    if 'username' in session:
        return render_template('tecni/home.html')
    else:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True, port=5000)