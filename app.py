import os
from flask import Flask, render_template, request, session, flash, redirect

from formularios import Busqueda, Roles, Mensaje, Ayuda
from db import accion, editarimg, seleccion

from routes.user_routes import user_blueprint
from routes.comment_routes import comment_blueprint
from routes.post_routes import post_blueprint
from routes.auth_routes import auth_blueprint

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.errorhandler(404)
def error404(e):
    return render_template('404.html'), 404

app.register_blueprint(user_blueprint)
app.register_blueprint(comment_blueprint)
app.register_blueprint(post_blueprint)
app.register_blueprint(auth_blueprint)

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
                return render_template('search-result.html', titulo='Resultados de la búsqueda', userList=res, imglist=res2, ava=sex, form=frm, idreceptor=msg_receptor)
            except Exception:
                return render_template('search-result.html', titulo='Resultados de la búsqueda', userList=res, imglist=res2, ava=sex, form=frm)

        else:
            texto = request.form['texto'].capitalize()
            return redirect(f'/busqueda/{texto}')

@app.route('/ayuda/')
def ayuda():
    frm = Ayuda()
    return render_template("help.html", form=frm, titulo="Ayuda")

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
