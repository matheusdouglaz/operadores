-- Criar tabela de operadoras
CREATE TABLE IF NOT EXISTS operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY,
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
    data_registro DATE
);

-- Criar tabela de demonstrações contábeis
CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(20),
    razao_social VARCHAR(255),
    data_referencia DATE,
    valor_capital_social DECIMAL(15,2),
    valor_patrimonio_liquido DECIMAL(15,2),
    valor_total_ativo DECIMAL(15,2),
    valor_total_passivo DECIMAL(15,2),
    valor_receita_bruta DECIMAL(15,2),
    valor_receita_operacional DECIMAL(15,2),
    valor_despesa_operacional DECIMAL(15,2),
    valor_resultado_operacional DECIMAL(15,2),
    valor_resultado_financeiro DECIMAL(15,2),
    valor_resultado_antes_ir_csll DECIMAL(15,2),
    valor_resultado_apos_ir_csll DECIMAL(15,2),
    valor_resultado_liquido DECIMAL(15,2),
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans)
);

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_dc_registro_ans ON demonstracoes_contabeis(registro_ans);
CREATE INDEX IF NOT EXISTS idx_dc_data_referencia ON demonstracoes_contabeis(data_referencia); 