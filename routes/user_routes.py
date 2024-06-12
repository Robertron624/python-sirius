from flask import Blueprint, redirect, render_template, request, session, flash, jsonify
from db import seleccion, accion, editarimg
from utilidades import format_datetime
from formularios import Edit_user, Search, Change_password, Message
from utilidades import pass_valido, is_adult
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

#create a Blueprint for user-related routes

user_blueprint = Blueprint('user', __name__)
@user_blueprint.route('/perfil/', methods=['GET', 'POST'])
@user_blueprint.route('/perfil/<int:id>', methods=['GET', 'POST'])
def profile(id=None):
    if 'id' not in session:
        return redirect('/')
    
    frm_search = Search()
    user_id = session['id']  # ID del usuario logueado

    if id is None:
        # Mostramos el perfil del usuario logueado
        id = user_id

    if id != user_id:
        # Mostrar perfil de otro usuario
        
        sql = f"SELECT nombre, apellidos, correo, urlavatar FROM usuarios WHERE id='{id}'"
        res = seleccion(sql)
        
        if not res:
            return render_template('404.html'), 404
        
        user_personal_info = res[0]
        user_personal_info_formatted = {
            'id': id, # 'id' es el 'id' del usuario
            'name': user_personal_info[0],
            'lastname': user_personal_info[1],
            'email': user_personal_info[2], # 'correo' es el 'email' del usuario
            'url_avatar': user_personal_info[3]
        }
        
        sql2 = f"SELECT id, nombre, apellido, datepost, text, urlavatar, url FROM post WHERE correo='{user_personal_info[2]}'"
        res2 = seleccion(sql2)
        
        
        formatted_results = [{
            'id': row[0], 
            'nombre': row[1], 
            'apellido': row[2], 
            'datepost': format_datetime(row[3]),
            'text': row[4],
            'urlavatar': row[5],
            'url': row[6]
        } for row in res2]

        return render_template('profile.html', titulo='Perfil', postList=formatted_results, form_search=frm_search, include_header=True, is_this_third_party_profile=True, user_personal_info=user_personal_info_formatted)
    
    else:
        # Mostrar perfil del usuario logueado
        usr = session['ema']
        sex = session["urlava"]
        try:
            sql = f"SELECT id, nombre, apellido, datepost, text, urlavatar, url FROM post WHERE correo='{usr}'"
            res = seleccion(sql)
        except Exception as e:
            print("Error fetching user posts, error:", e)
            return render_template('404.html'), 404

        formatted_results = [{
            'id': row[0], 
            'nombre': row[1], 
            'apellido': row[2], 
            'datepost': format_datetime(row[3]),
            'text': row[4],
            'urlavatar': row[5],
            'url': row[6]
        } for row in res]

        return render_template('profile.html', titulo='Mi perfil', ava=sex, form_search=frm_search, postList=formatted_results, include_header=True, is_this_third_party_profile=False)
    
@user_blueprint.route('/feed/', methods=['POST', 'GET'])
def home():
    if 'id' not in session:
        return redirect('/')
    else:
        frm_search = Search()
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

            return render_template('feed.html', titulo='Feed', posts_list=formatted_results, form_search=frm_search, include_header=True)
        else:
            search_text = request.form['search_text'].capitalize()
            return redirect(f'/busqueda/{search_text}')


@user_blueprint.route('/editar-usuario/', methods=['POST', 'GET'])
def edit_user():
    if 'id' not in session:
        return redirect('/')
    else:
        frm_edit_user = Edit_user()
        frm_search = Search()
        if request.method == 'GET':
            return render_template('edit-user.html', form_edit_user=frm_edit_user, titulo='Editar usuario', form_search=frm_search, include_header=True)
        else:
            # Recuperar los datos del formulario
            first_name = escape(request.form['edit_first_name']).capitalize()
            last_name = escape(request.form['edit_last_name']).capitalize()
            password = escape(request.form['edit_password']).strip()
            birthdate_str = escape(request.form['edit_birthdate'])
            sex = escape(frm_edit_user.edit_sex.data)
            
            birthdate_object = datetime.strptime(birthdate_str, '%Y-%m-%d')
            is_new_adult = is_adult(birthdate_object)
            
            email = session['ema']
            
            if sex == "H":
                urlava = "avatares/hombre-barba.jpg"
            elif sex == "M":
                urlava = "avatares/mujer1.jpg"
            elif sex == "P":
                urlava = "avatares/otro.png"

            swerror = False
            if first_name == None or len(first_name) == 0:
                flash('ERROR: Debe suministrar un nombre.')
                swerror = True
            if last_name == None or len(last_name) == 0:
                flash('ERROR: Debe suministrar sus apellidos.')
                swerror = True
            if password == None or len(password) == 0 or not pass_valido(password):
                flash('ERROR: Debe suministrar una contraseña valida.')
                swerror = True
            if birthdate_str == None or len(birthdate_str) == 0 or is_new_adult == False:
                flash('ERROR: Debes tener +18 para registrarte.')
                swerror = True
            pwd = escape(frm_edit_user.edit_password.data.strip())
            sql = f"SELECT contraseña FROM usuarios WHERE correo='{email}'"
            res2 = seleccion(sql)
            cbd = res2[0][0]

            if check_password_hash(cbd, pwd) == False:
                flash('ERROR: La contraseña no coincide.')
                swerror = True
            if not swerror:
                sql = f"UPDATE usuarios SET nombre='{first_name}',apellidos='{last_name}',fnac='{birthdate_object}',sexo='{sex}',urlavatar='{urlava}' WHERE correo='{email}'"
                res = editarimg(sql)
                # Proceso los resultados
                if res == 0:
                    flash(
                        'ERROR: No se pudieron registrar los datos, intente nuevamente')

                    return render_template('edit-user.html', form_edit_user=frm_edit_user, titulo='Editar usuario')
                else:
                    flash('Cambios efectuados correctamente.')

            return render_template('edit-user.html', form_edit_user=frm_edit_user, titulo='Editar usuario')
        
@user_blueprint.route('/cambiar-contraseña/', methods=['PUT', 'GET'])
def change_password():
    if 'id' not in session:
        return redirect('/')
    else:
        frm_change_password = Change_password()
        frm_search = Search()
        if request.method == 'GET':
            return render_template('change-password.html', form_change_password=frm_change_password, form_search=frm_search, titulo='Cambiar contraseña', include_header=True)
        else:
            
            data = request.get_json()
            
            if(not data):
                return jsonify({'error': 'No se han suministrado datos'}), 400
            
            previous_password = escape(data.get('previous_password')).strip()
            new_password = escape(data.get('new_password')).strip()
            new_password_confirm = escape(data.get('new_password_confirm')).strip()
            usr = session['ema']
            sql = f"SELECT contraseña FROM usuarios WHERE correo='{usr}'"
            res = seleccion(sql)
            current_password = res[0][0]

            if check_password_hash(current_password, previous_password) == False:
                return jsonify({'error': 'La contraseña actual es incorrecta.'}), 400
            if previous_password == None or len(previous_password) == 0 or not pass_valido(previous_password):
                return jsonify({'error': 'Debe suministrar la actual contraseña válida.'}), 400
            if new_password == None or len(new_password) == 0 or not pass_valido(new_password):
                return jsonify({'error': 'La nueva contraseña es inválida.'}), 400
            if new_password_confirm == None or len(new_password_confirm) == 0 or not pass_valido(new_password_confirm):
                return jsonify({'error': 'La confirmación de la nueva contraseña es inválida.'}), 400
            if new_password != new_password_confirm:
                return jsonify({'error': 'La nueva contraseña y su confirmación no coinciden.'}), 400
            
            new_password_hashed = generate_password_hash(new_password)

            sql = f"UPDATE usuarios SET contraseña='{new_password_hashed}' WHERE correo='{usr}'"
            res = editarimg(sql)
            
            if res == 0:
                return jsonify({'error': 'No se pudo cambiar la contraseña.'}), 400
            else:
                session.clear()
                return jsonify({'message': 'Contraseña cambiada correctamente.'}), 200

            
  
                
        