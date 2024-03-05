from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import json


# import routes
from routes.v1.auth.auth import auth
from routes.v1.kiosk import kiosk
from routes.v1.user.user import user


app = FastAPI()

app.include_router(auth)
app.include_router(kiosk)
app.include_router(user)