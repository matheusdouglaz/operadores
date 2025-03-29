-- Query para as 10 operadoras com maiores despesas no último trimestre
WITH ultimo_trimestre AS (
    SELECT MAX(data_referencia) as ultima_data
    FROM demonstracoes_contabeis
)
SELECT 
    o.razao_social,
    o.nome_fantasia,
    SUM(dc.valor) as total_despesas
FROM demonstracoes_contabeis dc
JOIN operadoras o ON dc.registro_ans = o.registro_ans
CROSS JOIN ultimo_trimestre ut
WHERE 
    dc.data_referencia >= ut.ultima_data - INTERVAL '3 months'
    AND dc.tipo_demonstracao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
GROUP BY o.razao_social, o.nome_fantasia
ORDER BY total_despesas DESC
LIMIT 10;

-- Query para as 10 operadoras com maiores despesas no último ano
WITH ultimo_ano AS (
    SELECT MAX(data_referencia) as ultima_data
    FROM demonstracoes_contabeis
)
SELECT 
    o.razao_social,
    o.nome_fantasia,
    SUM(dc.valor) as total_despesas
FROM demonstracoes_contabeis dc
JOIN operadoras o ON dc.registro_ans = o.registro_ans
CROSS JOIN ultimo_ano ua
WHERE 
    dc.data_referencia >= ua.ultima_data - INTERVAL '1 year'
    AND dc.tipo_demonstracao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
GROUP BY o.razao_social, o.nome_fantasia
ORDER BY total_despesas DESC
LIMIT 10; 