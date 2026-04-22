import logging
from fastapi import FastAPI
from temporalio.client import Client
from app.api.endpoints import router
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Temporal Notification Microservice",
    description="Send emails and SMS through Temporal workflows with Clean Architecture",
    version="2.0.0"
)

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    try:
        app.state.temporal_client = await Client.connect(settings.TEMPORAL_SERVER_URL)
        logger.info(f"Connected to Temporal server at {settings.TEMPORAL_SERVER_URL}")
    except Exception as e:
        logger.error(f"Failed to connect to Temporal server: {e}")
        # Not raising here so the API can still start and return 503 on endpoints

@app.on_event("shutdown")
async def shutdown_event():
    client = getattr(app.state, "temporal_client", None)
    if client:
        logger.info("Disconnected from Temporal server")

@app.get("/")
async def root():
    return {
        "service": "Temporal Notification Microservice",
        "version": "2.0.0",
        "endpoints": {
            "health": "/health",
            "send_notification": "POST /send-notification",
            "send_notification_async": "POST /send-notification-async",
            "workflow_status": "GET /workflow/{workflow_id}",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }
