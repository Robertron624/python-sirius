from flask import Blueprint, redirect, render_template, request, session, jsonify
from db import eliminarimg, seleccion, accion
from formularios import Search, Message
from utilidades import format_datetime
from datetime import datetime

message_blueprint = Blueprint('message', __name__)

@message_blueprint.route('/delete-message/<int:id>/', methods=['DELETE'])
def delete_message(id=None):
    if 'id' not in session:
        return jsonify({'error': 'User not logged in'}), 401
    else:
        
        user_id = session['id']
        
        sql_check_author = f"SELECT receiver_id FROM messages WHERE id IN ({id})"
        res_check_author = seleccion(sql_check_author)
        
        if not res_check_author or res_check_author[0][0] != user_id:
            return jsonify({'error': 'User not authorized to delete message'}), 401
        
        sql = f"DELETE FROM messages WHERE id IN ({id})"
        resultado = eliminarimg(sql)
        if resultado == 0:
            return jsonify({'error': 'Message not found or user not authorized to delete'}), 404
        else:
            return jsonify({'message': 'Message deleted successfully'}), 200
        
@message_blueprint.route('/mensajes', methods=['GET', 'POST'])
def private_messages(id=None):
    if 'id' not in session:
        return redirect('/')
    else:
        frm_search = Search()
        if request.method == 'GET':
            user_id = session['id']
            sql = f"""
                SELECT u.nombre, u.apellidos, m.id, m.text, m.image_url, m.created_at, m.updated_at
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
                    'id': row[2],
                    'text': row[3],
                    'image_url': row[4],
                    'created_at': format_datetime(row[5]),
                    'updated_at': format_datetime(row[6])
                } for row in response]
                
            return render_template('private-messages.html',
                                   form_search=frm_search, message_list=message_list, titulo='Mensajes privados', include_header=True)
        else:
            search_text = request.form['search_text'].capitalize()
            return redirect(f'/busqueda/{search_text}')


@message_blueprint.route('/enviar-mensaje/<int:receiver_id>/', methods=['GET', 'POST'])
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