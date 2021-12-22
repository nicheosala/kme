from typing import Final

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse

from kme.configs import Config
from kme.database import models
from kme.model import Error
from kme.routers import enc_keys, dec_keys, status

app: Final[FastAPI] = FastAPI(
    debug=Config.DEBUG,
    title="Key Management Entity"
)

app.include_router(enc_keys.router)
app.include_router(dec_keys.router)
app.include_router(status.router)


@app.get('/')
async def redirect() -> RedirectResponse:
    return RedirectResponse('/docs', 302)


@app.on_event("startup")
async def startup() -> None:
    await models.create_all()


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(
        _: Request,
        error: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=error.body
    )


@app.exception_handler(HTTPException)
async def error_handler(
        _: Request,
        exception: HTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content=jsonable_encoder(
            Error(
                message=exception.detail
            ))
    )
