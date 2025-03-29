import os
import pandas as pd
import PyPDF2
import re
import zipfile
from datetime import datetime

def extract_table_from_pdf(pdf_path):
    print(f"Processando arquivo: {pdf_path}")
    # Abrir o PDF
    with open(pdf_path, 'rb') as file:
        # Criar objeto PDF reader
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Lista para armazenar todas as linhas da tabela
        all_rows = []
        
        # Processar cada página
        total_pages = len(pdf_reader.pages)
        print(f"Total de páginas encontradas: {total_pages}")
        
        for page_num, page in enumerate(pdf_reader.pages, 1):
            print(f"Processando página {page_num}/{total_pages}")
            text = page.extract_text()
            
            # Dividir o texto em linhas
            lines = text.split('\n')
            
            # Processar cada linha
            for line in lines:
                # Padrão para identificar linhas da tabela
                # Ajuste este padrão de acordo com o formato real do PDF
                if re.match(r'^\d+\s+', line):
                    # Dividir a linha em colunas
                    columns = re.split(r'\s{2,}', line.strip())
                    if len(columns) >= 4:  # Garantir que temos pelo menos as colunas necessárias
                        all_rows.append(columns)
    
    print(f"Total de linhas extraídas: {len(all_rows)}")
    
    # Criar DataFrame
    df = pd.DataFrame(all_rows, columns=['Código', 'Descrição', 'OD', 'AMB'])
    
    # Substituir abreviações
    df['OD'] = df['OD'].replace({'S': 'Sim', 'N': 'Não'})
    df['AMB'] = df['AMB'].replace({'S': 'Sim', 'N': 'Não'})
    
    return df

def process_pdf_to_csv():
    # Diretório dos downloads
    downloads_dir = "../web_scraping/downloads"
    
    # Criar diretório se não existir
    if not os.path.exists(downloads_dir):
        print(f"Criando diretório {downloads_dir}")
        os.makedirs(downloads_dir)
        print("Por favor, execute primeiro o script web_scraping/download_pdfs.py para baixar os PDFs")
        return
    
    # Encontrar o arquivo Anexo I
    anexo1_file = None
    for file in os.listdir(downloads_dir):
        if 'Anexo I' in file and file.endswith('.pdf'):
            anexo1_file = os.path.join(downloads_dir, file)
            break
    
    if not anexo1_file:
        print("Arquivo Anexo I não encontrado no diretório downloads")
        print("Por favor, execute primeiro o script web_scraping/download_pdfs.py para baixar os PDFs")
        return
    
    # Extrair dados do PDF
    print("Extraindo dados do PDF...")
    df = extract_table_from_pdf(anexo1_file)
    
    # Criar diretório para saída se não existir
    output_dir = "output"
    if not os.path.exists(output_dir):
        print(f"Criando diretório de saída: {output_dir}")
        os.makedirs(output_dir)
    
    # Salvar CSV
    csv_filename = "rol_procedimentos.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    print(f"Salvando arquivo CSV: {csv_path}")
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"CSV criado com sucesso: {csv_filename}")
    
    # Criar ZIP
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"Teste_{timestamp}.zip"
    zip_path = os.path.join(output_dir, zip_filename)
    
    print(f"Criando arquivo ZIP: {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_path, csv_filename)
    
    print(f"Arquivo ZIP criado com sucesso: {zip_filename}")
    print("\nProcesso concluído com sucesso!")

if __name__ == "__main__":
    process_pdf_to_csv() 