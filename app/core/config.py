import os

class Settings:
    TEMPORAL_SERVER_URL: str = os.getenv("TEMPORAL_SERVER_URL", "localhost:7233")
    TEMPORAL_TASK_QUEUE: str = os.getenv("TEMPORAL_TASK_QUEUE", "notification-task-queue")

settings = Settings()
