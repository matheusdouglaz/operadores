import os
import requests
from bs4 import BeautifulSoup
import zipfile
from datetime import datetime

def download_pdfs():
    # URL do site
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    
    # Criar diretório para downloads se não existir
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
        print("Diretório 'downloads' criado")
    
    try:
        # Fazer requisição para a página
        print(f"Acessando {url}...")
        response = requests.get(url)
        response.raise_for_status()
        
        # Parsear o HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar links dos PDFs
        print("Procurando links dos PDFs...")
        pdf_links = []
        
        # Procurar por links que contenham 'Anexo I' ou 'Anexo II' e terminem com '.pdf'
        for link in soup.find_all('a'):
            href = link.get('href', '')
            text = link.get_text()
            
            # Verificar se é um link para PDF e contém Anexo I ou II
            if (href.endswith('.pdf') and 
                ('Anexo I' in text or 'Anexo II' in text)):
                
                # Se o link começar com /, adicionar o domínio
                if href.startswith('/'):
                    href = 'https://www.gov.br' + href
                
                print(f"Link encontrado: {href}")
                pdf_links.append(href)
        
        print(f"Links dos anexos encontrados: {len(pdf_links)}")
        
        if not pdf_links:
            print("Nenhum link de PDF encontrado. Tentando método alternativo...")
            # Método alternativo: procurar por links que contenham 'Anexo' e '.pdf'
            for link in soup.find_all('a'):
                href = link.get('href', '')
                if 'Anexo' in href and '.pdf' in href:
                    if href.startswith('/'):
                        href = 'https://www.gov.br' + href
                    print(f"Link encontrado (método alternativo): {href}")
                    pdf_links.append(href)
        
        if not pdf_links:
            raise Exception("Nenhum link de PDF encontrado na página")
        
        # Download dos PDFs
        for link in pdf_links:
            filename = link.split('/')[-1]
            # Limpar o nome do arquivo
            filename = filename.split('?')[0]  # Remover parâmetros da URL
            filepath = os.path.join("downloads", filename)
            
            print(f"Baixando {filename}...")
            pdf_response = requests.get(link)
            pdf_response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(pdf_response.content)
            
            print(f"Download concluído: {filename}")
        
        # Criar arquivo ZIP
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"anexos_{timestamp}.zip"
        zip_path = os.path.join("downloads", zip_filename)
        
        print(f"Criando arquivo ZIP: {zip_filename}")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in os.listdir("downloads"):
                if file.endswith('.pdf'):
                    filepath = os.path.join("downloads", file)
                    zipf.write(filepath, file)
                    print(f"Adicionando ao ZIP: {file}")
        
        print(f"\nArquivo ZIP criado com sucesso: {zip_filename}")
        
    except Exception as e:
        print(f"Erro durante o processo: {str(e)}")

if __name__ == "__main__":
    download_pdfs() 