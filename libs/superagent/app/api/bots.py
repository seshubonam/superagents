import logging

from fastapi import APIRouter, Depends, HTTPException, status
from decouple import config

from app.utils.admin import check_access_token, get_admin
from prisma.models import ApiUser
from app.utils.prisma import prisma

admin_api_key = config("ADMIN_API_KEY",None)

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post(
    "/bots/{email_id}/api_key",
    name="invoke",
    description="Invoke a specific workflow",
)
async def get_user_api_key(
    email_id: str,
    api_user=Depends(get_admin),
):
    api_user = await prisma.apiuser.find_unique(
        where={"email": email_id}
    )
    if api_user:
        {"success": True, "data" : api_user}
    return True

@router.post(
    "/bots/verify",
    name="Verify user",
    description="Verify and get user's api key",
)
async def get_user_api_key(
    matrix_user=Depends(check_access_token),
):
    try:
        pid_data = matrix_user["threepids"]
        email_id = pid_data[0]["address"]
        api_user = await prisma.apiuser.find_first(
            where={"email": email_id}
        )
        {"success": True, "data" : api_user}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"error: {e}")


