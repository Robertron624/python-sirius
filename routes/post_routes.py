import os
from flask import Blueprint, redirect, render_template, request, session, jsonify
from db import eliminarimg, accion, seleccion, editarimg
from werkzeug.utils import secure_filename
from markupsafe import escape
from datetime import datetime
from formularios import New_Post, Search, New_Comment, Edit_Post
from random import randint
from utilidades import format_datetime, format_comment_datetime

#create a Blueprint for post-related routes

post_blueprint = Blueprint('post', __name__)
@post_blueprint.route('/publicacion/<int:id>/', methods=['GET', 'POST'])
def post_page(id=None):
    if 'id' not in session:
        return redirect('/')
    else:
        frm_search = Search()
        frm_comentar = New_Comment()
        if request.method == 'GET':
            sql = f"SELECT nombre, apellido, correo, datepost, text, url FROM post WHERE id='{id}'"
            res = seleccion(sql)
            
            # If the post does not exist, redirect to 404 page
            if len(res) == 0:
                return render_template('404.html'), 404
                        
            correo = res[0][2]
            
            sql2 = f"SELECT correo,sexo FROM usuarios WHERE correo='{correo}'"
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
                'apellidos':    tuple_values[0],
                'datepost': format_datetime(tuple_values[2]),
                'text': tuple_values[3],
                'url': tuple_values[4]
            }

            urlava = ''
            if sex == "H":
                urlava = "avatares/hombre-barba.jpg"
            elif sex == "M":
                urlava = "avatares/mujer1.jpg"
            elif sex == "P":
                urlava = "avatares/otro.png"

            # Get comments
            sql3 = f"SELECT id,correo,nombre, apellidos, text, datecomment, urlavatar FROM comment WHERE idpost='{id_img}'"
            res3 = seleccion(sql3)
            
            if len(res3) == 0:
                formatted_comments_data = []
            else:
                formatted_comments_data = [{ 'id': row[0],
                                            'correo': row[1],
                                            'nombre': row[2],
                                            'apellidos': row[3],
                                            'text': row[4],
                                            'datecomment': format_comment_datetime(row[5]),
                                            'urlavatar': row[6] } for row in res3]
            html_title = f"Publicación de {post_data['nombre']} {post_data['apellidos']}"

            return render_template('post-page.html', titulo=html_title, postInfo=post_data, ava=urlava, owner=img_owner, id_img=id_img, form_search=frm_search, form_comentar=frm_comentar, commentList=formatted_comments_data, include_header=True)
        elif request.method == 'POST' and 'search_text' in request.form:
            search_text = request.form['search_text'].capitalize()
            return redirect(f'/busqueda/{search_text}')

@post_blueprint.route('/nueva-publicacion/', methods=['POST', 'GET'])
def new_post():
    if 'id' not in session:
        return redirect('/')
    else:
        frm_new_post = New_Post()
        frm_search = Search()
        if request.method == 'GET':
            sex = session["urlava"]
            return render_template('new-post.html', titulo='Subir publicación', form_new_post=frm_new_post, ava=sex, form_search=frm_search, include_header=True)
        elif request.method == 'POST':

            if frm_new_post.validate_on_submit():
                file = frm_new_post.post_file.data
                text = escape(frm_new_post.post_text.data).capitalize()
                
                parsed_filename = secure_filename(file.filename)
                
                if os.path.isfile(f"static/uploads/{parsed_filename}"):
                    random_name = str(randint(1, 5000))
                    final_filename = random_name + parsed_filename
                else:
                    final_filename = parsed_filename
                    
                url_img = f"/uploads/{final_filename}"
                
                try:
                    file.save(f"static{url_img}")
                except Exception as e:
                    return jsonify({'error': 'Error while trying to save the image, try again'}), 500
                
                user = session['ema']
                first_name = session['nom']
                last_name = session['ape']
                sex = session['sex']
                url_avatar = session['urlava']
                today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                
                sql = 'INSERT INTO post(correo, nombre, apellido, datepost, text, url, sexo, urlavatar) VALUES(?, ?, ?, ?, ?, ?, ?, ?)'
                resultado = accion(sql, (user, first_name, last_name, today, text, url_img, sex, url_avatar))
                
                print("resultado -> ", resultado)
                
                if resultado == 0:
                    return jsonify({'error': 'Error al guardar la publicación, intente de nuevo'}), 500
                
                return jsonify({'success': 'Publicación guardada correctamente', 'url': url_img}), 200
            else:
                errors = frm_new_post.errors
                print("errors -> ", errors)
                return jsonify({'error': 'Formulario inválido', 'errors': errors}), 400
        elif request.method == 'POST' and 'search_text' in request.form:
            search_text = request.form['search_text'].capitalize()
            return redirect(f'/busqueda/{search_text}')

@post_blueprint.route('/editar/<int:id>', methods=['GET', 'POST', 'PUT'])
def edit_post(id=None):
    if 'id' not in session:
        return redirect('/')
    else:
        frm_edit_post = Edit_Post()
        frm_search = Search()
        if request.method == 'GET':
            idImg = id
            sex = session["urlava"]
            sql_url = f"SELECT text from post WHERE id='{id}'"
            res = seleccion(sql_url)
            
            if len(res) != 0:
                frm_edit_post.edited_text.data = res[0][0]
            
            return render_template('edit-post.html', titulo='Editar publicación', form_edit_post=frm_edit_post, ava=sex, id_img=idImg, form_search=frm_search, include_header=True)
        elif request.method == 'POST' and 'search_text' in request.form:
            search_text = request.form['search_text'].capitalize()
            return redirect(f'/busqueda/{search_text}')
        elif request.method == 'PUT':
            
            user_email = session['ema']
        
            sql_check_author = f"SELECT correo FROM post WHERE id = {id}"
            res_check_author = seleccion(sql_check_author)
            
            if not res_check_author or res_check_author[0][0] != user_email:
                return jsonify({'error': 'User not authorized to edit post'}), 401
            
            data = request.get_json()
            text = escape(data.get('edited_text', '')).capitalize()
            sql = f"UPDATE post SET text='{text}' WHERE id='{id}'"
            
            try:
                res = editarimg(sql)
                
                if res == 0:
                    print('Error while trying to save: ', res)
                    return jsonify({'error': 'Error al editar la publicación, intente de nuevo'}), 500
                      
                return jsonify({'success': 'Publicación editada correctamente'}), 200
                
            except Exception as e:
                return jsonify({'error': 'Error al editar la publicación, intente de nuevo'}), 500
            
@post_blueprint.route('/eliminar-post/<int:id>', methods=['DELETE'])
def eliminar(id=None):
    if 'id' not in session:
        return redirect('/')
    else:
        
        user_email = session['ema']
        
        sql_check_author = f"SELECT correo FROM post WHERE id = {id}"
        res_check_author = seleccion(sql_check_author)
        
        if not res_check_author or res_check_author[0][0] != user_email:
            return jsonify({'error': 'User not authorized to delete post'}), 401
        
        sql = f"DELETE FROM post WHERE id IN ({id})"
        resultado = eliminarimg(sql)
        if resultado == 0:
            return jsonify({'error': 'Post not found or user not authorized to delete'}), 404
        else:
            return jsonify({'message': 'Post deleted successfully'}), 200