from flask import Blueprint, redirect, render_template, request, session, flash, jsonify
from db import seleccion, accion
from formularios import Login, Signup, Recuperarpsw
from utilidades import pass_valido, email_valido, is_adult
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
        
        # If the user is already logged in, redirect to the feed
        if 'id' in session:
            return redirect('/feed/')
        else:
            return render_template('login.html', form_login=frm_login, titulo='Login de usuario')
    else:
        # Recuperar datos del formulario
        login_user = escape(frm_login.login_user.data.strip()).lower()
        login_password = escape(frm_login.login_password.data.strip())

        sql = f"SELECT id, nombre, apellidos, fnac, contraseña,sexo,rol_id,urlavatar FROM usuarios WHERE correo='{login_user}'"
        # Ejecutar la consulta
        res = seleccion(sql)

        # Procesar los resultados
        if len(res) == 0:
            return jsonify({'error': 'Usuario o contraseña no valido'}), 401
        else:
            # Recuperar la clave almacenada en la base datos (cifrada)
            cbd = res[0][4]

            # Comparo la clave cifrada con la proporcianada en el formulario
            if check_password_hash(cbd, login_password):
                # Guardar los datos en una variable de sesion
                session.clear()
                session['id'] = res[0][0]
                session['nom'] = res[0][1]
                session['ape'] = res[0][2]
                session['ema'] = login_user
                session['con'] = login_password
                session['fna'] = res[0][3]
                session['sex'] = res[0][5]
                session['rolid'] = res[0][6]
                session['urlava'] = res[0][7]
                
                return jsonify({'success': True}), 200
            # Informar de clave incorrecta y refrescar la pagina
            else:
                return jsonify({'error': 'Usuario o contraseña no valido'}), 401
            
@auth_blueprint.route('/registro/', methods=['POST', 'GET'])
def registro():
    frm_register = Signup()
    if request.method == 'GET':
        return render_template('signup.html', form_register=frm_register, titulo='Registro de usuario')
    else:
        # Recuperar los datos del formulario
        first_name = escape(request.form['signup_first_name']).capitalize()
        last_name = escape(request.form['signup_last_name']).capitalize()
        email = escape(request.form['signup_email']).lower()
        confirm_email = escape(request.form['signup_confirm_email']).lower()
        password = escape(request.form['signup_password'])
        confirm_password = escape(request.form['signup_confirm_password'])
        birthdate = escape(request.form['signup_birthdate'])
        sex = escape(frm_register.signup_sex.data)

        birthdate_obj = datetime.strptime(birthdate, '%Y-%m-%d')
        is_user_adult = is_adult(birthdate_obj)

        # Preparacion de consulta no parametrica
        sql = f"SELECT id, nombre, apellidos, fnac, contraseña, sexo FROM usuarios WHERE correo='{email}'"
        # Ejecutar la consulta
        res = seleccion(sql)

        swerror = False
        if first_name == None or len(first_name) == 0:
            flash('ERROR: Debe suministrar un nombre.')
            swerror = True
        if last_name == None or len(last_name) == 0:
            flash('ERROR: Debe suministrar sus apellidos.')
            swerror = True
        if email == None or len(email) == 0 or not email_valido(email):
            flash('ERROR: Debe suministrar un correo electrónico válido.')
            swerror = True
        if confirm_email == None or len(confirm_email) == 0 or not email_valido(confirm_email):
            flash('ERROR: Debe suministrar un correo electronico de verificación válido.')
            swerror = True
        if password == None or len(password) == 0 or not pass_valido(password):
            flash('ERROR: Debe suministrar una contraseña válida.')
            swerror = True
        if confirm_password == None or len(confirm_password) == 0 or not pass_valido(confirm_password):
            flash('ERROR: Debe suministrar una contraseña válida.')
            swerror = True
        if birthdate == None or len(birthdate) == 0 or is_user_adult == False:
            flash('ERROR: Debes tener +18 para registrarte.')
            swerror = True
        if email != confirm_email:
            flash('ERRROR: el correo electronico y su verificación no coinciden.')
            swerror = True
        if password != confirm_password:
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
            hashed_password = generate_password_hash(password)
            res = accion(sql, (first_name, last_name, email, hashed_password, birthdate, sex, urlava))
            # Proceso los resultados
            if res == 0:
                flash('ERROR: No se pudieron registrar los datos, intente nuevamente')

                return render_template('signup.html', form_register=frm_register, titulo='Registro de usuario')
            else:
                flash('Usuario correctamente registrado')
                
                # esperar 3 segundos antes de redirigir
                time.sleep(3)
                return redirect('/login/')

        return render_template('signup.html', form_register=frm_register, titulo='Registro de usuario')

@auth_blueprint.route('/salir/', methods=['GET'])
def salir():
    if 'id' not in session:
        return redirect('/')
    else:
        session.clear()
        session.pop("id", None)
        return redirect('/')

@auth_blueprint.route('/recuperar-contraseña/', methods=['POST', 'GET'])
def password_recovery():
    frm_recover_password = Recuperarpsw()
    return render_template('recuperarpsw.html', form_recover_password=frm_recover_password, titulo='Recuperar contraseña')