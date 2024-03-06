from fastapi import APIRouter, Depends, status, HTTPException, Query, Cookie, Request
from fastapi.responses import JSONResponse, Response, ORJSONResponse
from typing_extensions import Annotated
from datetime import datetime

from connections.queries.tmallconn import KioskMall, ProceedBuyItem
from connections.queries.tuserconn import UserConnections
# import model
from core.model.kiosk.kiosk_model import Kiosk, KioskDetail, KioskResponse
from utilities.oauth2 import get_current_user

kiosk = APIRouter(prefix="/application/api/v1/routes/kiosk", tags=['Kiosk'])
kiosk_conn = KioskMall()
buy_kiosk_item = ProceedBuyItem()

@kiosk.get("/item_malls", response_class=ORJSONResponse, response_model=KioskResponse)
async def get_kiosk(response: Response,
              search: str = Query(None, alias="search"), 
              offset: int = Query(1, alias="page"),
              limit: int = Query(10, alias="perpage"),
              application_auth_token: str = Cookie(None)):

    kiosk_items = await kiosk_conn.getMall(search, limit, offset)
    showed_kiosk_detail = [Kiosk(mall_id=item.mall_id, 
                                 kiosk_detail=
                                     KioskDetail(
                                         item_id=item.item_id,item_name=item.item_name,
                                         item_stock=item.item_stock,
                                         item_image=item.item_image, 
                                         limited_item=item.limited_item,
                                         item_desc=item.item_desc, 
                                         item_price=item.item_price,
                                         item_category=item.item_category, 
                                         date_expired_item=item.date_expired_item.strftime('%d %B %Y, %H:%M:%S')))
                            for item in kiosk_items]

    konteks = {"status": status.HTTP_200_OK,
               "total_records": kiosk_conn.total_items_in_kiosk, 
               "kiosk_items": showed_kiosk_detail}

    
    return konteks


@kiosk.post("/buy")
async def buy_item_from_kiosk(request: Request, mall_id: int, 
                              application_auth_token: Annotated[str, Depends(get_current_user)]):
    if not application_auth_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    if not mall_id:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    
    if not request.headers.get("x_user_access_level") != "Anonymous":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, headers={"x_message": "You're not logged in, please login to buy the item"})
    
    buy_item = await buy_kiosk_item.buy_kiosk_item(mall_id=mall_id, user_id=application_auth_token.get('user_id'), qty_item_buy=34)
    
    konteks = {"status": None, "message": buy_item.get("status")}
    return konteks