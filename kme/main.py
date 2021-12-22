from typing import Final
from urllib.parse import unquote as url_decode
from uuid import UUID

from fastapi import FastAPI, Query, Path, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse

from kme import orm
from kme.configs import Config
from kme.database import models
from kme.errors import UnsupportedExtensionError, SizeNotMultipleOfEightError
from kme.model import Error
from kme.model import KeyContainer, Key, Status, KeyRequest, KeyIDs

app: Final[FastAPI] = FastAPI(
    debug=Config.DEBUG,
    title="Key Management Entity"
)


@app.on_event("startup")
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


@app.on_event("shutdown")
async def shutdown() -> None:
    await models.drop_all()


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


@app.get('/')
async def redirect() -> RedirectResponse:
    return RedirectResponse('/docs', 302)


@app.get(
    path="/api/v1/keys/{slave_SAE_ID}/enc_keys",
    summary="Get key",
    response_model=KeyContainer,
    response_model_exclude_unset=True
)
async def get_key(
        slave_SAE_ID: str,
        number: int = Query(
            default=1,
            description="Number of keys requested",
            ge=1
        ),
        size: int = Query(
            default=64,
            description="Size of each key in bits",
            ge=1
        ),
) -> KeyContainer:
    """
    Returns Key container data from the kme to the calling master SAE. The
    calling master SAE may supply Key request data to specify the
    requirement on Key container data. The slave SAE specified by the
    slave_SAE_ID parameter may subsequently request matching keys from a
    remote kme using key_ID identifiers from the returned Key container.
    """
    new_keys: Final[list[Key]] = []
    for _ in range(number):
        new_key: Key = await Key.generate(
            size,
            frozenset([url_decode(slave_SAE_ID)])
        )
        new_keys.append(new_key)

    return KeyContainer(keys=tuple(new_keys))


@app.get(
    path="/api/v1/keys/{master_SAE_ID}/dec_keys",
    summary="Get key with key IDs",
    response_model=KeyContainer,
    response_model_exclude_unset=True
)
async def get_key_with_key_i_ds(
        master_SAE_ID: str = Path(
            ...,
            description="URL-encoded SAE ID of master SAE"
        ),
        key_ID: UUID = Query(
            ...,
            description="single key ID"
        ),
) -> KeyContainer:
    """
    Returns Key container from the kme to the calling slave SAE. Key
    container contains keys matching those previously delivered to a
    remote master SAE based on the Key IDs supplied from the remote
    master SAE in response to its call to Get key. The kme shall reject
    the request with a 401 HTTP status code if the SAE ID of the
    requester was not an SAE ID supplied to the 'Get key' method each
    time it was called resulting in the return of the Key IDs being
    requested.
    """
    keys: Final[tuple[Key, ...]] = await Key.get(
        key_ID,
        url_decode(master_SAE_ID)
    ),

    return KeyContainer(keys=keys)


@app.get(
    path="/api/v1/keys/{slave_SAE_ID}/status",
    summary="Get status",
    response_model=Status,
    response_model_exclude_unset=True
)
async def get_status(
        slave_SAE_ID: str = Path(
            ...,
            description="URL-encoded SAE ID of slave SAE"
        )
) -> Status:
    """
    Returns Status from a kme to the calling SAE
    """
    return Status(
        source_KME_ID="TODO",
        target_KME_ID="TODO",
        master_SAE_ID="TODO",
        slave_SAE_ID=url_decode(slave_SAE_ID),
        key_size=64,
        stored_key_count=-1,
        max_key_count=-1,
        max_key_per_request=-1,
        max_key_size=-1,
        min_key_size=-1,
        max_SAE_ID_count=-1
    )


@app.post(
    path="/api/v1/keys/{slave_SAE_ID}/enc_keys",
    summary="Post key",
    response_model=KeyContainer,
    response_model_exclude_unset=True
)
async def post_key(
        key_request: KeyRequest,
        slave_SAE_ID: str = Path(
            ...,
            description="URL-encoded SAE ID of slave SAE"
        ),
) -> KeyContainer:
    """
    Returns Key container data from the kme to the calling master SAE. Key
    container data contains one or more keys. The calling master SAE may
    supply Key request data to specify the requirement on Key container
    data. The slave SAE specified by the slave_SAE_ID parameter may
    subsequently request matching keys from a remote kme using key_ID
    identifiers from the returned Key container.
    """
    for ext in key_request.extension_mandatory:
        for ext_name in ext.keys():
            if ext_name not in key_request.supported_extension_parameters:
                raise UnsupportedExtensionError

    if key_request.size % 8 != 0:
        raise SizeNotMultipleOfEightError

    new_keys: Final[list[Key]] = []
    for _ in range(key_request.number):
        new_key: Key = await Key.generate(
            key_request.size,
            frozenset((url_decode(slave_SAE_ID),
                       *key_request.additional_slave_SAE_IDs)),
            *key_request.extension_mandatory,
            *key_request.extension_optional
        )

        new_keys.append(new_key)

    return KeyContainer(keys=tuple(new_keys))


@app.post(
    path="/api/v1/keys/{master_SAE_ID}/dec_keys",
    summary="Post key with key IDs",
    response_model=KeyContainer,
    response_model_exclude_unset=True
)
async def post_key_with_key_i_ds(
        key_ids: KeyIDs,
        master_SAE_ID: str = Path(
            ...,
            description="URL-encoded SAE ID of master SAE"
        ),
) -> KeyContainer:
    """
    Returns Key container from the kme to the calling slave SAE. Key
    container contains keys matching those previously delivered to a
    remote master SAE based on the Key IDs supplied from the remote
    master SAE in response to its call to Get key. The kme shall reject
    the request with a 401 HTTP status code if the SAE ID of the
    requester was not an SAE ID supplied to the 'Get key' method each
    time it was called resulting in the return of the Key IDs being
    requested.
    """
    keys: Final[list[Key]] = []
    for key_id in key_ids.key_IDs:
        key: Key = await Key.get(
            key_id.key_ID,
            url_decode(master_SAE_ID)
        )
        keys.append(key)

    return KeyContainer(keys=tuple(keys))
