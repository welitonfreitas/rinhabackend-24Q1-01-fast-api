
import logging
from fastapi import FastAPI, Response
from psycopg2.extensions import connection
from app.database import Pool
from app import services
from app.schemas import Transaction, SaldoResponse, ExtratoResponse

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ENABLE_TIMING_COUT = int(os.getenv("ENABLE_TIMING_COUT") or False)

if ENABLE_TIMING_COUT:
    from fastapi_utils.timing import add_timing_middleware, record_timing
    add_timing_middleware(app, record=logger.info, prefix="app", exclude="untimed")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/clientes/{client_id}/transacoes")
def create_transactions(client_id: int, transaction: Transaction, response: Response):
    
    if not services.cliente_exists(client_id):
        response.status_code = 404
        return {"detail": "Client not found"}
    
    value = services.create_client_transaction(transaction, client_id)
    if hasattr(value, 'get') and value.get("error", None):
        response.status_code = value.get("status_code")
        return {"detail": value.get("error")}

    return value    

@app.get("/clientes/{client_id}/extrato")
def get_transactions(client_id, response: Response):
    if not services.cliente_exists(client_id):
        response.status_code = 404
        return {"detail": "Client not found"}
    
    return services.get_extrato(client_id)

