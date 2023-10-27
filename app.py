
from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import request
import datetime
from datetime import datetime, timezone, timedelta




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Arthur_Malveste:Amm.22.01.78@localhost/portaria'
app.config['TIMEZONE'] = 'America/Sao_Paulo'  # Substitua pelo seu fuso horário
db = SQLAlchemy(app)

# parte do banco de dados
class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    celular = db.Column(db.String(10), unique=True, nullable=False)
    telefone = db.Column(db.String(11), unique=True, nullable=False)
    whatsapp = db.Column(db.String(10), unique=True, nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    observacao = db.Column(db.Text)
    data_cadastro = db.Column(db.DateTime, default=datetime.now(timezone(timedelta(hours=-3))))  # Adicionando a coluna de hora de entrada
    cep = db.Column(db.String(8), unique=True, nullable=False)

    def __repr__(self):
        return f'<Pessoa {self.nome_completo}>'

@app.route('/')
def index():
    q = request.args.get('q')
    
    if q:
        pessoas = Pessoa.query.filter((Pessoa.nome_completo.like(f"%{q}%")) | (Pessoa.cpf.like(f"%{q}%"))).all()
    else:
        pessoas = Pessoa.query.all()

    return render_template('index.html', pessoas=pessoas)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

    if request.method == 'POST':
        nome_completo = request.form['nome_completo']

        # Verificar se o nome já existe no banco de dados
        pessoa_existente = Pessoa.query.filter_by(nome_completo=nome_completo).first()

        if pessoa_existente:
            # Se o nome já existe, crie uma nova entrada com a data atual
            pessoa = Pessoa(
                nome_completo=nome_completo,
                email=request.form['email'],
                cpf=request.form['cpf'],
                celular=request.form['celular'],
                telefone=request.form['telefone'],
                whatsapp=request.form['whatsapp'],
                endereco=request.form['endereco'],
                observacao=request.form['observacao'],
                cep=request.form['cep'],
                data_cadastro=datetime.now(timezone(timedelta(hours=-3)))
            )
        else:
            # Se o nome não existe, obtenha os valores dos outros campos do formulário
            pessoa = Pessoa(
                nome_completo=nome_completo,
                email=request.form['email'],
                cpf=request.form['cpf'],
                celular=request.form['celular'],
                telefone=request.form['telefone'],
                whatsapp=request.form['whatsapp'],
                endereco=request.form['endereco'],
                observacao=request.form['observacao'],
                cep=request.form['cep'],
                data_cadastro=datetime.now(timezone(timedelta(hours=-3)))
            )

        db.session.add(pessoa)
        db.session.commit()
        return redirect('/')

    return render_template('index.html')


@app.route('/tabela', methods=['GET'])
def tabela():
    pessoas = Pessoa.query.all()
    delete = False

    q = request.args.get('q')  # Obtém o valor do campo de pesquisa
    if q:
        # Filtra os resultados com base no nome ou CPF
        pessoas = Pessoa.query.filter(
            (Pessoa.nome_completo.like(f"%{q}%")) |
            (Pessoa.cpf.like(f"%{q}%")) |
            (Pessoa.celular.like(f"%{q}%"))
        ).all()
        delete = True
    else:
        # Se nenhum valor de pesquisa for fornecido, obtenha todas as pessoas
        pessoas = Pessoa.query.all()
    


    
    return render_template('tabela.html', pessoas=pessoas, delete=delete)

@app.route('/excluir/<int:id>', methods=['DELETE'])
def excluir_pessoa(id):
    pessoa = Pessoa.query.get(id)  # Consultar a pessoa pelo ID
    if pessoa:
        db.session.delete(pessoa)  # Excluir a pessoa do banco de dados
        db.session.commit()  # Realizar o commit para efetivar a exclusão
        return "Linha excluída com sucesso", 200
    else:
        return "ID não encontrado", 404


@app.route('/verificar_nome', methods=['GET'])
def verificar_nome():
    nome = request.args.get('nome')  # Obtenha o nome da consulta de URL
    pessoa = Pessoa.query.filter_by(nome_completo=nome).first()

    if pessoa:
        # Se o nome já existir, retorne seus detalhes em JSON
        return {
            'nome_completo': pessoa.nome_completo,
            'email': pessoa.email,
            'cpf': pessoa.cpf,
            'celular': pessoa.celular,
            'telefone': pessoa.telefone,
            'whatsapp': pessoa.whatsapp,
            'endereco': pessoa.endereco,
            'observacao': pessoa.observacao,
            'cep': pessoa.cep,
        }
    else:
        # Se o nome não existir, retorne um objeto JSON vazio
        return {}




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    gunicorn app:app(debug=True)
