from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing_extensions import Annotated, Optional
from decouple import config
import hashlib

from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Header
from fastapi import Depends

from connections.queries.tuserconn import UserConnections

oauth2_schemes = OAuth2PasswordBearer(tokenUrl=config("AUTH_TOKEN_ROUTE"))
user_connection = UserConnections()



async def verify_token(token: str):
    credential_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                   detail="Could not validate credentials",
                                   headers={"WWW-Authenticate": "Bearer"})
    try:
        pk_file = ""
        with open("../private_key.pem", "r") as pfile:
            pk_file += pfile.read()

        payload = jwt.decode(token, pk_file, config("ALGORITHM"))
        username: str = payload.get("sub")
        if not username:
            raise credential_exc
        
        expiration = payload.get("exp")
        if expiration:
            now = datetime.now().timestamp()
            if now > expiration:
                new_access_token = await create_access_token(payload)
                return new_access_token
    except JWTError as jtwerr:
        print(jtwerr)
        raise credential_exc
        
    return username


async def get_current_user(token: Annotated[str, Depends(oauth2_schemes)]):
    """
        JWT Verification (Use compile token name)
        Use for decoding JWT into separated pieces
    """
    credential_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                   detail="Could not validate credentials",
                                   headers={"WWW-Authenticate": "Bearer"})
    username = await verify_token(token=token)
    user = user_connection.getUser(login_id=username)
    if not user:
        raise credential_exc
    
    user_information =  {"user_id": user.user_id, "login_id": user.login_id, "grade": user.grade,
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
    expires = datetime.now() + expires_date if expires_date else datetime.now() + timedelta(minutes=int(config("ACCESS_TOKEN_VOID")))
    toEncode.update({"exp": expires})
    algorithm = config("ALGORITHM")
    #s_key = config("APPLICATION_SECRET_KEY")
    privateKey = ""
    with open("../private_key.pem", "r") as pk_file:
        privateKey += pk_file.read()
    
    encode_jwt = jwt.encode(toEncode, privateKey, algorithm)
    return encode_jwt

async def create_refresh_token(data: dict, expires_date: timedelta):
    toEncode = data.copy()
    expires_data = datetime.now() + expires_date if expires_date else datetime.now() + timedelta(minutes=int(config("REFRESH_TOKEN_VOID")))
    toEncode.update({"exp": expires_data})
    algorithm = config("ALGORITHM")
    privatekey_file = ""
    with open("../private_key.pem", 'r') as pk_file:
        privatekey_file += pk_file.read()
    EncodeJwt = jwt.encode(toEncode, privatekey_file, algorithm=algorithm)
    return EncodeJwt