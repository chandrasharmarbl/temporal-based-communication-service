import uuid
import logging
from fastapi import APIRouter, Depends, HTTPException
from temporalio.client import Client
from app.api.dependencies import get_temporal_client
from app.schemas.notification import SendNotificationRequest, WorkflowResponse
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health")
async def health_check(client: Client = Depends(get_temporal_client)):
    try:
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

@router.post("/send-notification", response_model=WorkflowResponse)
async def send_notification(
    request: SendNotificationRequest,
    client: Client = Depends(get_temporal_client)
):
    try:
        workflow_id = f"send-notification-{uuid.uuid4()}"
        
        # Execute workflow synchronously (waits for completion)
        result = await client.execute_workflow(
            "SendNotificationWorkflow",
            args=[request.email, request.phone_number, request.subject, request.message],
            id=workflow_id,
            task_queue=settings.TEMPORAL_TASK_QUEUE,
        )
        
        logger.info(f"Notification workflow completed: {workflow_id}")
        return WorkflowResponse(
            workflow_id=workflow_id,
            status="completed",
            message=f"Notification sent to {request.email} and {request.phone_number}",
            result=result
        )
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-notification-async", response_model=WorkflowResponse)
async def send_notification_async(
    request: SendNotificationRequest,
    client: Client = Depends(get_temporal_client)
):
    try:
        workflow_id = f"send-notification-async-{uuid.uuid4()}"
        
        # Start workflow asynchronously (returns immediately)
        handle = await client.start_workflow(
            "SendNotificationWorkflow",
            args=[request.email, request.phone_number, request.subject, request.message],
            id=workflow_id,
            task_queue=settings.TEMPORAL_TASK_QUEUE,
        )
        
        logger.info(f"Notification workflow started: {workflow_id}")
        return WorkflowResponse(
            workflow_id=workflow_id,
            status="started",
            message="Notification workflow started. Use workflow_id to track progress."
        )
    except Exception as e:
        logger.error(f"Error starting notification workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workflow/{workflow_id}")
async def get_workflow_status(
    workflow_id: str,
    client: Client = Depends(get_temporal_client)
):
    try:
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
                "status": str(describe.status),
                "started_at": describe.start_time,
                "message": "Workflow is still executing or failed"
            }
    except Exception as e:
        logger.error(f"Error getting workflow status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
