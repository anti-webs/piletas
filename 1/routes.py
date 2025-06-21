from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from models import User, Pool, ServiceRequest, ContactMessage
from forms import RegisterForm, LoginForm, ServiceRequestForm, ContactForm
from functools import wraps

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.create(form.full_name.data, form.username.data, form.email.data, form.password.data)
        if user:
            flash('¡Cuenta creada con éxito! Ahora puede iniciar sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error al crear la cuenta. El nombre de usuario o email ya está en uso.', 'danger')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Check if input is an email or username
        login_id = form.username.data
        
        # Try to find the user
        user = None
        # First try by email if it looks like an email
        if login_id and isinstance(login_id, str) and '@' in login_id:
            # Login with email
            user = User.get_by_email(login_id)
        else:
            # Login with username
            user = User.get_by_username(login_id)
            
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('¡Sesión iniciada correctamente!', 'success')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Usuario/Email o contraseña incorrectos. Por favor intente de nuevo.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ha cerrado sesión.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    service_requests = ServiceRequest.get_by_user(current_user.id)
    pools = Pool.get_all()
    return render_template('dashboard.html', service_requests=service_requests, pools=pools)

@app.route('/gallery')
def gallery():
    pools = Pool.get_all()
    return render_template('gallery.html', pools=pools)

@app.route('/service_request', methods=['GET', 'POST'])
@login_required
def service_request():
    form = ServiceRequestForm()
    pool_id = request.args.get('pool_id')
    pools = Pool.get_all()
    
    if pool_id:
        pool = Pool.get(pool_id)
        form.pool_id.data = pool_id
    else:
        pool = None
    
    if form.validate_on_submit():
        contact_info = {
            'email': form.email.data,
            'phone': form.phone.data
        }
        ServiceRequest.create(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            contact_info=contact_info,
            pool_id=form.pool_id.data if form.pool_id.data else None
        )
        flash('Solicitud de servicio enviada con éxito. Nos pondremos en contacto con usted pronto.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('service_request.html', form=form, pool=pool, pools=pools)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            ContactMessage.create(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                message=form.message.data
            )
            flash('Su mensaje ha sido enviado. Nos pondremos en contacto con usted pronto.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            app.logger.error(f"Error al guardar mensaje de contacto: {str(e)}")
            flash(f'Error al enviar mensaje: {str(e)}. Por favor intente nuevamente o contáctenos por teléfono.', 'danger')
            return render_template('contact.html', form=form)
    return render_template('contact.html', form=form)

# Admin functions
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        # For simplicity, we'll use the first registered user as admin
        # In a real app, you would have an admin flag in the user model
        if current_user.id != 1:
            flash('Acceso denegado. Se requieren privilegios de administrador.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.get_all()
    return render_template('admin/users.html', users=users)

@app.route('/api/users')
@admin_required
def api_users():
    users = User.get_all()
    users_list = []
    for user in users:
        users_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name
        })
    return jsonify(users_list)
