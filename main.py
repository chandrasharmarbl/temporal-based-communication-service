import asyncio
import uuid
from datetime import timedelta
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from temporalio.client import Client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Temporal Notification Microservice",
    description="Send emails and SMS through Temporal workflows",
    version="1.0.0"
)

_client: Optional[Client] = None


class SendNotificationRequest(BaseModel):
    email: EmailStr
    phone_number: str
    subject: str
    message: str

class WorkflowResponse(BaseModel):
    workflow_id: str
    status: str
    message: str


@app.on_event("startup")
async def startup_event():
    global _client
    try:
        _client = await Client.connect("localhost:7233")
        logger.info("Connected to Temporal server")
    except Exception as e:
        logger.error(f"Failed to connect to Temporal server: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    global _client
    if _client:
        _client.close()
        logger.info("Disconnected from Temporal server")


async def get_client() -> Client:
    if not _client:
        raise HTTPException(
            status_code=503,
            detail="Temporal client not initialized. Server may still be starting."
        )
    return _client


@app.get("/health")
async def health_check():
    try:
        client = await get_client()
        await client.describe_namespace("default")
        return {
            "status": "healthy",
            "temporal": "connected"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )


@app.post("/send-notification", response_model=WorkflowResponse)
async def send_notification(request: SendNotificationRequest):
    try:
        client = await get_client()
        workflow_id = f"send-notification-{uuid.uuid4()}"
        
        result = await client.execute_workflow(
            "SendNotificationWorkflow",
            args=[request.email, request.phone_number, request.subject, request.message],
            id=workflow_id,
            task_queue="my-task-queue",
        )
        
        logger.info(f"Notification workflow completed: {workflow_id}")
        return WorkflowResponse(
            workflow_id=workflow_id,
            status="completed",
            message=f"Notification sent to {request.email} and {request.phone_number}"
        )
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/send-notification-async", response_model=WorkflowResponse)
async def send_notification_async(request: SendNotificationRequest):
    try:
        client = await get_client()
        workflow_id = f"send-notification-async-{uuid.uuid4()}"
        
        handle = await client.start_workflow(
            "SendNotificationWorkflow",
            args=[request.email, request.phone_number, request.subject, request.message],
            id=workflow_id,
            task_queue="my-task-queue",
        )
        
        logger.info(f"Notification workflow started: {workflow_id}")
        return WorkflowResponse(
            workflow_id=workflow_id,
            status="started",
            message=f"Notification workflow started. Use workflow_id to track progress."
        )
    except Exception as e:
        logger.error(f"Error starting notification workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflow/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    try:
        client = await get_client()
        handle = client.get_workflow_handle(workflow_id)
        
        try:
            result = await handle.result()
            return {
                "workflow_id": workflow_id,
                "status": "completed",
                "result": result
            }
        except Exception as e:
            describe = await handle.describe()
            return {
                "workflow_id": workflow_id,
                "status": "running",
                "started_at": describe.start_time,
                "message": "Workflow is still executing"
            }
    except Exception as e:
        logger.error(f"Error getting workflow status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {
        "service": "Temporal Notification Microservice",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "send_notification": "POST /send-notification",
            "send_notification_async": "POST /send-notification-async",
            "workflow_status": "GET /workflow/{workflow_id}",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
