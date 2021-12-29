"""Main app."""
from typing import Final

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse

from kme.configs import Config
from kme.database.database import models
from kme.model.errors import Error, BadRequest, \
    ServiceUnavailable, Unauthorized
from kme.routers import enc_keys, dec_keys, status

app: Final[FastAPI] = FastAPI(
    debug=Config.DEBUG,
    title="Key Management Entity",
    responses={
        400: {"model": BadRequest},
        401: {"model": Unauthorized},
        503: {"model": ServiceUnavailable}
    }
)

app.include_router(enc_keys.router, prefix=Config.BASE_URL)
app.include_router(dec_keys.router, prefix=Config.BASE_URL)
app.include_router(status.router, prefix=Config.BASE_URL)


@app.get('/', include_in_schema=False)
async def redirect() -> RedirectResponse:
    """Redirect to docs."""
    return RedirectResponse('/docs', 302)


@app.on_event("startup")
async def startup() -> None:
    """Create ORM tables inside the database, if not already present."""
    await models.create_all()


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(
        _: Request,
        error: RequestValidationError
) -> JSONResponse:
    """Always return 400 for a RequestValidationError."""
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(
            Error(
                message=str(error.errors()[0])
            ))
    )


@app.exception_handler(HTTPException)
async def error_handler(
        _: Request,
        exception: HTTPException
) -> JSONResponse:
    """Always return a body of type kme.model.Error for an HTTPException."""
    return JSONResponse(
        status_code=exception.status_code,
        content=jsonable_encoder(
            Error(
                message=exception.detail
            ))
    )
