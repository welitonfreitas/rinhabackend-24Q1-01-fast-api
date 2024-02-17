from fastapi import FastAPI, Depends, HTTPException
from psycopg2.extensions import connection
from app.database import Pool
from app import services
from app.schemas import Transaction, SaldoResponse, ExtratoResponse


# Dependency
def get_db():
    connection = Pool.getconn()
    db = connection.cursor()
    try:
        yield db
    finally:
        connection.commit()
        db.close()
        Pool.putconn(connection)

app = FastAPI()

@app.post("/clientes/{client_id}/transacoes", response_model=SaldoResponse)
def create_transactions(client_id: int, transaction: Transaction, db: connection = Depends(get_db)):
    try:
        return services.create_client_transaction(db, transaction, client_id)
    except services.ClienteNotFound:
        raise HTTPException(status_code=404, detail="Client not found")
    except services.SaldoInsuficiente:
        raise HTTPException(status_code=422, detail="Insufficient balance")

@app.get("/clientes/{client_id}/extrato", response_model=ExtratoResponse)
def get_transactions(client_id, db: connection = Depends(get_db)):
    try:
        return services.get_extrato(db, client_id)
    except services.ClienteNotFound:
        raise HTTPException(status_code=404, detail="Client not found")
