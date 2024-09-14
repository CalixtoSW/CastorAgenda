from flask import Flask, render_template, request, redirect, url_for, session as login_session
from engine.database_fetchall import DatabaseFetchAll
from controllers.usuarios_controller import UsuarioController
from engine.config_db import DatabaseConfig

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'

# Configuração do banco de dados usando DatabaseConfig
config = DatabaseConfig()
DATABASE_URL = config.get_uri()

# Instanciando DatabaseFetchAll com a string de conexão
db_fetch_all = DatabaseFetchAll(DATABASE_URL)
usuario_controller = UsuarioController(db_fetch_all)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if usuario_controller.authenticate(username, password):
            login_session['user_id'] = username
            return redirect(url_for('agenda'))
        return 'Login inválido!'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario_controller.create_usuario(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/agenda')
def agenda():
    if 'user_id' in login_session:
        return render_template('agenda.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    login_session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
