from flask import Flask, render_template, request, redirect, url_for, session as login_session
from engine.database_fetchall import DatabaseFetchAll
from controllers.usuarios_controller import UsuarioController
from controllers.especialidades_controller import EspecialidadeController
from controllers.medicos_controller import MedicosController
from engine.config_db import DatabaseConfig

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'

config = DatabaseConfig()
DATABASE_URL = config.get_uri()

db_fetch_all = DatabaseFetchAll(DATABASE_URL)
usuario_controller = UsuarioController(db_fetch_all)
especialidade_controller = EspecialidadeController(db_fetch_all)
medicos_controller = MedicosController(db_fetch_all)

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
                return redirect(url_for('especialidades'))  # Redirecionar para evitar reenvio do formulário
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
        especialidade = next((e for e in especialidades if e.id == id), None)
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


# Rotas de Médicos
@app.route('/medicos', methods=['GET', 'POST'])
def create_medico():
    if 'user_id' in login_session:
        if request.method == 'POST':
            nome = request.form['nome']
            crm = request.form['crm']
            especialidades_ids = request.form.getlist('especialidades')
            medicos_controller.create_medico(nome, crm, especialidades_ids)
            return redirect(url_for('list_medicos'))

        especialidades = especialidade_controller.read_especialidades()
        return render_template('medico_form.html', especialidades=especialidades)
    return redirect(url_for('login'))


@app.route('/medicos/list')
def list_medicos():
    if 'user_id' in login_session:
        medicos = medicos_controller.read_medicos()
        print(medicos)  # Para depuração
        return render_template('medico.html', medicos=medicos)
    return redirect(url_for('login'))


@app.route('/medicos/edit/<int:id>', methods=['GET', 'POST'])
def update_medico(id):
    if request.method == 'POST':
        nome = request.form['nome']
        crm = request.form['crm']
        especialidades_ids = request.form.getlist('especialidades')

        medicos_controller.update_medico(id, nome, crm)
        medicos_controller.remove_especialidades_medico(id)

        for especialidade_id in especialidades_ids:
            medicos_controller.add_especialidade_medico(id, especialidade_id)

        return redirect(url_for('list_medicos'))

    medico = medicos_controller.read_medico_by_id(id)

    if isinstance(medico, dict) and 'especialidades' in medico:
        especialidades = especialidade_controller.read_especialidades()

        special_medico = [especialidade_controller.get_id_by_name(e) for e in medico['especialidades']]

        return render_template('editar_medico.html', medico=medico, especialidades=especialidades,
                               special_medico=special_medico)

    return redirect(url_for('list_medicos'))


@app.route('/medicos/delete/<int:id>')
def delete_medico(id):
    if 'user_id' in login_session:
        medicos_controller.delete_medico(id)
        return redirect(url_for('list_medicos'))
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
