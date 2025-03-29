# Sistema de Consulta de Operadoras ANS

Sistema desenvolvido para consulta e análise de dados das operadoras de planos de saúde, incluindo web scraping, processamento de dados, banco de dados e interface web.

## Funcionalidades

- Web Scraping de dados da ANS
- Transformação e processamento de dados
- Banco de dados PostgreSQL
- API REST com Flask
- Interface web com Vue.js
- Queries analíticas

## Requisitos

- Python 3.13
- Node.js
- PostgreSQL
- Git

## Estrutura do Projeto

```
operadores/
├── api/                    # Backend em Python/Flask
│   ├── app.py             # Aplicação principal
│   ├── import_data.py     # Script de importação de dados
│   ├── executar_queries.py # Script de queries analíticas
│   ├── requirements.txt   # Dependências Python
│   └── .env              # Variáveis de ambiente
│
├── frontend/              # Frontend em Vue.js
│   ├── src/              # Código fonte
│   ├── package.json      # Dependências Node.js
│   └── vite.config.js    # Configuração do Vite
│
└── README.md             # Este arquivo
```

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/operadores.git
cd operadores
```

2. Configure o ambiente Python:
```bash
cd api
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure o banco de dados:
- Crie um banco de dados PostgreSQL
- Configure as variáveis de ambiente no arquivo `.env`:
```
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ans
```

4. Configure o frontend:
```bash
cd frontend
npm install
```

## Executando o Projeto

1. Inicie o servidor backend:
```bash
cd api
python app.py
```

2. Em outro terminal, inicie o frontend:
```bash
cd frontend
npm run dev
```

3. Acesse a aplicação:
- Frontend: http://localhost:5173
- Backend: http://127.0.0.1:5000

## API Endpoints

- `GET /operadoras` - Lista todas as operadoras
- `GET /operadoras/<cnpj>` - Obtém detalhes de uma operadora
- `GET /operadoras/busca?q=<termo>` - Busca operadoras por termo
- `GET /analise/ultimo-trimestre` - Top 10 operadoras no último trimestre
- `GET /analise/ultimo-ano` - Top 10 operadoras no último ano

## Testando com Postman

1. Importe a coleção fornecida no Postman
2. Teste as rotas disponíveis
3. Verifique os resultados das queries analíticas

## Queries Analíticas

O sistema inclui queries para:
- Top 10 operadoras com maiores despesas no último trimestre
- Top 10 operadoras com maiores despesas no último ano

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request
