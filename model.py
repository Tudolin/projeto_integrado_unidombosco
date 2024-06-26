from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RegistroVacina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente = db.Column(db.String(100), nullable=False)
    data_vacinacao = db.Column(db.Date, nullable=False)
    vacina = db.Column(db.String(100), nullable=False)
    unidade = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<RegistroVacina {self.paciente}>'
