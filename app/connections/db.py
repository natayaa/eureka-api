from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from decouple import config

"""
    include declarative_dbconn to connect
"""

declarative_dbconn = declarative_base()
UserDatabase = config("MSSQL_USERDB")
WorkDatabase = config("MSSQL_WORK")
GameDatabase = config("MSSQL_GAME")
TradeDatabase = config("MSSQL_TRADE")
MallDatabase = config("MSSQL_MALL")

class DBConfig:
    ServerName = config("MSSQL_SERVERNAME")
    ServerUser = config("MSSQL_USERNAME")
    ServerPassword = config("MSSQL_PASSWORD")


def DatabaseConnection(dbname: str):
    """
        Options:
            - UserDatabase = RohanUser
            - WorkDatabase = RohanWork
            - GameDatabase = RohanGame
            - MallDatabase = RohanMall
            - TradeDatabase = RohanTrade
    """
    dbconn = DBConfig()
    str_conn = f"mssql+pyodbc://{dbconn.ServerUser}:{dbconn.ServerPassword}@{dbconn.ServerName}/{dbname}?driver=ODBC+Driver+17+for+SQL+Server"
    database_engine = create_engine(str_conn)
    SessionLocal = sessionmaker(autoflush=True, bind=database_engine, autocommit=False)
    return SessionLocal()