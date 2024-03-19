from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from hashlib import md5

# import relay connection engine
from connections.db import DatabaseConnection, UserDatabase
# import table object
from connections.objects.tbusers import TUser, TUserLogon


class UserConnections:
    def __init__(self):
        self.DBSession = DatabaseConnection(UserDatabase)

    def getUser(self, login_id: str):
        query = self.DBSession.query(TUser).filter_by(login_id=login_id).first()
        return query
    
    def register_user(self, **register):
        try:
            encode_pw = register.get("password").encode("UTF-8")  # decode it into utf after get
            get_user = self.getUser(login_id=register.get("username"))
            if not get_user:
                pass
            user = TUser()
            user.login_id = register.get("username")
            user.login_pw = md5(encode_pw).hexdigest()
            user.login_pw2 = register.get("security_code")
            user.email = register.get("email")

            self.DBSession.add(user)
            self.DBSession.commit()
            return True
        except IntegrityError as ie:
            print(ie)
            self.DBSession.rollback()
            return False
        
    def change_user_password(self, user_id: int, new_password: str) -> bool:
        try:
            query = self.DBSession.query(TUser).filter_by(user_id=user_id).first()
            if query:
                query.login_pw = md5(new_password.encode("utf-8")).hexdigest()
                self.DBSession.commit()
                return True
            else:
                return False
        except IntegrityError as ie:
            self.DBSession.rollback()
            print(ie)
            return False
        
    def web_cache_access(self, user_id, login_id, refresh_token):
        try:
            web_access = TUserLogon()
            web_access.user_id = user_id
            web_access.login_id = login_id
            web_access.refresh_token = refresh_token
            self.DBSession.add(web_access)
            self.DBSession.commit()
            return True
        except IntegrityError as e:
            print(e)
            self.DBSession.rollback()
            return None
        