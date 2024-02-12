import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class TransactionType(str, Enum):
    deposito = "d"
    credito = "c"

class Transaction(BaseModel):
    valor: int
    tipo: TransactionType
    descricao: str

class SaldoResponse(BaseModel):
    limite: int
    saldo: int

class TransactionResponse(Transaction):
    realizada_em: datetime.datetime
    class Config:
        orm_mode = True

class Saldo(BaseModel):
    total: Optional[int] = 0
    data_extrato: datetime.datetime
    limite: int
    class Config:
        orm_mode = True

class ExtratoResponse(BaseModel):
    saldo: Saldo
    ultimas_transacoes: List[TransactionResponse]
    class Config:
        orm_mode = True