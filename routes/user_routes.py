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

            
@user_blueprint.route('/mensajes', methods=['GET', 'POST'])
def private_messages(id=None):
    if 'id' not in session:
        return redirect('/')
    else:
        frm_search = Search()
        if request.method == 'GET':
            user_id = session['id']
            sql = f"""
                SELECT u.nombre, u.apellidos, m.text, m.image_url, m.created_at, m.updated_at
                FROM messages m
                JOIN usuarios u ON m.sender_id = u.id
                WHERE m.receiver_id = {user_id}
            """
            response = seleccion(sql)
            
            if len(response) == 0:
                message_list = []
            else:
                message_list = [{
                    'sender_name': row[0],
                    'sender_last_name': row[1],
                    'text': row[2],
                    'image_url': row[3],
                    'created_at': format_datetime(row[4]),
                    'updated_at': format_datetime(row[5])
                } for row in response]
                
            return render_template('private-messages.html',
                                   form_search=frm_search, message_list=message_list, titulo='Mensajes privados', include_header=True)
        else:
            search_text = request.form['search_text'].capitalize()
            return redirect(f'/busqueda/{search_text}')


@user_blueprint.route('/enviar-mensaje/<int:receiver_id>/', methods=['GET', 'POST'])
def send_message(receiver_id=None):
    if 'id' not in session:
        return redirect('/')
    else:
        frm_send_message = Message()
        frm_search = Search()
            
        if request.method == 'POST':
        
            # Handle search
            if 'search_text' in request.form:
                search_text = request.form['search_text'].capitalize()
                return redirect(f'/busqueda/{search_text}')
            
            # Handle message sending
            sender_id = session['id']
            
            if receiver_id is None:
                jsonify({'error': 'Receiver ID is required.'}), 400
            
            message_text = frm_send_message.message_text.data
            if not message_text:
                jsonify({'error': 'Message text is required.'}), 400
            
            attached_image = frm_send_message.attached_image.data
            
            if attached_image:
                file_extension = attached_image.filename.split('.')[-1]
                if file_extension not in ['jpg', 'jpeg', 'png', 'gif']:
                    jsonify({'error': 'Invalid file type.'}), 400

                try:
                    attached_image.save(f"static/uploads/{attached_image.filename}")
                    image_url = f"/uploads/{attached_image.filename}"
                except Exception as e:
                    print("Error while trying to save the image, error:", e)
                    jsonify({'error': 'Error while trying to save the image, try again'}), 500
            else:
                image_url = None
                
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            sql = "INSERT INTO messages (sender_id, receiver_id, text, image_url, created_at, updated_at) VALUES (? ,? ,? ,? ,? ,?)"
            res = accion(sql, (sender_id, receiver_id, message_text, image_url, created_at, updated_at))

            if res == 0:
                print('Could not send message.', res)
                return jsonify({'error': 'Could not send message.'}), 400
            else:
                return jsonify({'message': 'Message sent successfully.'}), 200
    
        logged_user_avatar = session['urlava']
        receiver_sql = f"SELECT nombre, apellidos, urlavatar FROM usuarios WHERE id='{receiver_id}'"
        receiver_response = seleccion(receiver_sql)
            
        formatted_receiver = {
            'name': receiver_response[0][0],
            'last_name': receiver_response[0][1],
            'url_avatar': receiver_response[0][2]
        }
            
        return render_template('send-message.html', form_send_message=frm_send_message, form_search=frm_search, receiver=formatted_receiver, logged_user_avatar=logged_user_avatar, include_header=True)  
                
        