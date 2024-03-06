from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# import routes
from routes.v1.auth.auth import auth
from routes.v1.kiosk import kiosk
from routes.v1.user.user import user

from routes.v1.index import index_page
from routes.v1.webmall import mall_page

app = FastAPI()

# templates 
app.mount("/static", StaticFiles(directory="routes/templates/static"), name="static")
templates = Jinja2Templates("templates/")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost"],
                   allow_credentials=True, allow_methods=["POST", "GET", "PUT"],
                   allow_headers=["*"])

app.include_router(auth)
app.include_router(kiosk)
app.include_router(user)

app.include_router(index_page)
app.include_router(mall_page)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
        handling 442 Unprocessable Entity
    """
    error_msg = []
    for error in exc.errors():
        error_msg.append({"error_field_at": error['loc'], "message": error['msg']})
    
    return ORJSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder({"issues": error_msg}))



##### HANDLING EXCEPTION OF ENDPOINTS/ROUTES #####
@app.exception_handler(HTTPException)
async def exception_handler_routes(request: Request, exc: HTTPException):
    konteks = {"WWW-Authenticate": "Bearer", "X-Access-Restricted": "", "X-User-Category": ""}

    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        konteks.update({"X-Access-Restricted": f"{exc.status_code} {exc.detail}",
                        "X-User-Category": "Anonymous"})
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, 
                              content={"message": "You're not allowed to access the content, please do authenticate/login."},
                              headers=konteks)
    elif exc.status_code == status.HTTP_400_BAD_REQUEST:
        konteks.update({"X-Access-Restricted": exc.detail})
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                              content={"message": f"An error occured: {exc.detail}"},
                              headers=konteks)
    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        konteks.update({"X-Access-Restricted": "Forbidden Access", "X-User-Category": f"{request.headers.get("X-User-Category")}"})
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": f"{exc.detail}", "location": exc['loc']},
                              headers=konteks)