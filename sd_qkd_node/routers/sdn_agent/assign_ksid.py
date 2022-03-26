import logging
from typing import Final

from fastapi import APIRouter

from sd_qkd_node.database.dbms import save_ksid
from sd_qkd_node.database.orm import Ksid
from sd_qkd_node.utils import Bcolors
from sdn_controller.model.new_app import RegisterApp, WaitingForApp

router: Final[APIRouter] = APIRouter(tags=["assign_ksid"])


@router.post(
    path="/assign_ksid",
    include_in_schema=False,
)
async def assign_ksid(
        request: RegisterApp | WaitingForApp
) -> None:
    """
    The SDN Controller calls this API to comunicate the assigned Ksid for a connection between two SAEs.
    """
    if isinstance(request, WaitingForApp):
        logging.getLogger("sd_qkd_node").info(f"{Bcolors.OKBLUE}Waiting the other app for Ksid{Bcolors.ENDC}")
    else:
        ksid: Final[Ksid] = Ksid(
            ksid=request.ksid, src=request.src, dst=request.dst, kme_src=request.kme_src,
            kme_dst=request.kme_dst, qos=request.qos
        )
        await save_ksid(ksid)
