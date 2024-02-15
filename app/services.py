import datetime
from app.schemas import SaldoResponse, Transaction, Saldo, ExtratoResponse, TransactionResponse
from app.models import Transacao, Cliente
from sqlalchemy.orm import Session
from sqlalchemy import desc


class ClienteNotFound(Exception):
    pass

class SaldoInsuficiente(Exception):
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
            TransactionResponse(**transacao.__dict__) for transacao in transacoes
        ]
    return ExtratoResponse(saldo=saldo, ultimas_transacoes=transacoes_response)

def get_cliente(db: Session, client_id: int):
    return db.query(Cliente).filter(Cliente.id == client_id).first()


def get_transactions(db: Session, client_id: int, skip: int = 0, limit: int = 10):
    return db.query(Transacao).filter(Transacao.cliente_id == client_id).order_by(desc(Transacao.realizada_em)).offset(skip).limit(limit).all()

def create_client_transaction(db: Session, transaction: Transaction, client_id: int):
    cliente = get_cliente(db, client_id)
    if not cliente:
        raise ClienteNotFound()

    if transaction.tipo == "d" and cliente.saldo - transaction.valor < -cliente.limite:
        raise SaldoInsuficiente()
    
    db_transaction = Transacao(**transaction.model_dump(), cliente_id=client_id)
    db.add(db_transaction)

    if transaction.tipo == "d":
        cliente.saldo -= db_transaction.valor
    else:
        cliente.saldo += db_transaction.valor
    
    db.commit()
    
    return SaldoResponse(saldo=cliente.saldo, limite=cliente.limite)
