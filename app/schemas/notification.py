from pydantic import BaseModel, EmailStr

class SendNotificationRequest(BaseModel):
    email: EmailStr
    phone_number: str
    subject: str
    message: str

class WorkflowResponse(BaseModel):
    workflow_id: str
    status: str
    message: str
    result: dict | None = None
