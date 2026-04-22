import asyncio
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from .activities import send_email, send_sms, send_notification

# Define a retry policy demonstrating Temporal's built-in durability
# If the activity fails, it will back off exponentially and retry.
default_retry_policy = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(seconds=10),
    maximum_attempts=5,
)

@workflow.defn
class SendNotificationWorkflow:
    @workflow.run
    async def run(self, email: str, phone: str, subject: str, message: str) -> Dict[str, Any]:
        # Execute email and SMS activities concurrently
        # If they fail, Temporal handles the retry based on the policy without 
        # requiring us to write complex retry loops in our code.
        email_task = asyncio.create_task(
            workflow.execute_activity(
                send_email,
                args=[email, subject, message],
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=default_retry_policy
            )
        )
        
        sms_task = asyncio.create_task(
            workflow.execute_activity(
                send_sms,
                args=[phone, message],
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=default_retry_policy
            )
        )
        
        # Wait for both to finish
        email_result, sms_result = await asyncio.gather(email_task, sms_task)
        
        # Once both are done, execute the final notification saving activity
        await workflow.execute_activity(
            send_notification,
            args=[email, phone, subject, message],
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=default_retry_policy
        )
        
        return {
            "email_result": email_result,
            "sms_result": sms_result,
            "status": "completed"
        }
