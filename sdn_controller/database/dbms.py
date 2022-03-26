"""Manage everything about database of the SDN Controller."""
import logging
import uuid
from typing import Final

from orm import NoMatch

from sdn_controller.database import orm
from sdn_controller.model.new_app import NewAppRequest, RegisterApp, WaitingForApp
from sd_qkd_node.model.new_kme import NewKmeRequest, NewKmeResponse
from sdn_controller.utils import Bcolors


async def add_new_kme(new_kme: NewKmeRequest) -> NewKmeResponse:
    """Adds a new KME assigning a new UUID."""
    kme = await orm.Kme.objects.create(ip=new_kme.ip, port=new_kme.port)
    logging.getLogger("sdn_controller").info(
        f"\n{Bcolors.OKGREEN}KME added:{Bcolors.ENDC} {Bcolors.BOLD}{kme.kme_id}{Bcolors.ENDC}\n"
    )
    return NewKmeResponse(kme_id=kme.kme_id)


async def find_peer(new_app: NewAppRequest) -> RegisterApp | WaitingForApp:
    """Creates the KSID for a connection."""
    try:
        ksid = await orm.Ksid.objects.get(
            src=new_app.src, dst=new_app.dst, qos=new_app.qos
        )
        logging.getLogger("sdn_controller").info(
            f"\n{Bcolors.OKGREEN}Connection added:{Bcolors.ENDC}\n"
            f"\tASSIGNED KSID: {Bcolors.BOLD}{ksid.ksid}{Bcolors.ENDC}\n"
            f"\tSAE src: {ksid.src}\n"
            f"\tSAE dst: {ksid.dst}\n"
            f"\tKME src: {ksid.kme_src or new_app.kme}\n"
            f"\tKME dst: {ksid.kme_dst or new_app.kme}\n"
            f"\tQoS: {ksid.qos}\n"
        )
        if new_app.src_flag:
            await ksid.update(kme_src=new_app.kme)
            return RegisterApp(
                ksid=ksid.ksid, src=new_app.src, dst=ksid.dst, kme_src=new_app.kme, kme_dst=ksid.kme_dst, qos=ksid.qos
            )
        else:
            await ksid.update(kme_dst=new_app.kme)
            return RegisterApp(
                ksid=ksid.ksid, src=new_app.src, dst=ksid.dst, kme_src=ksid.kme_src, kme_dst=new_app.kme, qos=ksid.qos
            )

    except NoMatch:
        logging.getLogger("sdn_controller").info(
            f"\n{Bcolors.OKBLUE}Connection required:{Bcolors.ENDC}\n"
            f"\tSAE src: {new_app.src}\n"
            f"\tSAE dst: {new_app.dst}\n"
            f"\tQoS: {new_app.qos}\n"
        )
        if new_app.src_flag:
            await orm.Ksid.objects.create(src=new_app.src, dst=new_app.dst, qos=new_app.qos, kme_src=new_app.kme)
        else:
            await orm.Ksid.objects.create(src=new_app.src, dst=new_app.dst, qos=new_app.qos, kme_dst=new_app.kme)
        return WaitingForApp()


async def get_kme_address(kme_uuid: uuid.UUID) -> str:
    """Gets the address of the KME referred to a SAE."""
    kme: Final[orm.Kme] = await orm.Kme.objects.get(kme_id=kme_uuid)
    return f"http://{kme.ip}:{kme.port}"
