from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import random

class User(db.Model):
    """Modello per gli utenti"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    salt = db.Column(db.Integer)

    def set_password(self, password):
        """Genera password hash con salt"""
        self.salt = random.randint(10000, 99999)
        self.password = generate_password_hash(f"{password}{self.salt}", method='pbkdf2:sha256')

    def check_password(self, password):
        """Verifica la password"""
        return check_password_hash(self.password, f"{password}{self.salt}")

class Corsi(db.Model):
    """Modello per i corsi"""
    __tablename__ = 'corsi'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.Text, nullable=False)
    prezzo = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Corso {self.nome}>'