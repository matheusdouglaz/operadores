-- Query para as 10 operadoras com maiores despesas no último trimestre
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
LIMIT 10;

-- Query para as 10 operadoras com maiores despesas no último ano
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
LIMIT 10; 