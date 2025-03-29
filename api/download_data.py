import requests
import os

def download_operadoras():
    url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/operadoras_ativas.csv"
    
    print("Baixando arquivo de operadoras...")
    response = requests.get(url)
    
    if response.status_code == 200:
        with open('operadoras.csv', 'wb') as f:
            f.write(response.content)
        print("Arquivo baixado com sucesso!")
    else:
        print(f"Erro ao baixar arquivo: {response.status_code}")

if __name__ == '__main__':
    download_operadoras() 