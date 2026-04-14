import asyncio
import httpx
from faker_service import FakerService

BASE_URL = "http://localhost:8000"

async def test_health():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/health")
            print("Health Check:")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}\n")
            return response.status_code == 200
        except Exception as e:
            print(f"Health check failed: {e}\n")
            return False


async def test_send_notification():
    data = FakerService.generate_notification_data()
    
    payload = {
        "email": data["email"],
        "phone_number": data["phone"],
        "subject": data["subject"],
        "message": data["message"]
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{BASE_URL}/send-notification", json=payload)
            print("Send Notification (Sync - Email + SMS):")
            print(f"   Email: {data['email']}")
            print(f"   Phone: {data['phone']}")
            print(f"   Subject: {data['subject']}")
            print(f"   Response: {response.json()}\n")
            return response.status_code == 200
        except Exception as e:
            print(f"Send notification failed: {e}\n")
            return False


async def test_send_notification_async():
    data = FakerService.generate_notification_data()
    
    payload = {
        "email": data["email"],
        "phone_number": data["phone"],
        "subject": data["subject"],
        "message": data["message"]
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{BASE_URL}/send-notification-async", json=payload)
            print("Send Notification (Async - Email + SMS):")
            print(f"   Email: {data['email']}")
            print(f"   Phone: {data['phone']}")
            print(f"   Subject: {data['subject']}")
            result = response.json()
            print(f"   Workflow ID: {result['workflow_id']}")
            print(f"   Status: {result['status']}\n")
            return response.status_code == 200
        except Exception as e:
            print(f"Send notification async failed: {e}\n")
            return False


async def test_get_workflow_status(workflow_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/workflow/{workflow_id}")
            print(f"Workflow Status for {workflow_id}:")
            print(f"   Response: {response.json()}\n")
            return response.status_code == 200
        except Exception as e:
            print(f"Get workflow status failed: {e}\n")
            return False


async def main():
    print("=" * 80)
    print("Temporal Notification Microservice - Test Client")
    print("=" * 80 + "\n")
    
    await asyncio.sleep(1)
    
    health_ok = await test_health()
    if not health_ok:
        print("Service is not healthy. Make sure Temporal and FastAPI servers are running.\n")
        return
    
    results = []
    results.append(("Health Check", health_ok))
    results.append(("Send Notification (Sync)", await test_send_notification()))
    results.append(("Send Notification (Async)", await test_send_notification_async()))
    
    print("=" * 80)
    print("Test Summary:")
    print("=" * 80)
    for name, passed in results:
        status = "PASSED" if passed else "FAILED"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")

if __name__ == "__main__":
    asyncio.run(main())
