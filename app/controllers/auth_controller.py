from fastapi import APIRouter

from app.schemas.auth_in import LoginIn
from app.security import sign_jwt
from app.views.auth_out import LoginOut

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=LoginOut)
async def login(post: LoginIn):
    return sign_jwt(customer_id=post.customer_id)