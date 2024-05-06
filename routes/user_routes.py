from flask import Blueprint, redirect, render_template, request, session
from db import seleccion
from formularios import Busqueda
from utilidades import format_datetime

#create a Blueprint for user-related routes

user_routes = Blueprint('user', __name__)

@user_routes.route('/perfil/', methods=['GET', 'POST'])
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

            return render_template('perfilusr.html', titulo='Mi perfil', ava=sex, form=frm, postList=formatted_results)
        else:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')
