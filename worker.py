import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from workflows import SendNotificationWorkflow
    from activities import send_email, send_sms, send_notification

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="my-task-queue",
        workflows=[SendNotificationWorkflow],
        activities=[send_email, send_sms, send_notification],
    )
    print("Worker started on task queue 'my-task-queue'")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())