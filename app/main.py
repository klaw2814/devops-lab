import logging
from fastapi import FastAPI
from datetime import datetime
import platform
import socket

app = FastAPI()


@app.get("/")
def root():
    logger.info("Root endpoint accessed")

    return {
        "message": "DevOps API running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": str(datetime.now())
    }


@app.get("/system")
def system_info():
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_version": platform.version()
    }


@app.get("/hello/{name}")
def hello(name: str):
    return {
        "message": f"Hello {name}"
    }

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
