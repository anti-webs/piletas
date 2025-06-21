from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, EmailField, TelField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp
from models import User
import re

class RegisterForm(FlaskForm):
    full_name = StringField('Nombre Completo', validators=[
        DataRequired(message="El nombre completo es obligatorio."),
        Length(min=5, max=50, message="El nombre completo debe tener entre 5 y 50 caracteres."),
        Regexp(r'^[A-Za-zÁáÉéÍíÓóÚúÑñ\s]+$', message="El nombre solo puede contener letras y espacios.")
    ])
    username = StringField('Usuario', validators=[DataRequired(message="El usuario no puede estar vacío."), 
                                                 Length(min=3, max=20, message="El usuario debe tener entre 3 y 20 caracteres.")])
    email = EmailField('Email (Gmail)', validators=[
        DataRequired(message="Por favor ingrese su dirección de correo electrónico."),
        Email(message="Por favor ingrese una dirección de correo electrónico válida."),
        Regexp(r'.*@gmail\.com$', message="Solo se permiten direcciones de Gmail (@gmail.com).")
    ])
    password = PasswordField('Contraseña', validators=[DataRequired(message="La contraseña no puede estar vacía."),
                                                     Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")])
    confirm_password = PasswordField('Confirmar Contraseña', 
                                    validators=[DataRequired(message="La confirmación no puede estar vacía."),
                                              EqualTo('password', message="Las contraseñas no son iguales.")])
    submit = SubmitField('Crear Cuenta')

    def validate_username(self, username):
        user = User.get_by_username(username.data)
        if user:
            raise ValidationError('Este nombre de usuario ya está en uso. Por favor elija otro.')
            
    def validate_email(self, email):
        # Check if a user with this email already exists
        user = User.get_by_email(email.data)
        if user:
            raise ValidationError('Este email ya está registrado. Por favor utilice otro.')
            
        # Additional validation to make sure it's a Gmail address
        if not email.data.lower().endswith('@gmail.com'):
            raise ValidationError('Solo se permiten direcciones de Gmail (@gmail.com).')

class LoginForm(FlaskForm):
    username = StringField('Usuario o Email', validators=[DataRequired(message="El usuario o email no puede estar vacío.")])
    password = PasswordField('Contraseña', validators=[DataRequired(message="La contraseña no puede estar vacía.")])
    submit = SubmitField('Iniciar Sesión')

class ServiceRequestForm(FlaskForm):
    title = StringField('Título de la Solicitud', validators=[DataRequired(message="Por favor ingrese un título para su solicitud.")])
    description = TextAreaField('Descripción', validators=[DataRequired(message="Por favor describa su solicitud.")])
    email = EmailField('Email de Contacto', validators=[DataRequired(message="Por favor ingrese su email."), 
                                                      Email(message="Por favor ingrese un email válido.")])
    phone = TelField('Teléfono de Contacto', validators=[DataRequired(message="Por favor ingrese su número de teléfono.")])
    pool_id = HiddenField('ID de Piscina')
    submit = SubmitField('Enviar Solicitud')

class ContactForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(message="Por favor ingrese su nombre.")])
    email = EmailField('Email', validators=[DataRequired(message="Por favor ingrese su email."), 
                                          Email(message="Por favor ingrese un email válido.")])
    phone = TelField('Teléfono', validators=[DataRequired(message="Por favor ingrese su número de teléfono.")])
    message = TextAreaField('Mensaje', validators=[DataRequired(message="Por favor ingrese su mensaje.")])
    submit = SubmitField('Enviar Mensaje')
