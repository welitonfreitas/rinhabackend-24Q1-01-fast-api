import datetime
from app.schemas import SaldoResponse, Transaction, Saldo, ExtratoResponse, TransactionResponse
from psycopg2.extensions import connection

class ClienteNotFound(Exception):
    pass

class SaldoInsuficiente(Exception):
    pass

def get_extrato(db: connection, client_id: int):
    cliente =  get_cliente(db, client_id)
    transacoes = get_transactions(db, client_id)
    
    total = cliente[0]
    limite = cliente[1]
    
    saldo = Saldo(total=total, limite=limite, data_extrato=datetime.datetime.utcnow())
    transacoes_response = [
            TransactionResponse(valor=transacao[0], tipo=transacao[1], descricao=transacao[2], realizada_em=transacao[3]) for transacao in transacoes
        ]
    return ExtratoResponse(saldo=saldo, ultimas_transacoes=transacoes_response)

def get_cliente(db: connection, client_id: int):
    db.execute("SELECT saldo, limite FROM clientes WHERE id = %s", (client_id,))
    client = db.fetchone()
    print(client)
    if not client:
        raise ClienteNotFound()
    return client


def get_transactions(db: connection, client_id: int, skip: int = 0, limit: int = 10):
    db.execute("SELECT valor, tipo, descricao, realizada_em FROM transacoes WHERE cliente_id = %s ORDER BY realizada_em DESC OFFSET %s LIMIT %s", (client_id, skip, limit))
    return db.fetchall()

def create_client_transaction(db: connection, transaction: Transaction, client_id: int):
    cliente = get_cliente(db, client_id)

    saldo = cliente[0]
    limite = cliente[1]
    novo_saldo = saldo + transaction.valor if transaction.tipo == "c" else saldo - transaction.valor

    if transaction.tipo == "d" and (saldo - transaction.valor) < -limite:
        raise SaldoInsuficiente()

    now = datetime.datetime.utcnow()
    insert = """
    INSERT INTO transacoes (tipo, valor, descricao, cliente_id, realizada_em) VALUES (%s, %s, %s, %s, %s);
    UPDATE clientes SET saldo = %s WHERE id = %s;
    """

    db.execute(insert, (transaction.tipo.value, transaction.valor, transaction.descricao, client_id, now, novo_saldo, client_id))
    
    return SaldoResponse(saldo=novo_saldo, limite=limite)
