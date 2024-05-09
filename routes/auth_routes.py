from flask import Blueprint, redirect, render_template, request, session, flash
from db import seleccion, accion
from formularios import Login, Registro, Recuperarpsw
from utilidades import pass_valido, email_valido
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import time

#create a Blueprint for auth-related routes
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/index/', methods=['POST', 'GET'])
@auth_blueprint.route('/home/', methods=['POST', 'GET'])
@auth_blueprint.route('/', methods=['GET', 'POST'])
@auth_blueprint.route('/login/', methods=['POST', 'GET'])
def login():
    frm_login = Login()
    if request.method == 'GET':
        return render_template('login.html', form_login=frm_login, titulo='Login de usuario')
    else:
        # Recuperar datos del formulario
        usr = escape(frm_login.usr.data.strip()).lower()
        pwd = escape(frm_login.pwd.data.strip())
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
                return render_template('login.html', form_login=frm_login, titulo='Login de usuario')
            
@auth_blueprint.route('/registro/', methods=['POST', 'GET'])
def registro():
    frm_register = Registro()
    if request.method == 'GET':
        return render_template('registro.html', form=frm_register, titulo='Registro de usuario')
    else:
        # Recuperar los datos del formulario
        nom = escape(request.form['nom']).capitalize()
        ape = escape(request.form['ape']).capitalize()
        ema = escape(request.form['ema']).lower()
        cema = escape(request.form['cema']).lower()
        cla = escape(request.form['cla'])
        ver = escape(request.form['ver'])
        fnac = escape(request.form['fnac'])
        sex = escape(frm_register.sex.data)

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

                return render_template('registro.html', form_register=frm_register, titulo='Registro de usuario')
            else:
                flash('Usuario correctamente registrado')
                
                # esperar 3 segundos antes de redirigir
                time.sleep(3)
                return redirect('/login/')

        return render_template('registro.html', form_register=frm_register, titulo='Registro de usuario')

@auth_blueprint.route('/salir/', methods=['GET'])
def salir():
    if 'id' not in session:
        return redirect('/')
    else:
        session.clear()
        session.pop("id", None)
        return redirect('/')

@auth_blueprint.route('/recuperarcontraseña/', methods=['POST', 'GET'])
def recuperarpsw():
    frm_recover_password = Recuperarpsw()
    return render_template('recuperarpsw.html', form_recover_password=frm_recover_password, titulo='Recuperar contraseña')