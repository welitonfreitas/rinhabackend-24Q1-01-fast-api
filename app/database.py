import os
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

Pool = psycopg2.pool.SimpleConnectionPool( 
    PG_POOL/2, PG_POOL, user=PG_USER, password=PG_PASSWORD, 
    host=PG_HOST, port=PG_PORT, database=PG_DB)

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
