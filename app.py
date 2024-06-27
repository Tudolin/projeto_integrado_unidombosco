from datetime import datetime

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from chatbot import chatbot

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacinas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Vacina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    fabricante = db.Column(db.String(100))
    lote = db.Column(db.String(100))
    validade = db.Column(db.Date)
    requisitos_armazenamento = db.Column(db.String(100))

class UnidadeSaude(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100))
    telefone = db.Column(db.String(100))

class RegistroPaciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    cpf = db.Column(db.String(100), nullable=False)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('registro_paciente.id'), nullable=False)
    vacina_id = db.Column(db.Integer, db.ForeignKey('vacina.id'), nullable=False)
    unidade_saude_id = db.Column(db.Integer, db.ForeignKey('unidade_saude.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    
    paciente = db.relationship('RegistroPaciente', backref=db.backref('agendamentos', lazy=True))
    vacina = db.relationship('Vacina', backref=db.backref('agendamentos', lazy=True))
    unidade_saude = db.relationship('UnidadeSaude', backref=db.backref('agendamentos', lazy=True))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = chatbot.get_response(user_message)
    return jsonify({"response": response})

@app.route('/cadastro_vacina', methods=['GET', 'POST'])
def cadastro_vacina():
    if request.method == 'POST':
        nome = request.form['nome']
        fabricante = request.form['fabricante']
        lote = request.form['lote']
        validade = request.form['validade']
        requisitos = request.form['requisitos']
        
        nova_vacina = Vacina(nome=nome, fabricante=fabricante, lote=lote, validade=datetime.strptime(validade, '%Y-%m-%d'), requisitos_armazenamento=requisitos)
        db.session.add(nova_vacina)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('cadastro_vacina.html')

@app.route('/cadastro_paciente', methods=['GET', 'POST'])
def cadastro_paciente():
    if request.method == 'POST':
        paciente = request.form['paciente']
        data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d')
        cpf = request.form['cpf']
        
        novo_registro = RegistroPaciente(paciente=paciente, data_nascimento=data_nascimento, cpf=cpf)
        db.session.add(novo_registro)
        db.session.commit()
        
        return redirect(url_for('cadastro_paciente'))
    return render_template('cadastro_paciente.html')

@app.route('/cadastro_unidade', methods=['GET', 'POST'])
def cadastro_unidade():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        
        nova_unidade = UnidadeSaude(nome=nome, endereco=endereco, telefone=telefone)
        db.session.add(nova_unidade)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('cadastro_unidade.html')

@app.route('/agendamento', methods=['GET', 'POST'])
def agendamento():
    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        vacina_id = request.form['vacina_id']
        unidade_saude_id = request.form['unidade_saude_id']
        data = request.form['data']
        hora = request.form['hora']
        
        novo_agendamento = Agendamento(
            paciente_id=paciente_id,
            vacina_id=vacina_id,
            unidade_saude_id=unidade_saude_id,
            data=datetime.strptime(data, '%Y-%m-%d'),
            hora=datetime.strptime(hora, '%H:%M').time()
        )
        db.session.add(novo_agendamento)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    pacientes = RegistroPaciente.query.all()
    vacinas = Vacina.query.all()
    unidades = UnidadeSaude.query.all()
    
    return render_template('agendamento.html', pacientes=pacientes, vacinas=vacinas, unidades=unidades)

@app.route('/registros')
def registros():
    agendamentos = db.session.query(
        Agendamento.id,
        RegistroPaciente.paciente,
        Vacina.nome,
        UnidadeSaude.nome,
        Agendamento.data,
        Agendamento.hora
    ).join(RegistroPaciente, Agendamento.paciente_id == RegistroPaciente.id)\
     .join(Vacina, Agendamento.vacina_id == Vacina.id)\
     .join(UnidadeSaude, Agendamento.unidade_saude_id == UnidadeSaude.id)\
     .all()

    return render_template('registros.html', agendamentos=agendamentos)

@app.route('/relatorios')
def relatorios():
    registros = db.session.query(Agendamento, RegistroPaciente, Vacina, UnidadeSaude).join(RegistroPaciente).join(Vacina).join(UnidadeSaude).all()

    unidades = [unidade.nome for unidade in UnidadeSaude.query.all()]
    vacinas_por_unidade = [db.session.query(Agendamento).filter(Agendamento.unidade_saude_id == unidade.id).count() for unidade in UnidadeSaude.query.all()]

    idade_intervals = [(0, 18), (19, 35), (36, 50), (51, 120)]
    vacinas_por_idade = [0, 0, 0, 0]

    for agendamento, paciente, vacina, unidade in registros:
        idade = datetime.now().year - paciente.data_nascimento.year - ((datetime.now().month, datetime.now().day) < (paciente.data_nascimento.month, paciente.data_nascimento.day))
        for i, interval in enumerate(idade_intervals):
            if interval[0] <= idade <= interval[1]:
                vacinas_por_idade[i] += 1
                break

    return render_template('relatorios.html', registros=registros, unidades=unidades, vacinas_por_unidade=vacinas_por_unidade, vacinas_por_idade=vacinas_por_idade)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)
