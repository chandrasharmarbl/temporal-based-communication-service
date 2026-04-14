from faker import Faker
from typing import Dict, List, Any
import random

fake = Faker()

class FakerService:
    @staticmethod
    def generate_email() -> str:
        return fake.email()
    
    @staticmethod
    def generate_phone() -> str:
        return fake.phone_number()
    
    @staticmethod
    def generate_subject() -> str:
        subjects = [
            "Welcome to our service!",
            "Your account has been updated",
            "Special offer just for you",
            "Important notification",
            "Your order has been shipped",
            "Password reset request",
            "Confirm your email address",
            "Thank you for your purchase",
        ]
        return random.choice(subjects)
    
    @staticmethod
    def generate_message() -> str:
        messages = [
            fake.paragraph(nb_sentences=3),
            fake.text(max_nb_chars=100),
            "Thank you for being a valued customer!",
            "We have an important update for you.",
            "Your request has been processed successfully.",
            "Please verify your account to continue.",
        ]
        return random.choice(messages)
    
    @staticmethod
    def generate_notification_data() -> Dict[str, str]:
        return {
            "email": FakerService.generate_email(),
            "phone": FakerService.generate_phone(),
            "subject": FakerService.generate_subject(),
            "message": FakerService.generate_message()
        }
    
    @staticmethod
    def generate_batch(count: int = 5) -> List[Dict[str, str]]:
        return [FakerService.generate_notification_data() for _ in range(count)]


if __name__ == "__main__":
    print("Testing Faker Service\n")
    
    print("Single Notification:")
    data = FakerService.generate_notification_data()
    print(f"  Email: {data['email']}")
    print(f"  Phone: {data['phone']}")
    print(f"  Subject: {data['subject']}")
    print(f"  Message: {data['message']}\n")
    
    print("Batch of 3 Notifications:")
    batch = FakerService.generate_batch(3)
    for i, item in enumerate(batch, 1):
        print(f"  {i}. Email: {item['email']}, Phone: {item['phone']}")
