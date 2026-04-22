import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio import workflow

from app.core.config import settings

with workflow.unsafe.imports_passed_through():
    from app.temporal.workflows import SendNotificationWorkflow
    from app.temporal.activities import send_email, send_sms, send_notification

async def main():
    client = await Client.connect(settings.TEMPORAL_SERVER_URL)
    worker = Worker(
        client,
        task_queue=settings.TEMPORAL_TASK_QUEUE,
        workflows=[SendNotificationWorkflow],
        activities=[send_email, send_sms, send_notification],
    )
    print(f"Worker started on task queue '{settings.TEMPORAL_TASK_QUEUE}' connecting to '{settings.TEMPORAL_SERVER_URL}'")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
