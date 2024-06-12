from typing import ValuesView
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField
from wtforms import validators
from wtforms.fields.choices import RadioField
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import FileField, TextAreaField, EmailField, SearchField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo


class Login(FlaskForm):
    login_user = EmailField('Usuario *', validators=[Length(
        min=5, max=40, message='Longitud fuera de rango'), InputRequired(message='Usuario es requerido')])
    login_password = PasswordField('Clave *', validators=[Length(
        min=5, max=40, message='Longitud fuera de rango'), InputRequired(message='Clave es requerido')])
    enter = SubmitField('Ingresar')


class Signup(FlaskForm):
    signup_first_name = StringField('Nombre *', validators=[Length(
        min=1, max=100, message='Longitud fuera de rango'), InputRequired(message='Nombre es requerido')])
    signup_last_name = StringField('Apellido *', validators=[Length(
        min=1, max=100, message='Longitud fuera de rango'), InputRequired(message='Apellido es requerido')])
    signup_email = EmailField('Email *', validators=[Length(
        min=3, max=100, message='Longitud fuera de rango'), InputRequired(message='Email es requerido')])
    signup_confirm_email = EmailField('Confirmar email *', validators=[Length(
        min=3, max=100, message='Longitud fuera de rango'), InputRequired(message='Email es requerido'),
        EqualTo(signup_email, message='Email y su verificación no corresponden')])
    signup_password = PasswordField('Clave *', validators=[Length(
        min=5, max=40, message='Longitud fuera de rango'), InputRequired(message='Clave es requerida')])
    signup_confirm_password = PasswordField('Verificación *', validators=[Length(min=5, max=40, message='Longitud fuera de rango'), InputRequired(
        message='Clave es requerido'), EqualTo(signup_password, message='La clave y su verificación no corresponden')])
    signup_birthdate = DateField(
        format="%d-%m-%y", validators=[DataRequired(message='Fecha de nacimiento requerida.')])
    signup_sex = RadioField('Label', choices=[
                     ('M', 'Mujer'), ('H', 'Hombre'), ('P', 'Otro')], default="P")
    signup_submit = SubmitField('Registrar')


class Password_Recovery(FlaskForm):
    usr = EmailField('Usuario *', validators=[Length(
        min=5, max=40, message='Longitud fuera de rango'), InputRequired(message='Usuario es requerido')])
    cema = EmailField('Confirmar email *', validators=[Length(
        min=3, max=100, message='Longitud fuera de rango'), InputRequired(message='Email es requerido'),
        EqualTo(usr, message='Email y su verificación no corresponden')])
    btn = SubmitField('Recuperar')


class Help(FlaskForm):
    help_username = EmailField('Usuario *', validators=[Length(
        min=5, max=40, message='Longitud fuera de rango'), InputRequired(message='Usuario es requerido')])
    help_doubt = TextAreaField(
        validators=[Length(min=3), InputRequired(message='Usuario es requerido')])
    help_submit = SubmitField('Enviar')


class New_Post(FlaskForm):
    post_text = TextAreaField('Texto')
    post_file = FileField('Seleccionar archivo', validators=[
        FileRequired(message='Archivo es requerido'),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Solo se permiten imágenes!')
    ])
    publish = SubmitField('Publicar')


class Edit_Post(FlaskForm):
    edited_text = TextAreaField('Texto')
    save_edit = SubmitField('Guardar cambios')


class Search(FlaskForm):
    search_text = SearchField()


class New_Comment(FlaskForm):
    new_comment_text = TextAreaField()
    new_comment_btn = SubmitField('Comentar')


class Message(FlaskForm):
    message_text = TextAreaField('Mensaje *', validators=[Length( min=1, max=500, message='Longitud fuera de rango'), InputRequired(message='Mensaje es requerido')])
    attached_image = FileField('Seleccionar archivo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Solo se permiten adjuntar imágenes!')
    ])
    submit_message_button = SubmitField('Enviar')


class Edit_user(FlaskForm):
    edit_first_name = StringField('Nombre *', validators=[Length(
        min=1, max=100, message='Longitud fuera de rango'), InputRequired(message='Nombre es requerido')])
    edit_last_name = StringField('Apellido *', validators=[Length(
        min=1, max=100, message='Longitud fuera de rango'), InputRequired(message='Apellido es requerido')])
    edit_password = PasswordField('Clave *', validators=[Length( min=5, max=40, message='Longitud fuera de rango'), InputRequired(message='Clave es requerida')])
    edit_birthdate = DateField(
        format="%d-%m-%y", validators=[DataRequired(message='Fecha de nacimiento requerida.')])
    edit_sex = RadioField('Label', choices=[
                     ('M', 'Mujer'), ('H', 'Hombre'), ('P', 'Otro')], default="P")
    edit_submit = SubmitField('Guardar cambios')

class Change_password(FlaskForm):
    previous_password = PasswordField(None, validators=[Length(
        min=5, max=40, message='Longitud fuera de rango'), InputRequired(message='Clave es requerido')])
    new_password = PasswordField(None, validators=[Length(
        min=5, max=40, message='Longitud fuera de rango'), InputRequired(message='Clave es requerido')])
    new_password_confirm = PasswordField(None, validators=[Length(
        min=5, max=40, message='Longitud fuera de rango'), InputRequired(message='Clave es requerido')])
    submit_new_password = SubmitField('Cambiar')

class Roles(FlaskForm):
    btn_admin = SubmitField('Administrador')
    btn_user = SubmitField('Usuario')


