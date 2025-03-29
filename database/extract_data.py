import os
import zipfile
import pandas as pd

def extract_data():
    data_dir = "data"
    
    # Extrair arquivo ZIP das demonstrações contábeis
    zip_file = "1T2024.zip"  # ou o nome do arquivo ZIP que você baixou
    zip_path = os.path.join(data_dir, zip_file)
    
    if os.path.exists(zip_path):
        print(f"Extraindo arquivo {zip_file}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
        print("Extração concluída!")
    else:
        print(f"Arquivo {zip_file} não encontrado na pasta {data_dir}")
    
    # Listar arquivos na pasta data
    print("\nArquivos na pasta data:")
    for file in os.listdir(data_dir):
        print(f"- {file}")

if __name__ == "__main__":
    extract_data() 