from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from connections.db import declarative_dbconn

class TItemMall(declarative_dbconn):
    __tablename__ = "TMallItems"

    mall_id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, nullable=False)
    item_price = Column(Integer, nullable=False)
    item_name = Column(Integer, nullable=False)
    item_quantity = Column(Integer, nullable=False)
    item_stock = Column(Integer)
    item_desc = Column(String)
    item_image = Column(String)
    item_category = Column(String)
    limited_item = Column(Boolean)
    binded = Column(Boolean)
    date_expired_item = Column(DateTime)
    date_added = Column(DateTime, default=datetime.now())
    admin_id = Column(Integer, nullable=False)

class ItemMallBuyHistory(declarative_dbconn):
    __tablename__ = "TItemBuyLog"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer)
    item_id = Column(Integer, ForeignKey("TMallItems.item_id"))
    qty = Column(Integer)
    date = Column(DateTime, default=datetime.now())
    total_points = Column(Integer)