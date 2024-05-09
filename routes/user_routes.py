from flask import Blueprint, redirect, render_template, request, session, flash
from db import seleccion, accion, editarimg
from utilidades import format_datetime
from formularios import EditarUsuario, Busqueda, Cambiarpsw, Mensaje
from utilidades import pass_valido
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

#create a Blueprint for user-related routes

user_blueprint = Blueprint('user', __name__)
@user_blueprint.route('/perfil/', methods=['GET', 'POST'])
def perfil():
    if 'id' not in session:
        return redirect('/')
    else:
        frm_search = Busqueda()
        if request.method == 'GET':
            usr = session['ema']
            sex = session["urlava"]
            sql = f"SELECT id, nombre, apellido, datepost, text, urlavatar, url FROM post WHERE correo='{usr}'"
            res = seleccion(sql)

            formatted_results = [{ 'id': row[0], 
                       'nombre': row[1], 
                       'apellido': row[2], 
                       'datepost': format_datetime(row[3]),
                       'text': row[4],
                       'urlavatar': row[5],
                       'url': row[6],
                        } for row in res]

            return render_template('perfilusr.html', titulo='Mi perfil', ava=sex, form_search=frm_search, postList=formatted_results, include_header=True)
        else:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')

@user_blueprint.route('/feed/', methods=['POST', 'GET'])
def home():
    if 'id' not in session:
        return redirect('/')
    else:
        frm_search = Busqueda()
        if request.method == 'GET':
            sql = f"SELECT id, correo,nombre,apellido, datepost, text, url, sexo, urlavatar FROM post"
            resget = seleccion(sql)

            formatted_results = [{ 'id': row[0], 
                       'correo': row[1], 
                       'nombre': row[2], 
                       'apellido': row[3], 
                       'datepost': format_datetime(row[4]),
                       'text': row[5], 
                       'url': row[6], 
                       'sexo': row[7], 
                       'urlavatar': row[8] } for row in resget]

            return render_template('feed.html', titulo='Feed', imglist=formatted_results, form_search=frm_search, include_header=True)
        else:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')
        
@user_blueprint.route('/editarusuario/', methods=['POST', 'GET'])
def editarusuario():
    if 'id' not in session:
        return redirect('/')
    else:
        frm_edit_user = EditarUsuario()
        if request.method == 'GET':
            return render_template('editarusuario.html', form_edit_user=frm_edit_user, titulo='Editar usuario', include_header=True)
        else:
            # Recuperar los datos del formulario
            nom = escape(request.form['nom']).capitalize()
            ape = escape(request.form['ape']).capitalize()
            cla = escape(request.form['cla']).strip()
            fnac = escape(request.form['fnac'])
            sex = escape(frm_edit_user.sex.data)
            fnac2 = str(fnac)
            ffinal = datetime.strptime(fnac2, "%Y-%m-%d")
            hoy = datetime.today()
            ema = session["ema"]
            nacerror = False
            if (ffinal.year + 18) < hoy.year:
                nacerror = True
            elif (ffinal.year + 18) == hoy.year:
                if (ffinal.month > hoy.month):
                    nacerror = True
                elif (ffinal.month == hoy.month):
                    if (ffinal.day >= hoy.day):
                        nacerror = True
                    else:
                        nacerror = False
            if sex == "H":
                urlava = "avatares/hombre-barba.jpg"
            elif sex == "M":
                urlava = "avatares/mujer1.jpg"
            elif sex == "P":
                urlava = "avatares/otro.png"

            swerror = False
            if nom == None or len(nom) == 0:
                flash('ERROR: Debe suministrar un nombre.')
                swerror = True
            if ape == None or len(ape) == 0:
                flash('ERROR: Debe suministrar sus apellidos.')
                swerror = True
            if cla == None or len(cla) == 0 or not pass_valido(cla):
                flash('ERROR: Debe suministrar una contraseña valida.')
                swerror = True
            if fnac == None or len(fnac) == 0 or nacerror == False:
                flash('ERROR: Debes tener +18 para registarte.')
                swerror = True
            pwd = escape(frm_edit_user.cla.data.strip())
            sql = f"SELECT contraseña FROM usuarios WHERE correo='{ema}'"
            res2 = seleccion(sql)
            cbd = res2[0][0]

            if check_password_hash(cbd, pwd) == False:
                flash('ERROR: La contraseña no coincide.')
                swerror = True
            if not swerror:
                sql = f"UPDATE usuarios SET nombre='{nom}',apellidos='{ape}',fnac='{fnac}',sexo='{sex}',urlavatar='{urlava}' WHERE correo='{ema}'"
                res = editarimg(sql)
                # Proceso los resultados
                if res == 0:
                    flash(
                        'ERROR: No se pudieron registrar los datos, intente nuevamente')

                    return render_template('editarusuario.html', form_edit_user=frm_edit_user, titulo='Editar usuario', include_header=True)
                else:
                    flash('Cambios efectuados correctamente.')

            return render_template('editarusuario.html', form_edit_user=frm_edit_user, titulo='Editar usuario', include_header=True)
        
@user_blueprint.route('/cambiarpsw/', methods=['POST', 'GET'])
def cambiarpsw():
    if 'id' not in session:
        return redirect('/')
    else:
        frm_change_password = Cambiarpsw()
        frm_search = Busqueda()
        if request.method == 'GET':
            return render_template('cambiarpsw.html', form_change_password=frm_change_password, form_search=frm_search, titulo='Cambiar contraseña', include_header=True)
        else:
            pwdan = escape(request.form['claan']).strip()
            pwdn = escape(request.form['clanue']).strip()
            pwdcn = escape(request.form['comclanue']).strip()
            usr = session['ema']
            sql = f"SELECT contraseña FROM usuarios WHERE correo='{usr}'"
            res = seleccion(sql)
            cbd = res[0][0]

            swerror = False
            if check_password_hash(cbd, pwdan) == False:
                flash('ERROR: La contraseña no coincide.')
                swerror = True
            if pwdan == None or len(pwdan) == 0 or not pass_valido(pwdan):
                flash('ERROR: Debe suministrar una contraseña válida.')
            if pwdn == None or len(pwdn) == 0 or not pass_valido(pwdn):
                flash('ERROR: Debe suministrar una contraseña válida.')
                swerror = True
            if pwdcn == None or len(pwdcn) == 0 or not pass_valido(pwdcn):
                flash('ERROR: Debe suministrar una contraseña válida.')
                swerror = True
            if pwdn != pwdcn:
                flash('ERRROR: la contraseña y su verificación no coinciden')
                swerror = True
            if not swerror:
                newcla = generate_password_hash(pwdn)

                sql = f"UPDATE usuarios SET contraseña='{newcla}' WHERE correo='{usr}'"
                res = editarimg(sql)
            if res == 0:
                flash('ERROR: No se pudo registrar el cambio.')
                return render_template('cambiarpsw.html', form_change_password=frm_change_password, form_search=frm_search, titulo='Cambiar contraseña', include_header=True)
            else:
                # make the user log in again with the new password
                session.clear()
                return redirect('/')

            
@user_blueprint.route('/mensajes/<int:id>', methods=['GET', 'POST'])
def mostrarmsj(id=None):
    if 'id' not in session:
        return redirect('/')
    else:
        frm_search = Busqueda()
        if request.method == 'GET':
            userid = id

            sql = f"SELECT nomemi,apeemi, texto FROM mensajes WHERE receptor='{userid}'"
            res = seleccion(sql)

            return render_template('mensajes_privados.html',
                                   form_search=frm_search, msgList=res, titulo='Mensajes privados', include_header=True)
        else:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')
    
@user_blueprint.route('/enviarmensaje/<int:idremitente>/<int:idreceptor>/', methods=['GET', 'POST'])
def enviarmsj(idremitente=None, idreceptor=None):
    if 'id' not in session:
        return redirect('/')
    else:
        frm_mensaje = Mensaje()
        frm_search = Busqueda()

        if request.method == 'GET':
            receptor = idreceptor
            sex = session['urlava']
            sql2 = f"SELECT nombre, apellidos FROM usuarios WHERE id='{receptor}'"
            res2 = seleccion(sql2)
            return render_template('enviar_mensaje.html', form_mensaje=frm_mensaje, form_search=frm_search, receptor=res2, ava=sex, include_header=True)
        elif request.method == 'POST' and ('btn_mensaje' or 'texto_mensaje'):
            remitente = idremitente
            receptor = idreceptor
            mensaje = request.form['texto_mensaje']
            sex = session['urlava']
            nombre_emisor = session['nom']
            apellido_emisor = session['ape']

            sql = "INSERT INTO mensajes(remitente, receptor,nomemi, apeemi, texto) VALUES(?,?,?,?,?)"
            res = accion(sql, (remitente, receptor,
                               nombre_emisor, apellido_emisor, mensaje))

            sql2 = f"SELECT nombre, apellidos FROM usuarios WHERE id='{receptor}'"
            res2 = seleccion(sql2)

            if res == 0:
                flash('Mensaje enviado correctamente')
                return render_template('enviar_mensaje.html', form_mensaje=frm_mensaje, form_search=frm_search, receptor=res2, ava=sex, include_header=True)
            else:
                flash('Error: no se pudo enviar el mensaje')
                return render_template('enviar_mensaje.html', form_mensaje=frm_mensaje, form_search=frm_search, receptor=res2, ava=sex, include_header=True)
        elif request.method == 'POST' and 'texto' in request.form:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')