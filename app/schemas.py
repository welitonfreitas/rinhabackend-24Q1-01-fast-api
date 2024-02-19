import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, conint

class TransactionType(str, Enum):
    deposito = "d"
    credito = "c"

class Transaction(BaseModel):
    valor: conint(strict=True, gt=0)
    tipo: TransactionType
    # string de 1 a 10 caracteres
    descricao: str = Field(min_length=1, max_length=10)

class SaldoResponse(BaseModel):
    limite: int
    saldo: int

class TransactionResponse(Transaction):
    realizada_em: datetime.datetime


class Saldo(BaseModel):
    total: Optional[int] = 0
    data_extrato: datetime.datetime
    limite: int

class ExtratoResponse(BaseModel):
    saldo: Saldo
    ultimas_transacoes: List[TransactionResponse]
