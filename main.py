from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db import db
from models import Usuario, Tarefa

app = Flask(__name__)
app.secret_key = 'lancode'
lm = LoginManager(app)
lm.login_view = 'login' #redireciona para a pagina login se o login não for feito (não deixa entrar na home)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

###LOGIN ID
@lm.user_loader
def user_loader(id):
    usuario = db.session.query(Usuario).filter_by(id=id).first() #puxa do db da tabela Usuario onde o id seja igual
    return usuario

#HOME
@app.route('/')
def home():
    return render_template('index.html')

#REGISTRO USUARIO
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method =='GET': #se o metodo for get
        return render_template('registro.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        senha = request.form['senhaForm']

        novo_usuario = Usuario(nome=nome, senha=senha) #cria um novo usuario  a parir dos inputs
        db.session.add(novo_usuario) #adiciona ao banco de dados
        db.session.commit()

        login_user(novo_usuario) #logando o novo usuario criado

        return redirect(url_for('home'))#funcao home

#LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        senha = request.form['senhaForm']

        user = db.session.query(Usuario).filter_by(nome=nome, senha=senha).first()
        if not user:
            flash('Nome ou senha incorretos', 'error')
            return redirect(url_for('login'))

        
        login_user(user) #logando o usuario
        return redirect(url_for('home'))
    
#LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

#LISTA TAREFAS
@app.route('/tarefas', methods=['GET'])
@login_required
def tarefas():
    tarefas_usuario = Tarefa.query.filter_by(id_usuario=current_user.id).all()
    return render_template('tarefas.html', tarefas=tarefas_usuario)
    
@app.route('/adicionartarefa', methods=['POST', 'GET'])
def adicionartarefas():
    if request.method == 'GET':
        return render_template('adicionartarefa.html')
    elif request.method == 'POST':
        descricao = request.form['descricaoForm']

        nova_tarefa = Tarefa(descricao=descricao, id_usuario=current_user.id)
        db.session.add(nova_tarefa) #adiciona ao banco de dados
        db.session.commit()

        return redirect(url_for('tarefas'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)