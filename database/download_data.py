import os
import requests
import pandas as pd
from datetime import datetime
import zipfile

def download_data():
    # Criar diretório de dados se não existir
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Diretório {data_dir} criado")
    
    # URLs dos dados
    urls = {
        'operadoras': [
            "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
        ],
        'demonstracoes': [
            "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/1T2024.zip",
            "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/2T2024.zip",
            "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/3T2024.zip",
            "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/4T2024.zip"
        ]
    }
    
    def download_file(url, filename):
        try:
            print(f"\nTentando baixar: {filename}")
            response = requests.get(url)
            response.raise_for_status()
            
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"Download concluído: {filename}")
            
            # Se for um arquivo ZIP, extrair o conteúdo
            if filename.endswith('.zip'):
                print(f"Extraindo arquivo ZIP: {filename}")
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    zip_ref.extractall(data_dir)
                print(f"Extração concluída: {filename}")
            
            return True
        except Exception as e:
            print(f"Erro ao baixar {filename}: {str(e)}")
            return False
    
    # Download dos dados das operadoras
    print("Baixando dados das operadoras...")
    operadoras_downloaded = False
    for url in urls['operadoras']:
        if download_file(url, "operadoras.csv"):
            operadoras_downloaded = True
            break
    
    # Download das demonstrações contábeis
    print("\nBaixando demonstrações contábeis...")
    demonstracoes_downloaded = False
    for url in urls['demonstracoes']:
        if download_file(url, url.split('/')[-1]):
            demonstracoes_downloaded = True
            break
    
    # Verificar se conseguiu baixar os arquivos
    if not (operadoras_downloaded and demonstracoes_downloaded):
        print("\nNão foi possível baixar os arquivos automaticamente.")
        print("Por favor, acesse manualmente o site da ANS para baixar os dados:")
        print("https://dadosabertos.ans.gov.br/FTP/PDA/")
        print("\nVocê precisa baixar:")
        print("1. O arquivo Relatorio_cadop.csv")
        print("2. Um arquivo de demonstrações contábeis (1T2024.zip, 2T2024.zip, 3T2024.zip ou 4T2024.zip)")
        print("\nE colocá-los na pasta:", os.path.abspath(data_dir))
    else:
        print("\nDownload concluído com sucesso!")

if __name__ == "__main__":
    download_data() 