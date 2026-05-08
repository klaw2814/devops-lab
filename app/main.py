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

    return {
        "message": "Ticket created successfully",
        "ticket": ticket
    }

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
