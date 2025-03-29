from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
from sqlalchemy import text
import random

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+pg8000://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos
class Operadora(db.Model):
    __tablename__ = 'operadoras'
    
    cnpj = db.Column(db.String(14), primary_key=True)
    razao_social = db.Column(db.String(255), nullable=False)
    nome_fantasia = db.Column(db.String(255))
    modalidade = db.Column(db.String(50))
    demonstracoes = db.relationship('Demonstracao', backref='operadora', lazy=True)

class Demonstracao(db.Model):
    __tablename__ = 'demonstracoes'
    
    id = db.Column(db.Integer, primary_key=True)
    operadora_cnpj = db.Column(db.String(14), db.ForeignKey('operadoras.cnpj'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    valor = db.Column(db.Float, nullable=False)

# Rotas
@app.route('/operadoras', methods=['GET'])
def listar_operadoras():
    operadoras = Operadora.query.all()
    return jsonify([{
        'cnpj': o.cnpj,
        'razao_social': o.razao_social,
        'nome_fantasia': o.nome_fantasia,
        'modalidade': o.modalidade
    } for o in operadoras])

@app.route('/operadoras/aleatoria', methods=['GET'])
def obter_operadora_aleatoria():
    operadoras = Operadora.query.all()
    if not operadoras:
        return jsonify({'error': 'Nenhuma operadora encontrada'}), 404
    
    operadora = random.choice(operadoras)
    return jsonify({
        'cnpj': operadora.cnpj,
        'razao_social': operadora.razao_social,
        'nome_fantasia': operadora.nome_fantasia,
        'modalidade': operadora.modalidade
    })

@app.route('/operadoras/<cnpj>', methods=['GET'])
def obter_operadora(cnpj):
    operadora = Operadora.query.get_or_404(cnpj)
    return jsonify({
        'cnpj': operadora.cnpj,
        'razao_social': operadora.razao_social,
        'nome_fantasia': operadora.nome_fantasia,
        'modalidade': operadora.modalidade
    })

@app.route('/operadoras/busca', methods=['GET'])
def buscar_operadoras():
    termo = request.args.get('q', '')
    if not termo:
        return jsonify([])
    
    operadoras = Operadora.query.filter(
        (Operadora.razao_social.ilike(f'%{termo}%')) |
        (Operadora.nome_fantasia.ilike(f'%{termo}%')) |
        (Operadora.modalidade.ilike(f'%{termo}%'))
    ).all()
    
    return jsonify([{
        'cnpj': o.cnpj,
        'razao_social': o.razao_social,
        'nome_fantasia': o.nome_fantasia,
        'modalidade': o.modalidade
    } for o in operadoras])

@app.route('/demonstracoes', methods=['GET'])
def listar_demonstracoes():
    demonstracoes = Demonstracao.query.all()
    return jsonify([{
        'id': d.id,
        'operadora_cnpj': d.operadora_cnpj,
        'data': d.data.strftime('%Y-%m-%d'),
        'valor': d.valor
    } for d in demonstracoes])

@app.route('/demonstracoes/<int:id>', methods=['GET'])
def obter_demonstracao(id):
    demonstracao = Demonstracao.query.get_or_404(id)
    return jsonify({
        'id': demonstracao.id,
        'operadora_cnpj': demonstracao.operadora_cnpj,
        'data': demonstracao.data.strftime('%Y-%m-%d'),
        'valor': demonstracao.valor
    })

@app.route('/analise/ultimo-trimestre', methods=['GET'])
def top_operadoras_ultimo_trimestre():
    query = text("""
        WITH ultimo_trimestre AS (
            SELECT MAX(data) as data_max
            FROM demonstracoes
        )
        SELECT 
            o.razao_social,
            o.nome_fantasia,
            SUM(d.valor) as total_despesas
        FROM demonstracoes d
        JOIN operadoras o ON d.operadora_cnpj = o.cnpj
        WHERE d.data >= (SELECT data_max - INTERVAL '3 months' FROM ultimo_trimestre)
        GROUP BY o.razao_social, o.nome_fantasia
        ORDER BY total_despesas DESC
        LIMIT 10
    """)
    
    result = db.session.execute(query)
    return jsonify([{
        'razao_social': row.razao_social,
        'nome_fantasia': row.nome_fantasia,
        'total_despesas': float(row.total_despesas)
    } for row in result])

@app.route('/analise/ultimo-ano', methods=['GET'])
def top_operadoras_ultimo_ano():
    query = text("""
        WITH ultimo_ano AS (
            SELECT MAX(data) as data_max
            FROM demonstracoes
        )
        SELECT 
            o.razao_social,
            o.nome_fantasia,
            SUM(d.valor) as total_despesas
        FROM demonstracoes d
        JOIN operadoras o ON d.operadora_cnpj = o.cnpj
        WHERE d.data >= (SELECT data_max - INTERVAL '1 year' FROM ultimo_ano)
        GROUP BY o.razao_social, o.nome_fantasia
        ORDER BY total_despesas DESC
        LIMIT 10
    """)
    
    result = db.session.execute(query)
    return jsonify([{
        'razao_social': row.razao_social,
        'nome_fantasia': row.nome_fantasia,
        'total_despesas': float(row.total_despesas)
    } for row in result])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 