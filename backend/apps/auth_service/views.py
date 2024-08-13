from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])

# @router.get("/auth")
# def auth_credentials(
#
# )