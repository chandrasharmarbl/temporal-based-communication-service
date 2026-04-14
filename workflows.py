from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from activities import send_email, send_sms, send_notification

@workflow.defn
class SendNotificationWorkflow:
    @workflow.run
    async def run(self, email: str, phone: str, subject: str, message: str) -> Dict[str, Any]:
        email_result = workflow.execute_activity(
            send_email,
            args=[email, subject, message],
            start_to_close_timeout=timedelta(seconds=10)
        )
        
        sms_result = workflow.execute_activity(
            send_sms,
            args=[phone, message],
            start_to_close_timeout=timedelta(seconds=10)
        )
        
        await workflow.execute_activity(
            send_notification,
            args=[email, phone, subject, message],
            start_to_close_timeout=timedelta(seconds=10)
        )
        
        return {
            "email_result": await email_result,
            "sms_result": await sms_result,
            "status": "completed"
        }