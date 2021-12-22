from typing import Final, Iterator
from urllib.parse import unquote as url_decode
from uuid import UUID

from fastapi import FastAPI, Query, Path, Depends, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from kme.configs import Config
from kme.errors import UnsupportedMandatoryExtensionParameterError, \
    SizeNotMultipleOfEightError
from kme.model import Error
from kme.model import KeyContainer, Key, Status, KeyRequest, KeyIDs, \
    KeyIDsKeyIDs
from kme.database import Base, engine, SessionLocal


def create_app() -> FastAPI:
    Base.metadata.create_all(engine)

    def get_db() -> Iterator[Session]:
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    app: Final[FastAPI] = FastAPI(
        debug=Config.DEBUG,
        title="Key Management Entity"
    )

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

    @app.get(
        path="/api/v1/keys/{slave_SAE_ID}/enc_keys",
        summary="Get key",
        response_model=KeyContainer
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
            session: Session = Depends(get_db)
    ) -> KeyContainer:
        """
        Returns Key container data from the kme to the calling master SAE. The
        calling master SAE may supply Key request data to specify the
        requirement on Key container data. The slave SAE specified by the
        slave_SAE_ID parameter may subsequently request matching keys from a
        remote kme using key_ID identifiers from the returned Key container.
        """
        new_keys: Final[tuple[Key, ...]] = tuple(Key.generate(
            session,
            size,
            frozenset((url_decode(slave_SAE_ID))),
        ) for _ in range(number))

        return KeyContainer(keys=new_keys)

    @app.get(
        path="/api/v1/keys/{master_SAE_ID}/dec_keys",
        summary="Get key with key IDs",
        response_model=KeyContainer
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
            session: Session = Depends(get_db)
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
        keys: Final[tuple[Key, ...]] = Key.get(
            session,
            key_ID,
            url_decode(master_SAE_ID)
        ),

        return KeyContainer(keys=keys)

    @app.get(
        path="/api/v1/keys/{slave_SAE_ID}/status",
        summary="Get status",
        response_model=Status
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
        response_model=KeyContainer
    )
    async def post_key(
            key_request: KeyRequest,
            slave_SAE_ID: str = Path(
                ...,
                description="URL-encoded SAE ID of slave SAE"
            ),
            session: Session = Depends(get_db)
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
                    raise UnsupportedMandatoryExtensionParameterError

        if key_request.size % 8 != 0:
            raise SizeNotMultipleOfEightError

        new_keys: Final[tuple[Key, ...]] = tuple(Key.generate(
            session,
            key_request.size,
            frozenset((url_decode(slave_SAE_ID),
                       *key_request.additional_slave_SAE_IDs)),
            *key_request.extension_mandatory,
            *key_request.extension_optional
        ) for _ in range(key_request.number))

        return KeyContainer(keys=new_keys)

    @app.post(
        path="/api/v1/keys/{master_SAE_ID}/dec_keys",
        summary="Post key with key IDs",
        response_model=KeyContainer
    )
    async def post_key_with_key_i_ds(
            key_ids: KeyIDs,
            master_SAE_ID: str = Path(
                ...,
                description="URL-encoded SAE ID of master SAE"
            ),
            session: Session = Depends(get_db)
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
        ids: Final[tuple[KeyIDsKeyIDs, ...]] = key_ids.key_IDs
        keys: Final[tuple[Key, ...]] = tuple(Key.get(
            session,
            k.key_ID,
            url_decode(master_SAE_ID)
        ) for k in ids)

        return KeyContainer(keys=keys)

    return app
