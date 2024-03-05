from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from hashlib import md5

# import relay connection engine
from connections.db import DatabaseConnection, UserDatabase
# import table object
from connections.objects.tbusers import TUser


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