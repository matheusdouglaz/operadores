import pandas as pd
from app import app, db, Operadora, Demonstracao
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def importar_operadoras():
    # Lê o arquivo CSV
    df = pd.read_csv('operadoras.csv', encoding='utf-8')
    
    # Itera sobre as linhas do DataFrame
    for _, row in df.iterrows():
        operadora = Operadora(
            cnpj=str(row['cnpj']).zfill(14),
            razao_social=row['razao_social'],
            nome_fantasia=row['nome_fantasia'],
            modalidade=row['modalidade']
        )
        db.session.add(operadora)
    
    # Commit das alterações
    db.session.commit()
    print("Operadoras importadas com sucesso!")

if __name__ == '__main__':
    with app.app_context():
        importar_operadoras() 