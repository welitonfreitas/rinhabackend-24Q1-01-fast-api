--ALTER SYSTEM SET max_connections = 200;

DO $$
BEGIN
  
  CREATE TABLE if NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    limite INTEGER NOT NULL,
    saldo INTEGER NOT NULL
  );

  CREATE TABLE if NOT EXISTS transacoes (
    id SERIAL PRIMARY KEY,
    valor INTEGER NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    tipo VARCHAR(1) NOT NULL,
    realizada_em TIMESTAMP NOT NULL,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
  );

  INSERT INTO clientes (nome, limite, saldo)
  VALUES
    ('o barato sai caro', 1000 * 100, 0),
    ('zan corp ltda', 800 * 100, 0),
    ('les cruders', 10000 * 100, 0),
    ('padaria joia de cocaia', 100000 * 100, 0),
    ('kid mais', 5000 * 100, 0);
END; $$
