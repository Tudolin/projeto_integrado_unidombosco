import sqlite3
from datetime import datetime

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacinas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class RegistroVacina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente = db.Column(db.String(100), nullable=False)
    data_vacinacao = db.Column(db.Date, nullable=False)
    vacina = db.Column(db.String(100), nullable=False)
    unidade = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<RegistroVacina {self.paciente}>'
def init_db():
    conn = sqlite3.connect('vacinas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Vacinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            fabricante TEXT,
            lote TEXT,
            validade DATE,
            requisitos_armazenamento TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UnidadesSaude (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT,
            telefone TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_nascimento DATE,
            cpf TEXT,
            endereco TEXT,
            telefone TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            vacina_id INTEGER,
            unidade_saude_id INTEGER,
            data DATE,
            hora TIME,
            FOREIGN KEY(paciente_id) REFERENCES Pacientes(id),
            FOREIGN KEY(vacina_id) REFERENCES Vacinas(id),
            FOREIGN KEY(unidade_saude_id) REFERENCES UnidadesSaude(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro_vacina', methods=['GET', 'POST'])
def cadastro_vacina():
    if request.method == 'POST':
        nome = request.form['nome']
        fabricante = request.form['fabricante']
        lote = request.form['lote']
        validade = request.form['validade']
        requisitos = request.form['requisitos']
        conn = sqlite3.connect('vacinas.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Vacinas (nome, fabricante, lote, validade, requisitos_armazenamento)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, fabricante, lote, validade, requisitos))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('cadastro_vacina.html')

@app.route('/cadastro_paciente', methods=['GET', 'POST'])
def cadastro_paciente():
    if request.method == 'POST':
        paciente = request.form['paciente']
        data_vacinacao = datetime.strptime(request.form['data_vacinacao'], '%Y-%m-%d')
        vacina = request.form['vacina']
        unidade = request.form['unidade']
        
        novo_registro = RegistroVacina(paciente=paciente, data_vacinacao=data_vacinacao, vacina=vacina, unidade=unidade)
        db.session.add(novo_registro)
        db.session.commit()
        
        return redirect(url_for('relatorios'))
    return render_template('cadastro_paciente.html')



@app.route('/cadastro_unidade', methods=['GET', 'POST'])
def cadastro_unidade():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        conn = sqlite3.connect('vacinas.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO UnidadesSaude (nome, endereco, telefone)
            VALUES (?, ?, ?)
        ''', (nome, endereco, telefone))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('cadastro_unidade.html')

@app.route('/agendamento', methods=['GET', 'POST'])
def agendamento():
    conn = sqlite3.connect('vacinas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome FROM Pacientes')
    pacientes = cursor.fetchall()
    cursor.execute('SELECT id, nome FROM Vacinas')
    vacinas = cursor.fetchall()
    cursor.execute('SELECT id, nome FROM UnidadesSaude')
    unidades = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        vacina_id = request.form['vacina_id']
        unidade_saude_id = request.form['unidade_saude_id']
        data = request.form['data']
        hora = request.form['hora']
        conn = sqlite3.connect('vacinas.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Agendamentos (paciente_id, vacina_id, unidade_saude_id, data, hora)
            VALUES (?, ?, ?, ?, ?)
        ''', (paciente_id, vacina_id, unidade_saude_id, data, hora))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('agendamento.html', pacientes=pacientes, vacinas=vacinas, unidades=unidades)

@app.route('/registros')
def registros():
    conn = sqlite3.connect('vacinas.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.id, p.nome, v.nome, u.nome, a.data, a.hora
        FROM Agendamentos a
        JOIN Pacientes p ON a.paciente_id = p.id
        JOIN Vacinas v ON a.vacina_id = v.id
        JOIN UnidadesSaude u ON a.unidade_saude_id = u.id
    ''')
    agendamentos = cursor.fetchall()
    conn.close()
    return render_template('registros.html', agendamentos=agendamentos)

@app.route('/relatorios')
def relatorios():
    return render_template('relatorios.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
