import datetime
from app.schemas import SaldoResponse, Transaction, Saldo, ExtratoResponse, TransactionResponse
from psycopg2.extensions import connection
from app.database import get_db

# criar objeto de cache em memoria para consultas de cliente

client_cache = {}

class ClienteNotFound(Exception):
    pass

class SaldoInsuficiente(Exception):
    pass

def get_extrato(client_id: int):
    total = 0
    limite = 0
    with get_db() as db:
        cliente =  get_cliente(db, client_id)
        transacoes = get_transactions(db, client_id)
        total = cliente[0]
        limite = cliente[1]
    
    saldo = Saldo(total=total, limite=limite, data_extrato=datetime.datetime.utcnow())
    transacoes_response = [
            TransactionResponse(valor=transacao[0], tipo=transacao[1], descricao=transacao[2], realizada_em=transacao[3]) for transacao in transacoes
        ]
    return ExtratoResponse(saldo=saldo, ultimas_transacoes=transacoes_response)

def client_exists(client_id: int):
    client = client_cache.get(client_id, None)
    if client:
        return client.get("exists", False), client.get("limite", 0)

    with get_db() as db:
        client = get_cliente(db, client_id)
        if not client:
            client_cache[client_id] = {"exists": False, "limite": 0}
            return False, 0
        else:
            client_cache[client_id] = {"exists": True, "limite": client[1]}
            return True, client[1]
    

def get_cliente(db: connection, client_id: int):
    db.execute("SELECT saldo, limite FROM clientes WHERE id = %s", (client_id,))
    client = db.fetchone()
    return client


def get_transactions(db: connection, client_id: int, skip: int = 0, limit: int = 10):
    db.execute("SELECT valor, tipo, descricao, realizada_em FROM transacoes WHERE cliente_id = %s ORDER BY realizada_em DESC OFFSET %s LIMIT %s", (client_id, skip, limit))
    return db.fetchall()

def create_client_transaction(transaction: Transaction, client_id: int):

    _, limite = client_exists(client_id)
    saldo = 0
    valor = transaction.valor
    now = datetime.datetime.utcnow()
    with get_db() as db:
        if transaction.tipo == "d":
            valor = -transaction.valor
        
        try:
            db.execute("select altera_saldo_cliente(%s, %s);", (client_id, valor))
            saldo = db.fetchone()[0]
        except Exception as e:
            return {"error": "Insufficient balance", "status_code": 422}

        insert = """
        INSERT INTO transacoes (tipo, valor, descricao, cliente_id, realizada_em) VALUES (%s, %s, %s, %s, %s);
        """
        db.execute(insert, (transaction.tipo.value, transaction.valor, transaction.descricao, client_id, now))
    
    return SaldoResponse(saldo=saldo, limite=limite)
