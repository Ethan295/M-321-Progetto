from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from jinja2 import TemplateNotFound
from functools import wraps
from api import create_app, db
from api.models import User, Corsi

app = create_app()

# Decorator per route protette
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Per favore accedi per accedere a questa pagina', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Gestione sessione
@app.before_request
def before_request():
    session.permanent = True
    if 'logged_in' not in session:
        session['logged_in'] = False

# Route principali
@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    corsi = Corsi.query.all()
    return render_template('main.html', corsi=corsi)

# Autenticazione
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session.update({
                'user_id': user.id,
                'user_email': user.email,
                'user_name': user.nome,
                'logged_in': True
            })
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('user_token', user.email, max_age=60*60*24*7)
            flash('Login effettuato!', 'success')
            return resp
        flash('Credenziali non valide', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Password non coincidono', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('Email già registrata', 'danger')
        else:
            new_user = User(nome=nome, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registrazione completata!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    resp = make_response(redirect(url_for('home')))
    resp.delete_cookie('session')
    resp.delete_cookie('user_token')
    flash('Logout effettuato', 'info')
    return resp

# Gestione corsi
@app.route('/corso_intro')
def corso_intro():
    return render_template('corso_intro.html')

@app.route('/corso_survival')
def corso_survival():
    return render_template('corso_survival.html')

@app.route('/corso_redstone')
def corso_redstone():
    return render_template('corso_redstone.html')

@app.route('/corso_<nome>')
def corso(nome):
    corsi_map = {
        "introduzione_a_minecraft": "corso_intro.html",
        "modalita_survival": "corso_survival.html",
        "redstone": "corso_redstone.html"
    }
    
    nome_normalized = nome.lower().replace('à', 'a').replace('è', 'e')
    template = corsi_map.get(nome_normalized)
    
    if template:
        try:
            return render_template(template)
        except TemplateNotFound:
            pass
    return "Corso non trovato", 404

if __name__ == '__main__':
    app.run(debug=True)