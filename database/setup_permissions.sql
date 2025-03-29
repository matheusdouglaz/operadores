-- Conectar como usuário postgres
\c postgres

-- Dar permissões necessárias ao usuário ans_user
ALTER USER ans_user WITH SUPERUSER;
GRANT ALL ON SCHEMA public TO ans_user;
GRANT ALL ON ALL TABLES IN SCHEMA public TO ans_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO ans_user;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO ans_user;

-- Conectar ao banco de dados ans_db
\c ans_db

-- Garantir que o usuário ans_user tem todas as permissões no banco
GRANT ALL ON SCHEMA public TO ans_user;
GRANT ALL ON ALL TABLES IN SCHEMA public TO ans_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO ans_user;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO ans_user; 