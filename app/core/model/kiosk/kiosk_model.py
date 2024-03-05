from pydantic import BaseModel
from typing_extensions import Optional, List
from datetime import datetime

class KioskDetail(BaseModel):
    item_id: int
    item_name: str
    item_stock: int
    item_image: str
    limited_item: bool
    item_desc: str 
    item_stock: int
    item_price: int
    item_category: str
    date_expired_item: str
    
class Kiosk(BaseModel):
    mall_id: int
    kiosk_detail: List[KioskDetail]

class KioskResponse(BaseModel):
    status: int
    total_records: int
    kiosk_items: List[Kiosk]