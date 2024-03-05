from fastapi import APIRouter, status, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing_extensions import Annotated

from core.model.user.usermodel import UserDetail, RegisterUser, RegisterResponse
from core.model.user.usermodel import UserChangePassword
from connections.queries.tuserconn import UserConnections

from utilities.oauth2 import get_current_user

user = APIRouter(prefix="/application/api/v1/routes/user", tags=['API User'])

@user.get("/detail", response_class=JSONResponse)
def get_user(application_auth_token: str = Depends(get_current_user)):
    konteks = {"user_detail": UserDetail(login_id_user=application_auth_token.get("login_id"),
                      email_user=application_auth_token.get("email"),
                      point_user=application_auth_token.get("point"),
                      point2_user=application_auth_token.get("point2"))}
    return konteks


@user.post("/register/user", response_class=JSONResponse)
def register_user(register: RegisterUser):
    konteks_regist = dict(register)
    reg = UserConnections().register_user(**konteks_regist)
    if not reg:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return {"message": "Register success", "konteks": RegisterResponse(login_id=register.username, email=register.email, default_point=100)}


@user.put("/{user_id}/change_password", response_class=JSONResponse)
def change_password(user_id: int, application_auth_token: Annotated[str, Depends(get_current_user)],
                    change_password_payload: UserChangePassword):
    if user_id != application_auth_token.get("user_id"):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    
    konteks = {"message": None}
    return konteks