import asyncio
import uuid
from temporalio.client import Client
from faker_service import FakerService

async def main():
    print("=" * 80)
    print("Temporal Notification Workflow Starter")
    print("=" * 80 + "\n")
    
    try:
        client = await Client.connect("localhost:7233")
        print("Connected to Temporal server\n")
    except Exception as e:
        print(f"Failed to connect to Temporal: {e}")
        print("Make sure Temporal server is running on localhost:7233")
        return
    
    print("Example 1: Single Notification (Email + SMS)")
    print("-" * 80)
    notif_data = FakerService.generate_notification_data()
    notif_workflow_id = f"send-notification-{uuid.uuid4()}"
    
    try:
        result = await client.execute_workflow(
            "SendNotificationWorkflow",
            args=[notif_data["email"], notif_data["phone"], notif_data["subject"], notif_data["message"]],
            id=notif_workflow_id,
            task_queue="my-task-queue",
        )
        print(f"Notification sent!")
        print(f"    Email: {notif_data['email']}")
        print(f"    Phone: {notif_data['phone']}")
        print(f"    Subject: {notif_data['subject']}")
        print(f"    Result: {result}\n")
    except Exception as e:
        print(f"Error sending notification: {e}\n")
    
    print("Example 2: Batch Processing (5 Notifications)")
    print("-" * 80)
    batch_data = FakerService.generate_batch(5)
    
    try:
        for i, data in enumerate(batch_data, 1):
            workflow_id = f"send-notification-batch-{i}-{uuid.uuid4()}"
            
            result = await client.execute_workflow(
                "SendNotificationWorkflow",
                args=[data["email"], data["phone"], data["subject"], data["message"]],
                id=workflow_id,
                task_queue="my-task-queue",
            )
            print(f"  {i}. Notification sent to {data['email']}")
        print()
    except Exception as e:
        print(f"Error in batch processing: {e}\n")
    
    print("=" * 80)
    print("All examples completed!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Check Temporal Web UI at http://localhost:8080 to view workflows")
    print("2. Use the FastAPI server to send notifications via HTTP:")
    print("   - Start server: python main.py")
    print("   - View API docs: http://localhost:8000/docs")
    print("3. Run the test client: python test_client.py")

if __name__ == "__main__":
    asyncio.run(main())
