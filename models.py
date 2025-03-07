from db import db
from flask_login import UserMixin #login

class Usuario(UserMixin, db.Model): #herda de usermixin que identifica como uma classe de usuario de login
    __tablename__ = 'usuarios'  #nome da tabela

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(), nullable=False)

class Tarefa(db.Model):
    __tablename__ = 'tarefas'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('tarefas', lazy=True))
    

