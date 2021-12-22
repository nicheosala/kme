from typing import Final
from uuid import UUID

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from kme import orm
from kme.configs import TestConfig
from kme.database import models
from kme.model import Error
from kme.routers import enc_keys, dec_keys, status

test_app: Final[FastAPI] = FastAPI(
    debug=TestConfig.DEBUG,
    title="Key Management Entity"
)

test_app.include_router(enc_keys.router)
test_app.include_router(dec_keys.router)
test_app.include_router(status.router)


@test_app.on_event("startup")
async def startup() -> None:
    await models.create_all()
    await orm.Key.objects.create(
        key_id=UUID("bc490419-7d60-487f-adc1-4ddcc177c139"),
        key_material="wHHVxRwDJs3/bXd38GHP3oe4svTuRpZS0yCC7x4Ly+s="
    )

    await orm.Key.objects.create(
        key_id=UUID("0a782fb5-3434-48fe-aa4d-14f41d46cf92"),
        key_material="OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA="
    )


@test_app.on_event("shutdown")
async def shutdown() -> None:
    await models.drop_all()


@test_app.exception_handler(RequestValidationError)
async def request_validation_error_handler(
        _: Request,
        error: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=error.body
    )


@test_app.exception_handler(HTTPException)
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
