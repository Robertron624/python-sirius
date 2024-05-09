from flask import Blueprint, redirect, request, session, jsonify
from db import get_last_comment_id, accion, eliminarimg
from datetime import datetime

#create a Blueprint for comment-related routes

comment_blueprint = Blueprint('comment', __name__)
@comment_blueprint.route('/new-comment/<int:id>/', methods=['POST'])
def create_comment(id=None):
    if 'id' not in session:
        return redirect('/')
    elif 'new_comment_text' not in request.form:
        return jsonify({'error-message': 'No comment text provided'}), 400
    else:
        comment_text = request.form['new_comment_text']
        emausuario = session['ema']
        nom = session['nom']
        ape = session['ape']
        urlava = session['urlava']
        fecpost = datetime.today()
        
        sql = 'INSERT INTO comment(correo, nombre, apellidos, text, datecomment, idpost, urlavatar) VALUES(?,?,?,?,?,?,?)'
        res = accion(sql, (emausuario, nom, ape, comment_text, fecpost, id, urlava))
        
        if res == 0:
            return jsonify({'error': 'Failed to save comment'}), 500
        else:
            
            new_comment_id = get_last_comment_id()
            
            comment_data = {
                'commentText': comment_text,
                'dateComment': fecpost.strftime('%B %d, %Y'),
                'userName': nom,
                'userLastName': ape,
                'userEmail': emausuario,
                'urlAvatar': urlava,
                'id': new_comment_id[0]
            }
            
            return jsonify({'message': 'Comment saved successfully', 'commentData': comment_data}), 200
        

    
@comment_blueprint.route('/eliminarcomment/<int:idpost>/<int:idcomment>', methods=['DELETE'])
def eliminarcomment(idpost=None, idcomment=None):
    try: 
        sql = f"DELETE FROM comment WHERE idpost = {idpost} AND id = {idcomment}"
        resultado = eliminarimg(sql)
        print("RESULT OF DELETE: ", resultado)
        if resultado == 0:
            return jsonify({'error': 'Comment not found or user not authorized to delete'}), 404
        else:
            return jsonify({'message': 'Comment deleted successfully'}), 200
    except Exception as e:
        print('Error: ', e)
        return jsonify({'error': 'Internal server error'}), 500