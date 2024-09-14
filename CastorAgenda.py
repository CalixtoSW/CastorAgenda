# Castor_Agenda/app.py
from flask import Flask, render_template, request, redirect, url_for, session
from engine.database_fetchall import DatabaseFetchAll
# Importe outros controladores conforme necessário

app = Flask(__name__)
app.secret_key = '123ghgfd7&#2kjjl564'

# Instâncias do DatabaseFetchAll e controladores devem ser inicializadas aqui
# Exemplo:
# db_fetch_all = DatabaseFetchAll(connection)
# especialidade_controller = EspecialidadeController(db_fetch_all)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lógica de autenticação
        pass
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Lógica de registro
        pass
    return render_template('register.html')

@app.route('/agenda')
def agenda():
    if 'user_id' in session:
        return render_template('agenda.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
