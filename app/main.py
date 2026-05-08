import time
from app.routes.system import router as system_router
import logging
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()
start_time = time.time()
app.include_router(system_router)


@app.get("/")
def root():
    logger.info("Root endpoint accessed")

    return {"message": "DevOps API running"}


@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": str(datetime.now())}


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/uptime")
def uptime():
    current_time = time.time()

    uptime_seconds = round(current_time - start_time, 2)

    return {
        "uptime_seconds": uptime_seconds
    }


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
