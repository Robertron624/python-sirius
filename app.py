import os
import random
from logging import exception
import time
from flask import Flask, render_template, request, session, flash, redirect, url_for
from werkzeug.utils import secure_filename
from wtforms.validators import Email
from formularios import Busqueda, Cambiarpsw, Roles, EditarUsuario, Comentario, Login, Mensaje, Registro, Recuperarpsw, Ayuda, Publicacion, editPublicacion
from markupsafe import escape
import os
from db import accion, editarimg, seleccion, eliminarimg
from werkzeug.security import check_password_hash, generate_password_hash
from utilidades import email_valido, pass_valido, format_datetime
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.errorhandler(404)
def error404(e):
    return render_template('404.html'), 404


@app.route('/index/', methods=['POST', 'GET'])
@app.route('/home/', methods=['POST', 'GET'])
@app.route('/', methods=['GET', 'POST'])
@app.route('/login/', methods=['POST', 'GET'])
def login():
    frm = Login()
    if request.method == 'GET':
        return render_template('login.html', form=frm, titulo='Login de usuario')
    else:
        # Recuperar datos del formulario
        usr = escape(frm.usr.data.strip()).lower()
        pwd = escape(frm.pwd.data.strip())
        # Preparacion de consulta no parametrica
        sql = f"SELECT id, nombre, apellidos, fnac, contraseña,sexo,rol_id,urlavatar FROM usuarios WHERE correo='{usr}'"
        # Ejecutar la consulta
        res = seleccion(sql)

        # Procesar los resultados
        if len(res) == 0:
            flash('ERROR: Usuario o contraseña no valido')
            return redirect('/login/')
        else:
            # Recuperar la clave almacenada en la base datos (cifrada)
            cbd = res[0][4]

            # Comparo la clave cifrada con la proporcianada en el formulario
            if check_password_hash(cbd, pwd):
                # Guardar los datos en una variable de sesion
                session.clear()
                session['id'] = res[0][0]
                session['nom'] = res[0][1]
                session['ape'] = res[0][2]
                session['ema'] = usr
                session['con'] = pwd
                session['fna'] = res[0][3]
                session['sex'] = res[0][5]
                session['rolid'] = res[0][6]
                session['urlava'] = res[0][7]
                return redirect('/feed/')
            # Informar de clave incorrecta y refrescar la pagina
            else:
                flash('ERROR: Usuario o contraseña no válida')
                return render_template('login.html', form=frm, titulo='Login de usuario')


@app.route('/registro/', methods=['POST', 'GET'])
def registro():
    frm = Registro()
    if request.method == 'GET':
        return render_template('registro.html', form=frm, titulo='Registro de usuario')
    else:
        # Recuperar los datos del formulario
        nom = escape(request.form['nom']).capitalize()
        ape = escape(request.form['ape']).capitalize()
        ema = escape(request.form['ema']).lower()
        cema = escape(request.form['cema']).lower()
        cla = escape(request.form['cla'])
        ver = escape(request.form['ver'])
        fnac = escape(request.form['fnac'])
        sex = escape(frm.sex.data)

        fnac2 = str(fnac)
        ffinal = datetime.strptime(fnac2, "%Y-%m-%d")
        hoy = datetime.today()

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

        # Preparacion de consulta no parametrica
        sql = f"SELECT id, nombre, apellidos, fnac, contraseña, sexo FROM usuarios WHERE correo='{ema}'"
        # Ejecutar la consulta
        res = seleccion(sql)

        swerror = False
        if nom == None or len(nom) == 0:
            flash('ERROR: Debe suministrar un nombre.')
            swerror = True
        if ape == None or len(ape) == 0:
            flash('ERROR: Debe suministrar sus apellidos.')
            swerror = True
        if ema == None or len(ema) == 0 or not email_valido(ema):
            flash('ERROR: Debe suministrar un correo electronico válido.')
            swerror = True
        if cema == None or len(ema) == 0 or not email_valido(ema):
            flash('ERROR: Debe suministrar un correo electronico de verificación válido.')
            swerror = True
        if cla == None or len(cla) == 0 or not pass_valido(cla):
            flash('ERROR: Debe suministrar una contraseña válida.')
            swerror = True
        if ver == None or len(ver) == 0 or not pass_valido(ver):
            flash('ERROR: Debe suministrar una contraseña válida.')
            swerror = True
        if fnac == None or len(fnac) == 0 or nacerror == False:
            flash('ERROR: Debes tener +18 para registrarte.')
            swerror = True
        if ema != cema:
            flash('ERRROR: el correo electronico y su verificación no coinciden.')
            swerror = True
        if cla != ver:
            flash('ERRROR: la contraseña y su verificación no coinciden')
            swerror = True
        if len(res) != 0:
            flash('ERRROR: Ya existe una cuenta registrada con este correo.')
            swerror = True
        if not swerror:
            # Preparar el query
            if sex == "H":
                urlava = "avatares/hombre-barba.jpg"
            elif sex == "M":
                urlava = "avatares/mujer1.jpg"
            elif sex == "P":
                urlava = "avatares/otro.png"
            sql = 'INSERT INTO usuarios(nombre, apellidos, correo, contraseña, fnac, sexo, urlavatar) VALUES(?, ?, ?, ?, ?, ?, ?)'
            # Ejecutar la consulta
            pwd = generate_password_hash(cla)
            res = accion(sql, (nom, ape, ema, pwd, fnac, sex, urlava))
            # Proceso los resultados
            if res == 0:
                flash('ERROR: No se pudieron registrar los datos, intente nuevamente')

                return render_template('registro.html', form=frm, titulo='Rereturn rendergistro de usuario')
            else:
                flash('Usuario correctamente registrado')
                
                # esperar 3 segundos antes de redirigir
                time.sleep(3)
                return redirect('/login/')

        return render_template('registro.html', form=frm, titulo='Rereturn rendergistro de usuario')


@app.route('/feed/', methods=['POST', 'GET'])
def home():
    if 'id' not in session:
        return redirect('/')
    else:
        frm = Busqueda()
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

            return render_template('feed.html', titulo='Feed', imglist=formatted_results, form=frm)
        else:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')


@app.route('/perfil/', methods=['GET', 'POST'])
def perfil():
    if 'id' not in session:
        return redirect('/')
    else:
        frm = Busqueda()
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

            print("RESGET -> ",res)
            return render_template('perfilusr.html', titulo='Mi perfil', ava=sex, form=frm, postList=formatted_results)
        else:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')


@app.route('/nueva_publicacion/', methods=['POST', 'GET'])
def nueva_publi():
    if 'id' not in session:
        return redirect('/')
    else:
        frm = Publicacion()
        frm_busqueda = Busqueda()
        if request.method == 'GET':
            sex = session["urlava"]
            return render_template('nueva_publicacion.html', titulo='Subir publicación', form=frm, ava=sex, form_busqueda=frm_busqueda)
        elif request.method == 'POST' and 'publish' in request.form:
            f = request.files['adj']
            nom2 = secure_filename(f.filename)
            if os.path.isfile(f'uploads/{nom2}'):
                name = str(random.randint(1, 5000))
                usr = session['ema']
                nom = session["nom"]
                ape = session["ape"]
                sex = session["sex"]
                urlava = session["urlava"]
                hoy = datetime.today().year
                hoy1 = datetime.today().month
                hoy2 = datetime.today().day
                hoy3 = datetime.today().hour
                hoy4 = datetime.today().minute
                fecpost = datetime(hoy, hoy1, hoy2, hoy3, hoy4)
                text = escape(request.form['publi'].capitalize())
                urlimg = f'/uploads/{name+nom2}'

                f.save(f'static/uploads/{name+nom2}')
                sql = 'INSERT INTO post(correo, nombre, apellido, datepost, text, url,sexo,urlavatar) VALUES(?, ?, ?, ?, ?, ?, ?, ?)'
                res = accion(sql, (usr, nom, ape, fecpost,
                                   text, urlimg, sex, urlava))
                return render_template('nueva_publicacion.html', titulo='Subir publicación', form=frm, ava=urlava, form_busqueda=frm_busqueda)
            else:
                usr = session['ema']
                nom = session["nom"]
                ape = session["ape"]
                urlava = session["urlava"]
                sex = session["sex"]
                urlava = session["urlava"]
                hoy = datetime.today().year
                hoy1 = datetime.today().month
                hoy2 = datetime.today().day
                hoy3 = datetime.today().hour
                hoy4 = datetime.today().minute
                fecpost = datetime(hoy, hoy1, hoy2, hoy3, hoy4)
                text = escape(request.form['publi'])
                urlimg = f'/uploads/{nom2}'

                f.save(f'static/uploads/{nom2}')
                sql = 'INSERT INTO post(correo, nombre, apellido, datepost, text, url,sexo,urlavatar) VALUES(?, ?, ?, ?, ?, ?, ?, ?)'
                res = accion(sql, (usr, nom, ape, fecpost,
                                   text, urlimg, sex, urlava))
                return render_template('nueva_publicacion.html', titulo='Subir publicación', form=frm, ava=urlava, form_busqueda=frm_busqueda)
        elif request.method == 'POST' and 'texto' in request.form:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')


@app.route('/publicacion/<int:id>/', methods=['GET', 'POST'])
def publicacion(id=None):
    if 'id' not in session:
        return redirect('/')
    else:
        frm_busqueda = Busqueda()
        frm_comentar = Comentario()
        if request.method == 'GET':
            sql = f"SELECT nombre, apellido, datepost, text, url FROM post WHERE id='{id}'"
            res = seleccion(sql)
            nombre = res[0][0]
            apellidos = res[0][1]
            sql2 = f"SELECT correo,sexo FROM usuarios WHERE nombre='{nombre}' AND apellidos='{apellidos}'"
            res2 = seleccion(sql2)
            sex = res2[0][1]
            img_owner = res2[0][0]
            id_img = id

            res_formatted = {tup[0]: tup[1:] for tup in res}

            temp_dict = {}

            for key, value in res_formatted.items():  # Iterate over items, not keys
                temp_dict[key] = value

            first_key = next(iter(temp_dict))  # Get the first key in the dictionary, which is the name of the image owner
            tuple_values = temp_dict[first_key]

            post_data = {
                'nombre': first_key,
                'apellidos': tuple_values[0],
                'datepost': tuple_values[1],
                'text': tuple_values[2],
                'url': tuple_values[3]
            }

            urlava = ''
            if sex == "H":
                urlava = "avatares/hombre-barba.jpg"
            elif sex == "M":
                urlava = "avatares/mujer1.jpg"
            elif sex == "P":
                urlava = "avatares/otro.png"

            sql3 = f"SELECT id,correo,nombre, apellidos, text, datecomment, urlavatar FROM comment WHERE idpost='{id_img}'"
            res3 = seleccion(sql3)

            formatted_comments_data = [{ 'id': row[0],
                                        'correo': row[1],
                                        'nombre': row[2],
                                        'apellidos': row[3],
                                        'text': row[4],
                                        'datecomment': format_datetime(row[5]),
                                        'urlavatar': row[6] } for row in res3]

            return render_template('publicacion.html', titulo='publicación', postInfo=post_data, ava=urlava, owner=img_owner, id_img=id_img, form_busqueda=frm_busqueda, form_comentar=frm_comentar, commentList=formatted_comments_data)
        elif request.method == 'POST' and 'texto' in request.form:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')
        elif request.method == 'POST' and 'comment_btn' in request.form:
            comentario = request.form['comment_text']
            hoy = datetime.today().year
            hoy1 = datetime.today().month
            hoy2 = datetime.today().day
            hoy3 = datetime.today().hour
            hoy4 = datetime.today().minute
            emausuario = session['ema']
            nom = session['nom']
            ape = session['ape']
            urlava = session['urlava']
            fecpost = datetime(hoy, hoy1, hoy2, hoy3, hoy4)
            idimg = id

            sql = 'INSERT into comment(correo, nombre, apellidos, text, datecomment, idpost, urlavatar) VALUES(?,?,?,?,?,?,?)'
            res = accion(sql, (emausuario, nom, ape,
                               comentario, fecpost, idimg, urlava))
            if res == 0:
                flash('Error: no se pudo guardar el comentario')
                print('HUBO UN ERROR AL GUARDAR')
            else:
                return redirect(f'/publicacion/{id}')


@app.route('/eliminar/<int:id>')
def eliminar(id=None):
    if 'id' not in session:
        return redirect('/')
    else:
        sql = f"DELETE FROM post WHERE id IN ({id})"
        resultado = eliminarimg(sql)
        if resultado == 0:
            flash('Error al eliminar la publicacion')
            return redirect(f'/publicacion/{id}')
        else:
            return redirect('/feed/')


@app.route('/eliminarcomment/<int:id>/<int:idcomment>')
def eliminarcomment(id=None, idcomment=None):
    if 'id' not in session:
        return redirect('/')
    else:
        sql = f"DELETE FROM comment WHERE id IN ({idcomment})"
        resultado = eliminarimg(sql)
        if resultado == 0:
            flash('Error al eliminar el comentario')
            return redirect(f'/publicacion/{id}')
        else:
            return redirect(f'/publicacion/{id}')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id=None):
    if 'id' not in session:
        return redirect('/')
    else:
        frm = editPublicacion()
        frm_busqueda = Busqueda()
        if request.method == 'GET':
            idImg = id
            sex = session["urlava"]
            sql_url = f"SELECT url from post WHERE id='{id}'"
            res = seleccion(sql_url)
            url_img = res[0][0]
            return render_template('editar_publicacion.html', titulo='Editar publicación', form=frm, ava=sex, id_img=idImg, ruta=url_img, form_busqueda=frm_busqueda)
        elif request.method == 'POST' and 'texto' in request.form:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')
        else:
            text = escape(request.form['publi']).capitalize()
            sql = f"UPDATE post SET text='{text}' WHERE id='{id}'"
            resultado = editarimg(sql)

            if resultado == 0:
                flash('Error al guardar los cambios')
                return redirect('/editar_publicacion/')
            else:
                return redirect('/feed/')


@app.route('/recuperarcontraseña/', methods=['POST', 'GET'])
def recuperarpsw():
    recu = Recuperarpsw()
    return render_template('recuperarpsw.html', form=recu, titulo='Recuperar contraseña')


@app.route('/busqueda/<string:texto>', methods=['POST', 'GET'])
def busqueda(texto=None):
    if 'id' not in session:
        return redirect('/')
    else:
        frm = Busqueda()
        if request.method == 'GET':
            # Request a base de datos de usuario
            busr = str(texto).capitalize()
            sql = f"SELECT id, nombre, apellidos, urlavatar FROM usuarios WHERE nombre='{busr}'"
            res = seleccion(sql)
            sex = session["urlava"]

            # Request a base de datos de post
            busr2 = str(texto).lower()
            sql2 = f"SELECT DISTINCT id, text, url FROM post WHERE LOWER(text) LIKE LOWER('{busr2}')"
            res2 = seleccion(sql2)

            try:
                msg_receptor = res[0][0]
                return render_template('result-busqueda.html', titulo='Resultados de la búsqueda', userList=res, imglist=res2, ava=sex, form=frm, idreceptor=msg_receptor)
            except Exception:
                return render_template('result-busqueda.html', titulo='Resultados de la búsqueda', userList=res, imglist=res2, ava=sex, form=frm)

        else:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')


@app.route('/enviarmensaje/<int:idremitente>/<int:idreceptor>/', methods=['GET', 'POST'])
def enviarmsj(idremitente=None, idreceptor=None):
    if 'id' not in session:
        return redirect('/')
    else:
        frm_mensaje = Mensaje()
        frm_busqueda = Busqueda()

        if request.method == 'GET':
            receptor = idreceptor
            sex = session['urlava']
            sql2 = f"SELECT nombre, apellidos FROM usuarios WHERE id='{receptor}'"
            res2 = seleccion(sql2)
            return render_template('enviar_mensaje.html', form_mensaje=frm_mensaje, form_busqueda=frm_busqueda, receptor=res2, ava=sex)
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
                return render_template('enviar_mensaje.html', form_mensaje=frm_mensaje, form_busqueda=frm_busqueda, receptor=res2, ava=sex)
            else:
                flash('Error: no se pudo enviar el mensaje')
                return render_template('enviar_mensaje.html', form_mensaje=frm_mensaje, form_busqueda=frm_busqueda, receptor=res2, ava=sex)
        elif request.method == 'POST' and 'texto' in request.form:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')


@app.route('/mensajes/<int:id>', methods=['GET', 'POST'])
def mostrarmsj(id=None):
    if 'id' not in session:
        return redirect('/')
    else:
        frm_busqueda = Busqueda()
        if request.method == 'GET':
            userid = id

            sql = f"SELECT nomemi,apeemi, texto FROM mensajes WHERE receptor='{userid}'"
            res = seleccion(sql)

            return render_template('mensajes_privados.html',
                                   form_busqueda=frm_busqueda, msgList=res)
        else:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')


@app.route('/ayuda/')
def ayuda():
    frm = Ayuda()
    return render_template("ayuda.html", form=frm, titulo="Ayuda")


@app.route('/salir/', methods=['GET'])
def salir():
    if 'id' not in session:
        return redirect('/')
    else:
        session.clear()
        session.pop("id", None)
        return redirect('/')


@app.route('/editarusuario/', methods=['POST', 'GET'])
def editarusuario():
    if 'id' not in session:
        return redirect('/')
    else:
        frm = EditarUsuario()
        if request.method == 'GET':
            return render_template('editarusuario.html', form=frm, titulo='Editar usuario')
        else:
            # Recuperar los datos del formulario
            nom = escape(request.form['nom']).capitalize()
            ape = escape(request.form['ape']).capitalize()
            cla = escape(request.form['cla']).strip()
            fnac = escape(request.form['fnac'])
            sex = escape(frm.sex.data)
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
            pwd = escape(frm.cla.data.strip())
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

                    return render_template('editarusuario.html', form=frm, titulo='Editar usuario')
                else:
                    flash('Cambios efectuados correctamente.')

            return render_template('editarusuario.html', form=frm, titulo='Editar usuario')


@app.route('/cambiarpsw/', methods=['POST', 'GET'])
def cambiarpsw():
    if 'id' not in session:
        return redirect('/')
    else:
        recu = Cambiarpsw()
        if request.method == 'GET':
            return render_template('cambiarpsw.html', form=recu, titulo='Cambiar contraseña')
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
                return render_template('cambiarpsw.html', form=recu, titulo='Cambiar contraseña')
            else:
                return render_template('login.html', form=recu, titulo='Cambiar contraseña')


@app.route('/roles/<int:iduser>/', methods=['GET', 'POST'])
def asigroles(iduser=None):
    frm = Roles()
    frm_busqueda = Busqueda()
    if request.method == 'GET':
        idbus = iduser
        sql = f"SELECT nombre, apellidos, rol_id FROM usuarios WHERE id='{idbus}'"
        res = seleccion(sql)
        nombre = res[0][0]
        apellido = res[0][1]
        rol = res[0][2]
        sex = session["urlava"]

        return render_template('roles.html', form=frm, nom=nombre, ape=apellido, rol=rol, ava=sex, form_busqueda=frm_busqueda, rolLog=session['rolid'])
    elif request.method == 'POST' and 'btn_admin' in request.form:
        idbus = iduser
        sql = f"SELECT nombre, apellidos, rol_id FROM usuarios WHERE id='{idbus}'"
        res = seleccion(sql)
        sex = session["urlava"]
        nombre = res[0][0]
        apellido = res[0][1]
        rol = res[0][2]
        sql2 = f"UPDATE usuarios SET rol_id='ADMINISTRADOR' WHERE id='{idbus}'"
        res2 = editarimg(sql2)

        if res == 0:
            flash('Error al cambiar de rol')
            return render_template('roles.html', form=frm, nom=nombre, ava=sex, ape=apellido, rol=rol, rolLog=session['rolid'])
        else:
            return redirect(f'/roles/{idbus}')
    elif request.method == 'POST' and 'btn_user' in request.form:
        idbus = iduser
        sql = f"SELECT nombre, apellidos, rol_id FROM usuarios WHERE id='{idbus}'"
        res = seleccion(sql)
        sex = session["urlava"]
        nombre = res[0][0]
        apellido = res[0][1]
        rol = res[0][2]
        sql2 = f"UPDATE usuarios SET rol_id='USUARIO' WHERE id='{idbus}'"
        res2 = editarimg(sql2)
        if res2 == 0:

            return render_template('roles.html', form=frm, nom=nombre, ava=sex, ape=apellido, rol=rol)
        else:
            return redirect(f'/roles/{idbus}')
    elif request.method == 'POST' and 'texto' in request.form:
        texto = request.form['texto']
        return redirect(f'/busqueda/{texto}')


if __name__ == '__main__':
    app.run(debug=True, port=80)
