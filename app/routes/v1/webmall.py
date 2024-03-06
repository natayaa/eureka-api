from fastapi import APIRouter, Request, status, Cookie, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from decouple import config

from utilities.oauth2 import get_current_user

mall_page = APIRouter(tags=['Web Mall'], include_in_schema=False)
template = Jinja2Templates("routes/templates")


@mall_page.get("/web-mall")
async def get_webMall(request: Request, application_auth_token: str = Cookie(None)):
    konteks = {"request": request, "is_user": None, "login_user": None, "user_point": None,
               "rohan_title": config("API_TITLE")}

    if application_auth_token:
        user = await get_current_user(application_auth_token)
        if user:
            konteks.update({"is_user": True, "login_user": user.get("login_id"),
                            "user_point": user.get("point"), "user_email": user.get("email")})
        else:
            raise HTTPException(status_code=status.HTTP_410_GONE)
        
    return template.TemplateResponse("mall.html", context=konteks, status_code=status.HTTP_200_OK)