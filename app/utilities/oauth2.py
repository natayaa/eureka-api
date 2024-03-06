from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing_extensions import Annotated, Optional
from decouple import config
import hashlib

from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from fastapi import Depends

from connections.queries.tuserconn import UserConnections

oauth2_schemes = OAuth2PasswordBearer(tokenUrl=config("AUTH_TOKEN_ROUTE"))
user_connection = UserConnections()

async def get_current_user(token: Annotated[str, Depends(oauth2_schemes)]):
    """
        JWT Verification (Use compile token name)
        Use for decoding JWT into separated pieces
    """
    try:
        payload = jwt.decode(token, config("APPLICATION_SECRET_KEY", config("ALGORITHM")))
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or token doesn't exist.")
        
    except JWTError as jwterr:
        print(f"Bearer <unidentified_token>: {jwterr}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sub segmentation header cannot be reached")
    
    user = user_connection.getUser(login_id=username)
    if not user:
        return False
    
    if not jwt.get_unverified_header(token).get("alg") == config("ALGORITHM"):
        print("no alg header")
        return None

    
    # filter what data going to be served
    user_information = {"user_id": user.user_id, "login_id": user.login_id, "grade": user.grade,
                        "point": user.point, "point2": user.point_2, "email": user.email}
    return user_information


def verify_password(input_password, hashed_password):
    password_decode = hashlib.md5(input_password.encode()).hexdigest()
    if password_decode == hashed_password:
        return True
    else:
        return False
    

def authenticate_user(username: str, password: str):
    user = user_connection.getUser(login_id=username)
    if not user:
        return None
    if not verify_password(password, user.login_pw):
        return False
    
    return user

async def create_access_token(data: dict, expires_date: timedelta):
    toEncode = data.copy()
    expires = datetime.utcnow() + expires_date if expires_date else datetime.utcnow() + timedelta(minutes=int(config("ACCESS_TOKEN_VOID")))
    toEncode.update({"exp": expires})
    algorithm = config("ALGORITHM")
    s_key = config("APPLICATION_SECRET_KEY")
    
    encode_jwt = jwt.encode(toEncode, s_key, algorithm)
    return encode_jwt