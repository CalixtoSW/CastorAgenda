# CastorAgenda/CastorAgenda.py
from flask import Flask, render_template, request, redirect, url_for, jsonify, session as login_session

from engine.database_fetchall import DatabaseFetchAll
from engine.config_db import DatabaseConfig

from controllers.usuarios_controller import UsuarioController
from controllers.especialidades_controller import EspecialidadeController
from controllers.medico_controller import MedicoController
from controllers.sala_controller import SalaController
from controllers.paciente_controller import PacienteController
from controllers.agendamento_controller import AgendamentoController




app = Flask(__name__)
app.secret_key = '1245fvcx323423423dfdscxvxvcxgerr43'

config = DatabaseConfig()
DATABASE_URL = config.get_uri()
db_fetch_all = DatabaseFetchAll(DATABASE_URL)

usuario_controller = UsuarioController(db_fetch_all)
especialidade_controller = EspecialidadeController(db_fetch_all)
medico_controller = MedicoController(db_fetch_all)
sala_controller = SalaController(db_fetch_all)
paciente_controller = PacienteController(db_fetch_all)
agendamento_controller = AgendamentoController(db_fetch_all)

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

@app.route('/especialidades', methods=['GET', 'POST'])
def especialidades():
    if 'user_id' in login_session:
        if request.method == 'POST':
            nome = request.form['nome']
            if nome:
                especialidade_controller.create_especialidade(nome)
                return redirect(url_for('especialidades'))  # Evitar reenvio do formulário
        especialidades = especialidade_controller.listar_especialidades()
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
        especialidades = especialidade_controller.listar_especialidades()
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

@app.route('/medico')
def listar_medicos():
    # Obtém a lista de médicos do MedicoController
    medicos = medico_controller.listar_medicos()
    return render_template('medico.html', medicos=medicos)

@app.route('/medicos/novo', methods=['POST'])
def novo_medico():
    if 'user_id' in login_session:
        nome = request.form.get('nome')  # Verifica se 'nome' está sendo enviado
        crm = request.form.get('crm')    # Verifica se 'crm' está sendo enviado
        if nome and crm:
            medico_controller.inserir_medico(nome, crm)
            return redirect(url_for('listar_medicos'))
        else:
            return 'Erro: Nome e CRM são obrigatórios.', 400
    return redirect(url_for('login'))


@app.route('/medicos/editar/<int:id_medico>', methods=['GET', 'POST'])
def editar_medico(id_medico):
    if request.method == 'POST':
        nome = request.form['nome']
        crm = request.form['crm']
        especialidades_selecionadas = request.form.getlist('especialidades')
        medico_controller.editar_medico(id_medico, nome, crm, especialidades_selecionadas)
        return redirect(url_for('listar_medicos'))

    medico = medico_controller.buscar_medico_por_id(id_medico)
    if medico is None:
        return "Médico não encontrado", 404

    todas_especialidades = especialidade_controller.listar_especialidades()
    especialidades_do_medico = [e['id'] for e in medico.get('especialidades', [])]
    return render_template('editar_medico.html', medico=medico, especialidades=todas_especialidades, especialidades_do_medico=especialidades_do_medico)

@app.route('/medicos/delete/<int:id>', methods=['POST'])
def delete_medico(id):
    if 'user_id' in login_session:
        medico_controller.delete_medico(id)
        return redirect(url_for('listar_medicos'))
    return redirect(url_for('login'))

@app.route('/medicos/<int:id_medico>/especialidade/nova', methods=['GET', 'POST'])
def adicionar_especialidade(id_medico):
    if request.method == 'POST':
        nome_especialidade = request.form['nome']
        especialidade_controller.create_especialidade(nome_especialidade)
        return redirect(url_for('editar_medico', id_medico=id_medico))
    return render_template('adicionar_especialidade.html', medico={'id': id_medico})

@app.route('/sala', methods=['GET'])
def listar_salas():
    salas = sala_controller.listar_salas()
    return render_template('sala.html', salas=salas)

@app.route('/sala/nova', methods=['POST'])
def nova_sala():
    nome = request.form.get('nome')
    numero = request.form.get('numero-sala')
    capacidade = request.form.get('capacidade')
    sala_controller.cadastrar_sala(nome, numero, capacidade)
    return redirect(url_for('listar_salas'))

@app.route('/sala/editar/<int:id>', methods=['GET', 'POST'])
def editar_sala(id):
    if request.method == 'POST':
        nome = request.form.get('nome')
        numero = request.form.get('numero')
        capacidade = request.form.get('capacidade')
        sala_controller.editar_sala(id, nome, numero, capacidade)
        return redirect(url_for('listar_salas'))

    sala = sala_controller.buscar_sala_por_id(id)
    return render_template('editar_sala.html', sala=sala)

@app.route('/sala/excluir/<int:id>', methods=['POST'])
def excluir_sala(id):
    sala_controller.excluir_sala(id)
    return redirect(url_for('listar_salas'))

@app.route('/pacientes', methods=['GET'])
def listar_pacientes():
    pacientes = paciente_controller.listar_pacientes()
    return render_template('paciente.html', pacientes=pacientes)

@app.route('/paciente/novo', methods=['POST'])
def cadastrar_paciente():
    nome = request.form.get('nome')
    dt_nascimento = request.form.get('dt_nascimento')
    sexo = request.form.get('sexo')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    endereco = request.form.get('endereco')
    paciente_controller.cadastrar_paciente(nome, dt_nascimento, sexo, telefone, email, endereco)
    return redirect(url_for('listar_pacientes'))

@app.route('/paciente/editar/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    if request.method == 'POST':
        nome = request.form.get('nome')
        dt_nascimento = request.form.get('dt_nascimento')
        sexo = request.form.get('sexo')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        endereco = request.form.get('endereco')
        paciente_controller.editar_paciente(id, nome, dt_nascimento, sexo, telefone, email, endereco)
        return redirect(url_for('listar_pacientes'))

    paciente = paciente_controller.buscar_paciente_por_id(id)
    return render_template('editar_paciente.html', paciente=paciente)


@app.route('/paciente/excluir/<int:id>', methods=['POST'])
def excluir_paciente(id):
    paciente_controller.excluir_paciente(id)
    return redirect(url_for('listar_pacientes'))


@app.route('/agenda', methods=['GET'])
def agenda():
    agendamentos = agendamento_controller.listar_agendamentos()
    return render_template('agenda.html', agendamentos=agendamentos)


@app.route('/agendamento/cadastrar', methods=['GET', 'POST'])
def cadastrar_agendamento():
    if request.method == 'POST':
        # Lógica para POST (criar agendamento)
        data = request.form['data']
        hora = request.form['hora']
        sala_id = request.form['sala_id']
        medico_id = request.form['medico_id']
        paciente_id = request.form['paciente_id']

        if not data or not hora or not sala_id or not medico_id:
            return 'Todos os campos são obrigatórios', 400

        agendamento_controller.cadastrar_agendamento(data, hora, sala_id, medico_id, paciente_id)
        return redirect(url_for('agenda'))

    # GET request - return necessary data in JSON format for AJAX
    medicos = agendamento_controller.listar_medicos_combo()
    salas = agendamento_controller.listar_salas()
    pacientes = agendamento_controller.listar_pacientes()

    # Debug prints to verificar os dados
    print('Medicos:', medicos)
    print('Salas:', salas)
    print('Pacientes:', pacientes)

    # Retorna os dados como um JSON
    return jsonify(medicos=medicos, salas=salas, pacientes=pacientes)

@app.route('/agendamento/editar/<int:id>', methods=['GET', 'POST'])
def editar_agendamento(id):
    if request.method == 'POST':
        data = request.form['data']
        hora = request.form['hora']
        sala_id = request.form['sala_id']
        medico_id = request.form['medico_id']
        paciente_id = request.form['paciente_id']
        status_agendamento = request.form['status_agendamento']

        if not data or not hora or not sala_id or not medico_id or not paciente_id or not status_agendamento:
            return 'Todos os campos são obrigatórios', 400

        agendamento_controller.editar_agendamento(id, data, hora, sala_id, medico_id, paciente_id, status_agendamento)
        return redirect(url_for('agenda'))

    agendamento = agendamento_controller.buscar_agendamento_por_id(id)
    medicos = agendamento_controller.listar_medicos()
    salas = agendamento_controller.listar_salas()
    pacientes = agendamento_controller.listar_pacientes()

    return render_template('editar_agendamento.html', agendamento=agendamento, medicos=medicos, salas=salas,
                           pacientes=pacientes)


@app.route('/agendamento/excluir/<int:id>', methods=['POST'])
def excluir_agendamento(id):
    agendamento_controller.excluir_agendamento(id)
    return redirect(url_for('agenda'))


@app.route('/agendamento/buscar/<data>', methods=['GET'])
def buscar_agendamentos_por_dia(data):
    agendamentos = agendamento_controller.buscar_agendamentos_por_dia(data)
    return jsonify(agendamentos)


@app.route('/agendamento', methods=['GET'])
def novo_agendamento():
    medicos = agendamento_controller.listar_medicos()
    salas = agendamento_controller.listar_salas()
    pacientes = agendamento_controller.listar_pacientes()
    return render_template('agendamento.html', medicos=medicos, salas=salas, pacientes=pacientes)

@app.route('/agendamentos/<data>', methods=['GET'])
def listar_agendamentos(data):
    agendamentos = agendamento_controller.buscar_agendamentos_por_dia(data)
    return jsonify(agendamentos)


@app.route('/agenda/contagem', methods=['GET'])
def contagem_agendamentos():
    contagens = agendamento_controller.contar_agendamentos_por_dia()
    return jsonify(contagens)


if __name__ == '__main__':
    app.run(debug=True, port=8090)

