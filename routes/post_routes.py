import os
from flask import Blueprint, redirect, render_template, request, session, flash
from db import eliminarimg, accion, seleccion, editarimg
from werkzeug.utils import secure_filename
from markupsafe import escape
from datetime import datetime
from formularios import Publicacion, Busqueda, Comentario, EditPublicacion
from random import randint
from utilidades import format_datetime, format_comment_datetime

#create a Blueprint for post-related routes

post_blueprint = Blueprint('post', __name__)
@post_blueprint.route('/publicacion/<int:id>/', methods=['GET'])
def publicacion(id=None):
    if 'id' not in session:
        return redirect('/')
    else:
        frm_search = Busqueda()
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
                'datepost': format_datetime(tuple_values[1]),
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

            return render_template('publicacion.html', titulo=html_title, postInfo=post_data, ava=urlava, owner=img_owner, id_img=id_img, form_search=frm_search, form_comentar=frm_comentar, commentList=formatted_comments_data, include_header=True)
        elif request.method == 'POST' and 'texto' in request.form:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')

@post_blueprint.route('/nueva_publicacion/', methods=['POST', 'GET'])
def nueva_publi():
    if 'id' not in session:
        return redirect('/')
    else:
        frm_new_post = Publicacion()
        frm_search = Busqueda()
        if request.method == 'GET':
            sex = session["urlava"]
            return render_template('nueva_publicacion.html', titulo='Subir publicación', form_new_post=frm_new_post, ava=sex, form_search=frm_search, include_header=True)
        elif request.method == 'POST' and 'publish' in request.form:
            f = request.files['adj']
            nom2 = secure_filename(f.filename)
            if os.path.isfile(f'uploads/{nom2}'):
                name = str(randint(1, 5000))
                usr = session['ema']
                nom = session["nom"]
                ape = session["ape"]
                sex = session["sex"]
                urlava = session["urlava"]
                
                today = datetime.today()
                year = today.year
                month = today.month
                day = today.day
                hour = today.hour
                minute = today.minute
                fecpost = datetime(year, month, day, hour, minute)
                text = escape(request.form['publi'].capitalize())
                urlimg = f'/uploads/{name+nom2}'

                f.save(f'static/uploads/{name+nom2}')
                sql = 'INSERT INTO post(correo, nombre, apellido, datepost, text, url,sexo,urlavatar) VALUES(?, ?, ?, ?, ?, ?, ?, ?)'
                res = accion(sql, (usr, nom, ape, fecpost,
                                   text, urlimg, sex, urlava))
                return render_template('nueva_publicacion.html', titulo='Subir publicación', form_new_post=frm_new_post, ava=urlava, form_search=frm_search, include_header=True)
            else:
                usr = session['ema']
                nom = session["nom"]
                ape = session["ape"]
                urlava = session["urlava"]
                sex = session["sex"]
                urlava = session["urlava"]
                
                today = datetime.today()
                
                year = today.year
                month = today.month
                day = today.day
                hour = today.hour
                minutes = today.minute
                fecpost = datetime(year, month, day, hour, minutes)
                text = escape(request.form['publi'])
                urlimg = f'/uploads/{nom2}'

                f.save(f'static/uploads/{nom2}')
                sql = 'INSERT INTO post(correo, nombre, apellido, datepost, text, url,sexo,urlavatar) VALUES(?, ?, ?, ?, ?, ?, ?, ?)'
                res = accion(sql, (usr, nom, ape, fecpost,
                                   text, urlimg, sex, urlava))
                
                print(res)
                return render_template('nueva_publicacion.html', titulo='Subir publicación', form_new_post=frm_new_post, ava=urlava, form_search=frm_search, include_header=True)
        elif request.method == 'POST' and 'texto' in request.form:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')

@post_blueprint.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id=None):
    if 'id' not in session:
        return redirect('/')
    else:
        frm_edit_post = EditPublicacion()
        frm_search = Busqueda()
        if request.method == 'GET':
            idImg = id
            sex = session["urlava"]
            sql_url = f"SELECT url from post WHERE id='{id}'"
            res = seleccion(sql_url)
            url_img = res[0][0]
            return render_template('editar_publicacion.html', titulo='Editar publicación', form_edit_post=frm_edit_post, ava=sex, id_img=idImg, ruta=url_img, form_search=frm_search, include_header=True)
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

@post_blueprint.route('/eliminarpost/<int:id>', methods=['DELETE'])
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