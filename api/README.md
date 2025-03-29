# API de Consulta de Operadoras ANS

Este é o backend da aplicação de consulta de operadoras da ANS.

## Requisitos

- Python 3.8+
- Flask
- pandas
- flask-cors

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Certifique-se de que o arquivo CSV das operadoras está no diretório correto:
```
database/data/operadoras.csv
```

## Executando a API

```bash
python app.py
```

A API estará disponível em `http://localhost:5000`

## Endpoints

### GET /api/operadoras/search

Busca operadoras por texto.

Parâmetros:
- `q`: Texto para busca (query string)

Exemplo:
```
GET /api/operadoras/search?q=saude
```

Resposta:
```json
[
  {
    "registro_ans": "123456",
    "razao_social": "Empresa de Saúde",
    "nome_fantasia": "Saúde Plus",
    "cidade": "São Paulo",
    "uf": "SP",
    ...
  }
]
``` 