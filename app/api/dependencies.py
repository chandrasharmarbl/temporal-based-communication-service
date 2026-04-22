from fastapi import Request, HTTPException
from temporalio.client import Client

async def get_temporal_client(request: Request) -> Client:
    client = getattr(request.app.state, "temporal_client", None)
    if not client:
        raise HTTPException(
            status_code=503,
            detail="Temporal client not initialized. Server may still be starting."
        )
    return client
