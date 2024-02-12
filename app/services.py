import datetime
from app.schemas import SaldoResponse, Transaction, Saldo, ExtratoResponse, TransactionResponse
from app.models import Transacao, Cliente
from sqlalchemy.orm import Session


class ClienteNotFound(Exception):
    pass

def get_extrato(db: Session, client_id: int):
    cliente =  get_cliente(db, client_id)
    if not cliente:
        raise ClienteNotFound()
    
    transacoes = get_transactions(db, client_id)
    total = cliente.saldo
    limite = cliente.limite
    saldo = Saldo(total=total, limite=limite, data_extrato=datetime.datetime.utcnow())
    transacoes_response = [
            TransactionResponse(**transacao) for transacao in transacoes
        ]
    return ExtratoResponse(saldo=saldo, ultimas_transacoes=transacoes_response)

def get_cliente(db: Session, client_id: int):
    return db.query(Cliente).filter(Cliente.id == client_id).first()


def get_transactions(db: Session, client_id: int, skip: int = 0, limit: int = 10):
    return db.query(Transacao).filter(Transacao.cliente_id == client_id).offset(skip).limit(limit).all()

def create_client_transaction(db: Session, transaction: Transaction, client_id: int):
    cliente = get_cliente(db, client_id)
    if not cliente:
        raise ClienteNotFound()

    db_transaction = Transacao(**transaction.dict(), cliente_id=client_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return SaldoResponse(saldo=1000, limite=1000)
