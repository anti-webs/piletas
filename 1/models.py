from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from db_config import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(256), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    service_requests = db.relationship('ServiceRequest', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username} ({self.full_name})>'

    def __init__(self, full_name, username, email, password_hash):
        self.full_name = full_name
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @classmethod
    def get(cls, id):
        return cls.query.get(int(id))

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
        
    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def create(cls, full_name, username, email, password):
        try:
            if cls.get_by_username(username) or cls.get_by_email(email):
                return False
            password_hash = generate_password_hash(password)
            user = cls(full_name=full_name, username=username, email=email, password_hash=password_hash)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            db.session.rollback()
            return False

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Pool model kept as a static list since it's catalog data
class Pool:
    pools = [
        {
            'id': 1,
            'name': 'Piscina Comercial',
            'description': 'Piscina comercial ideal para instalaciones deportivas y sociales.',
            
            
            'features': ['Carriles de competición', 'Control de temperatura', 'Sistema de filtración profesional', 'Iluminación subacuática'],
            'image_url': '/static/images/pools/pool_olympic.jpeg'
        },
        {
            'id': 2,
            'name': 'Piscina Familiar',
            'description': 'Piscina rectangular perfecta para jardines familiares.',
            
            
            'features': ['Escalera de acceso', 'Sistema de filtración', 'Skimmers'],
            'image_url': '/static/images/pools/pool_family.jpg'
        },
        {
            'id': 3,
            'name': 'Piscina Infinity',
            'description': 'Piscina de borde infinito con vistas panorámicas espectaculares.',
            
            
            'features': ['Borde infinito', 'Control de temperatura', 'Sistema de filtración', 'Skimmers', 'Iluminación LED multicolor'],
            'image_url': '/static/images/pools/pool_infinity.jpg'
        },
        {
            'id': 4,
            'name': 'Piscina Spa',
            'description': 'Combinación de piscina y spa con chorros de hidromasaje.',
            
            
            'features': ['Hidromasaje', 'Calefacción', 'Luces LED multicolor'],
            'image_url': '/static/images/pools/pool_spa.jpeg'
        },
        {
            'id': 5,
            'name': 'Piscina Infantil',
            'description': 'Piscina de poca profundidad ideal para niños pequeños.',
            
            
            'features': ['Profundidad gradual', 'Sistema de filtración', 'Fácil acceso'],
            'image_url': '/static/images/pools/pool_kids.jpg'
        }
    ]
    
    @classmethod
    def get_all(cls):
        return cls.pools
    
    @classmethod
    def get(cls, pool_id):
        for pool in cls.pools:
            if pool['id'] == int(pool_id):
                return pool
        return None

# Database model for service requests
class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact_info = db.Column(db.JSON, nullable=False)
    pool_id = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default='Pendiente')
    
    @classmethod
    def create(cls, user_id, title, description, contact_info, pool_id=None):
        service_request = cls(
            user_id=user_id,
            title=title,
            description=description,
            contact_info=contact_info,
            pool_id=pool_id
        )
        db.session.add(service_request)
        db.session.commit()
        return service_request
    
    @classmethod
    def get_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    @classmethod
    def create(cls, name, email, phone, message):
        contact_message = cls(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        db.session.add(contact_message)
        db.session.commit()
        return contact_message