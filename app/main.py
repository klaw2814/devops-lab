from app.database.database import SessionLocal
from app.database.models import TicketRecord
from app.database.database import engine
from app.database.models import Base
from app.models.ticket import Ticket
from fastapi.responses import JSONResponse
from fastapi import Request
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
from app.utils.time_utils import calculate_uptime
import time
from app.routes.system import router as system_router
import logging
from fastapi import FastAPI
from datetime import datetime
from app.config.settings import settings

app = FastAPI()
start_time = time.time()
app.include_router(system_router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request received: {request.method} {request.url}")

    response = await call_next(request)

    logger.info(f"Response status: {response.status_code}")

    return response

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"app": settings.APP_NAME, "environment": settings.ENVIRONMENT
}

Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc)
        }
    )

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "timestamp": str(datetime.now())
    }

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/uptime")
def uptime():
    uptime_seconds = calculate_uptime(start_time)

    return {
        "uptime_seconds": uptime_seconds
    }

@app.get("/error")
def trigger_error():
    raise Exception("Simulated application failure")

@app.post("/tickets")
def create_ticket(ticket: Ticket):
    logger.info(f"Ticket created: {ticket.title}")

    db = SessionLocal()

    db_ticket = TicketRecord(
        title=ticket.title,
        priority=ticket.priority,
        description=ticket.description
    )

    db.add(db_ticket)

    db.commit()

    db.refresh(db_ticket)

    db.close()

    return {
        "message": "Ticket created successfully",
        "ticket_id": db_ticket.id
    }

@app.get("/tickets")
def get_tickets():
    db = SessionLocal()

    tickets = db.query(TicketRecord).all()

    db.close()

    return tickets

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    db = SessionLocal()

    ticket = (
        db.query(TicketRecord)
        .filter(TicketRecord.id == ticket_id)
        .first()
    )

    db.close()

    if not ticket:
        return {
            "error": "Ticket not found"
        }

    return ticket

@app.get("/tickets/filter/")
def filter_tickets(priority: str):
    db = SessionLocal()

    tickets = (
        db.query(TicketRecord)
        .filter(TicketRecord.priority == priority)
        .all()
    )

    db.close()

    return tickets


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
