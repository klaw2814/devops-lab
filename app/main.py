from app.routes.system import router as system_router
import logging
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()
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


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
