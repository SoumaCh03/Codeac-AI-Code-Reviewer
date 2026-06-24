import hmac
import hashlib
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db

router = APIRouter()

def verify_signature(payload_body: bytes, secret_token: str, signature_header: str):
    """Verify that the payload was sent from GitHub by validating SHA256."""
    if not signature_header:
        raise HTTPException(status_code=403, detail="x-hub-signature-256 header is missing!")
    hash_object = hmac.new(secret_token.encode("utf-8"), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=403, detail="Request signatures didn't match!")

@router.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    payload_body = await request.body()
    signature = request.headers.get("x-hub-signature-256")
    
    if settings.GITHUB_WEBHOOK_SECRET:
        verify_signature(payload_body, settings.GITHUB_WEBHOOK_SECRET, signature)

    event = request.headers.get("x-github-event")
    payload = await request.json()

    if event == "pull_request":
        action = payload.get("action")
        if action in ["opened", "synchronize", "reopened"]:
            # Trigger celery task
            from app.worker.tasks import process_pull_request
            process_pull_request.delay(payload)
            return {"status": "accepted", "message": "Pull request review queued."}
            
    return {"status": "ignored", "event": event}
