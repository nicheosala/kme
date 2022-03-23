"""Manage everything about database."""
import uuid
from typing import Final

from orm import NoMatch

from sdn_controller.database import orm
from sdn_controller.database.orm import Kme, Sae
from sdn_controller.model.errors import KmeNotFound
from sdn_controller.model.new_app import NewAppRequest, NewAppResponse
from kme.model.new_kme import NewKmeRequest, NewKmeResponse


async def add_new_kme(new_kme: NewKmeRequest) -> NewKmeResponse:
    """Adds a new KME."""
    kme = uuid.uuid4()
    await orm.Kme.objects.create(kme_id=kme, ip=new_kme.ip, port=new_kme.port)
    return NewKmeResponse(kme_id=kme)


async def add_new_app(new_app: NewAppRequest) -> NewAppResponse:
    """Adds a SAE which wants to start a connection.
    If the other SAE is already registered, creates the ksid."""

    try:
        kme_src: Final[Kme] = await orm.Kme.objects.get(kme_id=new_app.kme)
    except NoMatch:
        raise KmeNotFound()
    src, created = await orm.Sae.objects.get_or_create(
        sae_id=new_app.src,
        defaults={"sae_id": new_app.src, "kme": kme_src}
    )
    try:
        dst: Final[Sae] = await orm.Sae.objects.get(sae_id=new_app.dst)
    except NoMatch:
        return NewAppResponse(sae1=new_app.src, sae2=new_app.dst)
    try:
        kme_dst: Final[Kme] = await orm.Kme.objects.get(id=dst.kme)
        ksid = uuid.uuid4()
        await orm.Ksid.objects.create(
            key_stream_id=ksid,
            sae1=dst,
            sae2=src,
            kme1=kme_dst,
            kme2=kme_src,
            qos=new_app.qos
        )
    except NoMatch:
        raise KmeNotFound()

    return NewAppResponse(key_stream_id=ksid, sae1=new_app.src, sae2=new_app.dst)


async def get_kme_address(sae_uuid: uuid.UUID) -> str:
    """Gets the address of the KME referred to a SAE."""
    try:
        sae: Final[Sae] = await orm.Sae.objects.get(sae_id=sae_uuid)
        kme: Final[Kme] = await orm.Kme.objects.get(id=sae.kme)
    except NoMatch:
        raise KmeNotFound()
    return f"http://{kme.ip}:{kme.port}"
