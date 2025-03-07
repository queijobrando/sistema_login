from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db import db
from models import Usuario, Tarefa
from flask import Blueprint

tarefas_bp = Blueprint('tarefas', __name__, template_folder='templates')# inicia o blueprint e informa onde estõ os templates

#LISTA TAREFAS
@tarefas_bp.route('/', methods=['GET'])
@login_required
def listar_tarefas():
    tarefas_usuario = Tarefa.query.filter_by(id_usuario=current_user.id).all() #filtra as tarefas por id do usuario atual
    return render_template('tarefas.html', tarefas=tarefas_usuario)

#ADICIONAR TAREFA
@tarefas_bp.route('/adicionartarefa', methods=['POST', 'GET'])
@login_required
def adicionartarefas():
    if request.method == 'GET':
        return render_template('adicionartarefa.html')
    elif request.method == 'POST':
        descricao = request.form['descricaoForm']

        nova_tarefa = Tarefa(descricao=descricao, id_usuario=current_user.id)
        db.session.add(nova_tarefa) #adiciona ao banco de dados
        db.session.commit()

        return redirect(url_for('tarefas.listar_tarefas'))


#EXCLUIR TAREFA 
@tarefas_bp.route('/excluir_tarefa/<int:id_tarefa>', methods=['POST'])
@login_required
def excluir_tarefa(id_tarefa):
    tarefa = Tarefa.query.filter_by(id=id_tarefa, id_usuario=current_user.id).first() #pega o id_tarefa que será mostrado na rota /excluir_tarefa/id_tarefa, junto com o id atual

    if not tarefa:
        flash('Tarefa não existente ou você não possui permissão')
        return redirect(url_for('listar_tarefas'))

    db.session.delete(tarefa)
    db.session.commit()

    return redirect(url_for('tarefas.listar_tarefas'))
