-- Configurar o formato da data
SET datestyle TO 'ISO, YMD';

-- Criar tabela temporária para operadoras
CREATE TEMP TABLE temp_operadoras (
    registro_ans VARCHAR(20),
    cnpj VARCHAR(14),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(50),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(2),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    email VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    data_registro VARCHAR(10),
    regiao_comercializacao VARCHAR(100)
);

-- Criar tabela temporária para demonstrações
CREATE TEMP TABLE temp_demonstracoes (
    data_referencia DATE,
    registro_ans VARCHAR(20),
    cd_conta_contabil VARCHAR(20),
    descricao VARCHAR(255),
    vl_saldo_inicial VARCHAR(20),
    vl_saldo_final VARCHAR(20)
);

-- Importar dados para tabelas temporárias
\copy temp_operadoras FROM 'data/operadoras.csv' WITH (FORMAT csv, HEADER true, DELIMITER ';', NULL '', ENCODING 'UTF8', QUOTE '"');
\copy temp_demonstracoes FROM 'data/1T2024.csv' WITH (FORMAT csv, HEADER true, DELIMITER ';', NULL '', ENCODING 'UTF8', QUOTE '"');

-- Inserir dados nas tabelas finais
INSERT INTO operadoras 
SELECT DISTINCT ON (registro_ans) 
    registro_ans, cnpj, razao_social, nome_fantasia, modalidade, 
    logradouro, numero, complemento, bairro, cidade, uf, cep, 
    ddd, telefone, fax, email, representante, cargo_representante, 
    CASE 
        WHEN data_registro ~ '^[0-9]+$' THEN 
            (data_registro::integer || ' days')::interval + '2024-01-01'::date
        ELSE NULL 
    END
FROM temp_operadoras;

-- Inserir dados nas demonstrações contábeis
INSERT INTO demonstracoes_contabeis (data_referencia, registro_ans, valor_patrimonio_liquido)
SELECT 
    data_referencia,
    registro_ans,
    CASE 
        WHEN vl_saldo_final ~ '^[0-9]+([.,][0-9]+)?$' THEN 
            REPLACE(vl_saldo_final, ',', '.')::numeric 
        ELSE NULL 
    END
FROM temp_demonstracoes
WHERE cd_conta_contabil = '463919'
AND registro_ans IN (SELECT registro_ans FROM operadoras);

-- Limpar tabelas temporárias
DROP TABLE temp_operadoras;
DROP TABLE temp_demonstracoes;