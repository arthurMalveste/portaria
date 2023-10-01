
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import request
import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Arthur_Malveste:Amm.22.01.78@localhost/portaria'
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
    data_cadastro = db.Column(db.DateTime, default=datetime.datetime.utcnow)  # Adicionando a coluna de hora de entrada

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
        email = request.form['email']
        cpf = request.form['cpf']
        celular = request.form['celular']
        telefone = request.form['telefone']
        whatsapp = request.form['whatsapp']
        endereco =request.form['endereco']
        observacao = request.form['observacao']

        # A data_cadastro é definida automaticamente como datetime.datetime.utcnow()

        pessoa = Pessoa(
            nome_completo=nome_completo,
            email=email,
            cpf=cpf,
            celular=celular,
            telefone=telefone,
            whatsapp=whatsapp,
            observacao=observacao,
            endereco=endereco
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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
