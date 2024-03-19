from fastapi import APIRouter, Request, status, HTTPException, Cookie
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from decouple import config

from utilities.oauth2 import get_current_user

index_page = APIRouter(tags=['HOME Page'], include_in_schema=False)
template = Jinja2Templates("routes/templates/")

@index_page.get("/", response_class=HTMLResponse)
async def get_index(request: Request, access_token: str = Cookie(None)):
    konteks = {"request": request, "rohan_title": config("API_TITLE"),
               "is_user": None, "login_user": None, "user_email": None, "user_point": None}
    
    if access_token:
        user = await get_current_user(access_token)
        if user:
            konteks.update({"is_user": True, "login_user": user.get("login_id"),
                        "user_email": user.get("email"), "user_point": user.get("point")})
        else:
            raise HTTPException(status_code=status.HTTP_410_GONE)
    
    return template.TemplateResponse("index.html", context=konteks, status_code=status.HTTP_200_OK)
