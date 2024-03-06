from fastapi import APIRouter, status, Request


srv_info = APIRouter(prefix="/application/api/v1/routes/information", tags=["Server Information"])

@srv_info.get("/server")
def get_server_information():
    konteks = {"rates": ""}
    return konteks