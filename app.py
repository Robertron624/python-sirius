import os
from flask import Flask, render_template, request, session, redirect, jsonify, url_for, make_response
from datetime import datetime, timedelta

from formularios import Search, Help
from db import seleccion
from utilidades import escape_html

from routes.user_routes import user_blueprint
from routes.comment_routes import comment_blueprint
from routes.post_routes import post_blueprint
from routes.auth_routes import auth_blueprint
from routes.message_routes import message_blueprint

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.errorhandler(404)
def error404(e):
    return render_template('404.html'), 404

app.register_blueprint(user_blueprint)
app.register_blueprint(comment_blueprint)
app.register_blueprint(post_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(message_blueprint)

@app.route('/busqueda/<string:search_text>', methods=['POST', 'GET'])
def search(search_text=None):
    if 'id' not in session:
        return redirect('/')
    else:
        frm_search = Search()
        if request.method == 'GET':
            
            sanitized_search_text = escape_html(search_text)
            
            # Search for user name in database
            user_search = str(sanitized_search_text).capitalize()
            user_search_sql = f"SELECT id, nombre, apellidos, urlavatar FROM usuarios WHERE nombre = '{user_search}' OR apellidos = '{user_search}'"
            response_user_search = seleccion(user_search_sql)
            
            if response_user_search:
                users_found = [dict(id=user[0], name=user[1], last_name=user[2], url_avatar=user[3]) for user in response_user_search]
            else:
                users_found = []

            # Search for the text in the post
            post_text_search = f"%{str(sanitized_search_text).lower()}%"
            sql_post_search = f"SELECT DISTINCT id, correo,nombre,apellido, datepost, text, url, sexo, urlavatar FROM post WHERE LOWER(text) LIKE '{post_text_search}'"
            response_post_search = seleccion(sql_post_search)
            
            if response_post_search:
                posts_found = [dict(id=post[0], email=post[1], name=post[2], last_name=post[3], date=post[4], text=post[5], image_url=post[6]) for post in response_post_search]
            else:
                posts_found = []
                
            print("POSTS FOUND: ", posts_found)
            
            results_count = len(users_found) + len(posts_found)
                
            return render_template('search-result.html', form_search=frm_search, search_text=sanitized_search_text, users_found=users_found, posts_found=posts_found, include_header=True, results_count = results_count)

        else:
            search_text = request.form['search_text'].capitalize()
            return redirect(f'/busqueda/{search_text}')

@app.route('/ayuda/', methods=['GET', 'POST'])
def help():
    frm = Help()
    if request.method == 'POST':
        help_username = request.form.get('help_username')
        help_doubt = request.form.get('help_doubt')
        
        is_data_valid = (help_username != "") and (help_doubt != "")
        
        if not is_data_valid:
            return jsonify({"message": "El usuario y el mensaje son obligatorios"}), 400
        else:
            print(f"Ayuda enviada por {help_username} con el mensaje: {help_doubt}")
            
            return jsonify({"message": "Ayuda enviada correctamente"}), 200
    return render_template("help.html", form=frm, title="Ayuda")

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages = []
    ten_days_ago = (datetime.now() - timedelta(days=10)).date().isoformat()
    
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and rule.defaults is not None and len(rule.defaults) >= len(rule.arguments):
            pages.append(
                [url_for(rule.endpoint, **(rule.defaults or {})), ten_days_ago]
            )
    
    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    
    return response


if __name__ == '__main__':
    app.run(debug=True, port=80)
