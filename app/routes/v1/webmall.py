from fastapi import APIRouter, Request, status, Cookie, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from decouple import config

from utilities.oauth2 import get_current_user

mall_page = APIRouter(tags=['Web Mall'])
template = Jinja2Templates("routes/templates")



@mall_page.get("/web-mall", include_in_schema=False)
async def get_webMall(request: Request, access_token: str = Cookie(None)):
    konteks = {"request": request, "avail_user": None, "login_user": None, "user_point": None,
               "rohan_title": config("API_TITLE")}

    if access_token:
        user = await get_current_user(access_token)
        if user:
            konteks.update({"request": request, "avail_user": True, "login_user": user.get("login_id"),
                            "user_point": user.get("point"), "user_email": user.get("email")})
        else:
            raise HTTPException(status_code=status.HTTP_410_GONE)
        
    return template.TemplateResponse("mall.html", context=konteks, status_code=status.HTTP_200_OK)


@mall_page.get("/web-mall/buy", include_in_schema=True)
async def get_detail_item(request: Request):
    #if not request.headers.get("X-Authenticated") == "true":
    #    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
       
    #if not access_token:
    #    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, headers={"X-User-Authenticated": "none"})
    
    #if access_token:
    #    user = await get_current_user(access_token)
    #    if user:
    #        konteks.update({"request": request, "avail_user": True, "login_user": user.get("login_id"),
    #                        "user_point": user.get("point"), "user_email": user.get("email")})
    return template.TemplateResponse(name="buy_modal.html", context={"request": request}, status_code=status.HTTP_200_OK)