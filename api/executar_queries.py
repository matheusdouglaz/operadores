import pandas as pd
from app import app, db
from sqlalchemy import text
import os

def executar_queries():
    with app.app_context():
        # Query do último trimestre
        query_trimestre = text("""
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
        
        # Query do último ano
        query_ano = text("""
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
        
        # Executa as queries e salva os resultados
        resultados_trimestre = pd.read_sql(query_trimestre, db.engine)
        resultados_ano = pd.read_sql(query_ano, db.engine)
        
        # Salva os resultados em arquivos CSV
        resultados_trimestre.to_csv('top_operadoras_trimestre.csv', index=False)
        resultados_ano.to_csv('top_operadoras_ano.csv', index=False)
        
        print("Queries executadas com sucesso!")
        print("\nTop 10 operadoras no último trimestre:")
        print(resultados_trimestre)
        print("\nTop 10 operadoras no último ano:")
        print(resultados_ano)

if __name__ == '__main__':
    executar_queries() 