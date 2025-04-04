from fastapi import APIRouter

from utils import EmailClient

router = APIRouter(
    prefix="/emails",
    tags=["Emails"],
)


@router.get("/")
async def get_email():
    async with EmailClient() as email_client:
        return {"email_address": email_client.email_address}


@router.get("/messages")
async def get_email_messages(email_address: str):
    async with EmailClient(email_address=email_address) as email_client:
        await email_client.get_token()
        messages = await email_client.get_emails()
        return {"email_messages": messages}
