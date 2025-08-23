from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse


from authx.exceptions import MissingTokenError

from apps import api_router

app = FastAPI(openapi_prefix="/api")
app.include_router(api_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(title="AuthX API", version="1.0", description="API with JWT auth", routes=app.routes)
    schema["components"]["securitySchemes"] = {
        "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    schema["security"] = [{"bearerAuth": []}]
    schema["servers"] = [{"url": "/api"}]
    app.openapi_schema = schema
    return schema


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.openapi = custom_openapi

@app.exception_handler(MissingTokenError)
async def missing_token_handler(request: Request, exc: MissingTokenError):
    return JSONResponse(
        status_code=404,
        content={"detail": "not found"}
    )