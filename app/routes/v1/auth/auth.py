from fastapi import APIRouter, Depends
from fastapi.responses import Response, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from datetime import timedelta
from decouple import config

from utilities.oauth2 import create_access_token, authenticate_user

auth = APIRouter(prefix="/application/api/v1/directory/authentication", tags=["Authentication"])

@auth.post("/tokenizer")
async def auth_endpoint(response: Response, login_form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(username=login_form.username, password=login_form.password)
    if not user:
        return False
    token_expires = timedelta(minutes=int(config("ACCESS_TOKEN_VOID")))
    access_token = await create_access_token(data={"sub": user.login_id}, expires_date=token_expires)
    response.set_cookie(key="application_auth_token", value=access_token, expires=15, path="/")
    response.headers['X-User-Category'] = "Authenticated User"
    return {"application_auth_token": access_token, "type": "Bearer"}


@auth.delete("/tokenizer", response_class=JSONResponse)
def logout_auth(response: Response):
    response.delete_cookie(key="application_auth_token", path="/")
    return {"message": "OK"}