from fastapi import APIRouter, Depends
from fastapi.responses import Response, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from datetime import timedelta
from decouple import config

from utilities.oauth2 import create_access_token, authenticate_user, create_refresh_token, get_current_user
from connections.queries.tuserconn import UserConnections

auth = APIRouter(prefix="/application/api/v1/directory/authentication", tags=["Authentication"])
web_auth = UserConnections()

token_expires = timedelta(minutes=int(config("ACCESS_TOKEN_VOID")))
refrehs_token_expires = timedelta(minutes=int(config("REFRESH_TOKEN_VOID")))

@auth.post("/tokenizer")
async def auth_endpoint(response: Response, login_form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(username=login_form.username, password=login_form.password)
    if not user:
        return False
    
    access_token = await create_access_token(data={"sub": user.login_id}, expires_date=token_expires)
    refresh_token = await create_refresh_token(data={"sub": user.login_id}, expires_date=refrehs_token_expires)
    
    response.set_cookie(key="access_token", value=access_token, path="/", expires=str(config("ACCESS_TOKEN_VOID")), httponly=False, secure=False, samesite="lax")
    # set table with access
    web_auth.web_cache_access(user_id=user.user_id, login_id=user.login_id,
                              refresh_token=refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token, "type": "Bearer"}


@auth.post("/refresh-token")
async def refresh_token(token: str):
    refresh_data = await get_current_user(token)
    if refresh_data:
        renewed_access_token = await create_access_token(refresh_data, token_expires)

    return {"access_token": renewed_access_token, "type": "Bearer", "status": 200}


@auth.delete("/tokenizer", response_class=JSONResponse)
def logout_auth(response: Response):
    response.delete_cookie(key="access_token", path="/")
    return {"message": "OK"}