import asyncio
import random
from temporalio import activity
from typing import Dict, Any

@activity.defn
async def send_email(recipient: str, subject: str, body: str) -> Dict[str, Any]:
    await asyncio.sleep(0.5)
    
    # Simulate a flaky external API for durability demonstration
    if random.random() < 0.5:
        print(f"Simulating email failure for {recipient}... Temporal will retry this.")
        raise RuntimeError("Simulated external email API failure")

    result = {
        "status": "sent",
        "recipient": recipient,
        "subject": subject,
        "message_id": f"email_{hash(recipient + subject) % 1000000}",
        "timestamp": asyncio.get_event_loop().time()
    }
    print(f"Email sent successfully to {recipient}: {subject}")
    return result

@activity.defn
async def send_sms(phone_number: str, message: str) -> Dict[str, Any]:
    await asyncio.sleep(0.3)
    result = {
        "status": "sent",
        "phone_number": phone_number,
        "message": message,
        "message_id": f"sms_{hash(phone_number + message) % 1000000}",
        "timestamp": asyncio.get_event_loop().time()
    }
    print(f"SMS sent to {phone_number}: {message}")
    return result

@activity.defn
async def send_notification(email: str, phone: str, subject: str, message: str) -> Dict[str, Any]:
    await asyncio.sleep(0.1)
    result = {
        "status": "sent",
        "email": email,
        "phone": phone,
        "notification_id": f"notif_{hash(email + phone) % 1000000}",
        "timestamp": asyncio.get_event_loop().time()
    }
    print(f"Notification record saved for {email} and {phone}")
    return result
