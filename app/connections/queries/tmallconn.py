from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import or_, func

from connections.db import DatabaseConnection, MallDatabase, UserDatabase # call the session and database attribute from db file
from connections.objects.titemmall import TItemMall, ItemMallBuyHistory # import the object of item mall
from connections.objects.tbusers import TUser

class KioskMall:
    def __init__(self):
        """
            total_items_in_kiosk  # to count items on selected table, in this case
            TMallItems
        """
        self.session = DatabaseConnection(MallDatabase)
        self.session_user = DatabaseConnection(UserDatabase)
        self.total_items_in_kiosk = None

    @staticmethod
    def count_total_items(session):
        try:
            total_items = session.query(func.count(TItemMall.mall_id)).scalar()
            return total_items
        finally:
            # Close the session to release resources
            session.close()
    
    def update_total_item(self):
        self.total_items_in_kiosk = self.count_total_items(self.session)

    async def getMall(self, search: str = None, limit=int, offset=int):
        """
            Return dictionary contain:
            - items
            - total_records
        """
        try:
            items = self.session.query(TItemMall).order_by(TItemMall.mall_id)

            if search:
                search = f"%{search}%"
                items = items.filter(or_(
                    TItemMall.item_category.ilike(search),
                    TItemMall.item_name.ilike(search),
                    TItemMall.item_price.ilike(search)
                ))
            
            self.update_total_item() # count records and update selected attribute
            return items.limit(limit).offset(offset).all()
        except IntegrityError as ie:
            return None

    async def add_kiosk_items(self, items: list):
        try:
            items_to_insert = []
            for params in items:
                item = TItemMall(
                    item_id = params.item_id,
                    item_name = params.item_name,
                    item_quantity = params.item_quantity,
                    item_price = params.item_price,
                    item_image = params.item_image,
                    item_stock = params.item_stock,
                    item_desc = params.item_desc,
                    item_category = params.item_category,
                    binded = params.is_binded,
                    date_expired_item = params.kiosk_limited_date
                )
                items_to_insert.append(item)
            
            self.session._bulk_save_mappings(items_to_insert)
            self.session.commit()
            return True
        except IntegrityError as ie:
            print(ie)
            self.session.rollback()
            return False
        
    async def delete_item_from_kiosk(self, mall_id: int) -> bool:
        query = self.session.query(TItemMall).filter_by(mall_id=mall_id).first()
        if query:
            self.session.delete(query)
            self.session.commit()
            return True
        else:
            return False

    
class ProceedBuyItem(KioskMall):
    def update_user_point(self, user_id: int, reduce_point: int) -> bool:
        try:
            user = self.session_user.query(TUser).filter_by(user_id=user_id).first()
            if user:
                if reduce_point <= user.point:
                    user.point -= reduce_point
                    self.session_user.commit()
                    return True
                else:
                    return False
            else:
                return False
        except SQLAlchemyError as e:
            print(f"Error updating user points: {str(e)}")
            self.session_user.rollback()
            return False

    def update_stock_kiosk(self, mall_id: int, reduce_stock: int) -> bool:
        try:
            query = self.session.query(TItemMall).filter_by(mall_id=mall_id).first()
            if query:
                if reduce_stock <= query.item_stock:
                    query.item_stock -= reduce_stock
                    self.session.commit()
                    return True
                else:
                    return False
            else:
                print(f"No item found in kiosk with mall_id {mall_id}")
                return False
        except SQLAlchemyError as e:
            print(f"Error updating kiosk stock: {str(e)}")
            self.session.rollback()
            return False

    async def buy_kiosk_item(self, mall_id: int, user_id: int, qty_item_buy: int) -> dict:
        """
            parameters for the return values
            - availiable status : 
             - "invalid_point"
             - "usr_not_found"
             - "insufficient_point"
             - "bought_item"
             - "no_item_found"
        """
        konteks = {"message_point": None, "message_user": None, "status": None,
                   "message_item_found": None}
        try:
            query = self.session.query(TItemMall).filter_by(mall_id=mall_id).first()
            if query:
                total_points = query.item_price * qty_item_buy
                if total_points <= 0:
                    print("Invalid total points.")
                    konteks.update({"message_point": "Your point is insufficient to buy selected item with your point ammount.",
                                    "status": "invalid_point"})
                    return konteks
                
                user = self.session_user.query(TUser).filter_by(user_id=user_id).first()
                if not user:
                    konteks.update({"message_user": "User not found", "status": "usr_not_found"})
                    return konteks

                if user.point < total_points:
                    konteks.update({"message_lack_point": "Insufficient point of your account to buy the item",
                                    "status": "insufficient_point"})
                    return konteks

                reduce_point = self.update_user_point(user_id=user_id, reduce_point=total_points)
                reduce_item_qty = self.update_stock_kiosk(mall_id=mall_id, reduce_stock=qty_item_buy)

                if reduce_point and reduce_item_qty:
                    history_buy = ItemMallBuyHistory(
                        user_id=user_id,
                        item_id=query.item_id,
                        qty=query.item_quantity,
                        total_points=total_points
                    )
                    self.session.add(history_buy)
                    self.session.commit()
                    konteks.update({"message": "Accepted", "status": True})
                    return konteks
            else:
                konteks.update({"message_item_found": "No item found in the kiosk",
                                "status": "no_item_found"})
                return konteks
        except SQLAlchemyError as e:
            print(f"Error buying kiosk item: {str(e)}")
            self.session.rollback()
            return False