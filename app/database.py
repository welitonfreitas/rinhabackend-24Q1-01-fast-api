import os
import time
import psycopg2
import psycopg2.pool
import contextlib
PG_HOST = os.getenv("PG_HOST") or "localhost"
PG_PORT = os.getenv("PG_PORT") or 5432
PG_USER = os.getenv("PG_USER") or "postgres"
PG_PASSWORD = os.getenv("PG_PASSWORD") or "postgres"
PG_DB = os.getenv("PG_DB") or "rinha_db"
PG_POOL = int(os.getenv("PG_POOL") or 10)

# Connection = psycopg2.connect(database=PG_DB,
#                         host=PG_HOST,
#                         user=PG_USER,
#                         password=PG_PASSWORD,
#                         port=PG_PORT)

# tenta reconectar até que o postgres esteja pronto para receber conexões
Pool = None
while not Pool:
    try:
        Pool = psycopg2.pool.SimpleConnectionPool( 
            PG_POOL/2, PG_POOL, user=PG_USER, password=PG_PASSWORD, 
            host=PG_HOST, port=PG_PORT, database=PG_DB)
    except psycopg2.OperationalError as erro:
        print(erro)
        time.sleep(1)

# outra solução possível seria checar se o postgres está pronto com healthcheck no seu docker-compose.yml
# api01: &app
#   [...] demais configurações
#   depends_on:
#     rinha-db:
#       condition: service_healthy
#
# rinha-db:
#   [...] demais configurações
#   healthcheck:
#     test: ["CMD-SHELL", "pg_isready"]
#     interval: 5s
#     timeout: 5s
#     retries: 4
# assim não seria preciso mexer no código, mas o docker ficará verificando o container do postgres constantemente de 5 em 5 segundos... o que consumirá processamento do container

# Dependency
@contextlib.contextmanager
def get_db():
    connection = Pool.getconn()
    db = connection.cursor()
    try:
        yield db
    finally:
        connection.commit()
        db.close()
        Pool.putconn(connection)
