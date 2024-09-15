from flask import Flask, render_template, request, redirect, url_for, session as login_session
from engine.database_fetchall import DatabaseFetchAll
from controllers.usuarios_controller import UsuarioController
from controllers.especialidades_controller import EspecialidadeController
# from controllers.medicos_controller import MedicosController
from controllers.medico_controller import MedicoController
from engine.config_db import DatabaseConfig

app = Flask(__name__)
app.secret_key = '1245fvcx323423423dfdscxvxvcxgerr43'

# Configuração do banco de dados e instância do DatabaseFetchAll
config = DatabaseConfig()
DATABASE_URL = config.get_uri()
db_fetch_all = DatabaseFetchAll(DATABASE_URL)

# Inicialização dos controladores com a conexão configurada
usuario_controller = UsuarioController(db_fetch_all)
especialidade_controller = EspecialidadeController(db_fetch_all)
# medicos_controller = MedicosController(db_fetch_all)
medico_controller = MedicoController(db_fetch_all)


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


@app.route('/especialidades', methods=['GET', 'POST'])
def especialidades():
    if 'user_id' in login_session:
        if request.method == 'POST':
            nome = request.form['nome']
            if nome:
                especialidade_controller.create_especialidade(nome)
                return redirect(url_for('especialidades'))  # Evitar reenvio do formulário
        especialidades = especialidade_controller.read_especialidades()
        return render_template('especialidades.html', especialidades=especialidades)
    return redirect(url_for('login'))


@app.route('/especialidades/excluir/<int:id>', methods=['POST'])
def excluir_especialidade(id):
    especialidade_controller.delete_especialidade(id)
    return redirect(url_for('especialidades'))


@app.route('/especialidades/editar/<int:id>', methods=['GET', 'POST'])
def editar_especialidade(id):
    if request.method == 'POST':
        new_nome = request.form['nome']
        especialidade_controller.update_especialidade(id, new_nome)
        return redirect(url_for('especialidades'))
    else:
        especialidades = especialidade_controller.read_especialidades()
        especialidade = next((e for e in especialidades if e['id'] == id), None)
        if especialidade:
            return render_template('editar_especialidade.html', especialidade=especialidade)
        return redirect(url_for('especialidades'))


@app.route('/profile')
def profile():
    if 'user_id' in login_session:
        user_id = login_session['user_id']
        user_info = usuario_controller.get_user_info(user_id)  # Assumindo que essa função existe
        return render_template('profile.html', user_info=user_info)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    login_session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/medico')
def listar_medicos():
    # Obtém a lista de médicos do MedicoController
    medicos = medico_controller.listar_medicos()
    return render_template('medico.html', medicos=medicos)

@app.route('/medicos/novo', methods=['POST'])
def novo_medico():
    if 'user_id' in login_session:
        nome = request.form['nome']
        crm = request.form['crm']
        especialidade_id = request.form.get('especialidade', 1)
        medico_controller.inserir_medico(nome, crm, [especialidade_id])
        return redirect(url_for('list_medicos'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
