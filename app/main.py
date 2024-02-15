import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Base
from app.database import SessionLocal, engine
from app import services
from app.schemas import Transaction, SaldoResponse, ExtratoResponse

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/clientes/{client_id}/transacoes", response_model=SaldoResponse)
def create_transactions(client_id: int, transaction: Transaction, db: Session = Depends(get_db)):
    try:
        return services.create_client_transaction(db, transaction, client_id)
    except services.ClienteNotFound:
        raise HTTPException(status_code=404, detail="Client not found")
    except services.SaldoInsuficiente:
        raise HTTPException(status_code=422, detail="Insufficient balance")

@app.get("/clientes/{client_id}/extrato", response_model=ExtratoResponse)
def get_transactions(client_id, db: Session = Depends(get_db)):
    try:
        return services.get_extrato(db, client_id)
    except services.ClienteNotFound:
        raise HTTPException(status_code=404, detail="Client not found")
