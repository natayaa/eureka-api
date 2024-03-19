from sqlalchemy import Column, String, Integer, DateTime, BINARY, ForeignKey
from sqlalchemy.orm import relationship
from connections.db import declarative_dbconn
from datetime import datetime

class TUser(declarative_dbconn):
    __tablename__ = "TUser"

    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    login_id = Column(String, nullable=False)
    login_pw = Column(String, nullable=False)
    grade = Column(Integer, default=10)
    session_id = Column(String(length=36), default=0)
    session_date = Column(DateTime, default=datetime.now())
    species = Column(Integer, default=0)
    bill_no = Column(Integer, default=0)
    server_id = Column(Integer, default=0)
    optionkey_version = Column(BINARY, default=0)
    optionkey_info = Column(BINARY, default=0)
    point = Column(Integer, default=100)
    login_pw2 = Column(Integer)
    point_2 = Column(Integer, default=0)
    email = Column(String)


class TWebAdmin(declarative_dbconn):
    __tablename__ = "TWebAdmin"

    no = Column(Integer, primary_key=True, autoincrement=True)
    web_id = Column(String(length=20))
    web_pw = Column(String)
    level = Column(Integer)

    #web_admin = relationship("TItemMall", back_populates="web_user")

class TUserLogon(declarative_dbconn):
    __tablename__ = "TUserLogon"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    login_id = Column(String)
    refresh_token = Column(String)
    date_login = Column(DateTime, default=datetime.now())