import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True)
    valor = Column(Integer)
    descricao = Column(String)
    tipo = Column(String)
    realizada_em = Column(DateTime, default=datetime.datetime.utcnow)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    cliente = relationship("Cliente", back_populates="transacoes")

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    limite = Column(Integer)
    saldo = Column(Integer)
    nome = Column(String)
    transacoes = relationship("Transacao", back_populates="cliente")
