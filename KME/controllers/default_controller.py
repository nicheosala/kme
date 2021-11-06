from __future__ import annotations

from typing import Final
from urllib.parse import unquote as url_decode
from uuid import uuid4 as get_id

import connexion

from KME.models import Error
from KME.models.key import Key
from KME.models.key_container import KeyContainer  # noqa: E501
from KME.models.key_i_ds import KeyIDs  # noqa: E501
from KME.models.key_request import KeyRequest  # noqa: E501
from KME.models.status import Status  # noqa: E501

DEFAULT_NUMBER: Final[int] = 1


def id_gen() -> str:
    return str(get_id())


def gen(size: int) -> Key:
    # TODO This in an example key!
    return Key(
        key_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        key="OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA="
    )


def get(key_id: str) -> Key:
    # TODO This in an example key!
    return Key(
        key_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        key="OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA="
    )


class KeyNotFoundError(Exception):
    pass


key_size: Final[int] = 64  # TODO
kme_id: Final[str] = id_gen()


def get_key(slave_sae_id: str, number: int = DEFAULT_NUMBER, size: int = None) -> KeyContainer:
    """Get key

    Returns Key container data from the KME to the calling master SAE. Key container data contains one or more keys.
    The calling master SAE may supply Key request data to specify the requirement on Key container data.
    The slave SAE specified by the slave_SAE_ID parameter may subsequently request matching keys from a remote KME
    using key_ID identifiers from the returned Key container.

    :param slave_sae_id: URL-encoded SAE ID of slave SAE.
    :type slave_sae_id: str
    :param number: Number of keys requested, default value is 1
    :type number: int
    :param size: Size of each key in bits, default value is defined as key_size in Status data format
    :type size: int

    :rtype: KeyContainer
    """
    return KeyContainer([gen(size) for _ in range(number)])


def get_key_with_key_i_ds(master_sae_id, key_id) -> tuple[KeyContainer | Error, int]:
    """Get key with key IDs

    Returns Key container from the KME to the calling slave SAE. Key container contains keys matching those previously
    delivered to a remote master SAE based on the Key IDs supplied from the remote master SAE in response to its
    call to Get key. The KME shall reject the request with a 401 HTTP status code if the SAE ID of the requester
    was not an SAE ID supplied to the &#x27;Get key&#x27; method each time it was called resulting in the return
    of any of the Key IDs being requested.

    :param master_sae_id: URL-encoded SAE ID of master SAE.
    :type master_sae_id: str
    :param key_id: single key ID
    :type key_id: 

    :rtype: KeyContainer
    """
    try:
        return KeyContainer([get(key_id)]), 200
    except KeyNotFoundError:
        return Error("One or more keys specified are not found on KME"), 400


def get_status(slave_sae_id: str) -> Status:
    """Get status

    Returns Status from a KME to the calling SAE.
    Status contains information on keys available to be requested by a master SAE for a specified slave SAE.

    :param slave_sae_id: URL-encoded SAE ID of slave SAE.
    :type slave_sae_id: str

    :rtype: Status
    """
    # TODO Why doesn't it throw an error when required fields are None?
    return Status(source_kme_id=kme_id,
                  target_kme_id=None,  # TODO
                  master_sae_id=None,  # TODO
                  slave_sae_id=url_decode(slave_sae_id),
                  key_size=key_size,
                  stored_key_count=None,  # TODO
                  max_key_count=None,  # TODO
                  max_key_per_request=None,  # TODO
                  max_key_size=None,  # TODO
                  min_key_size=None,  # TODO
                  max_sae_id_count=None  # TODO
                  )


def post_key(body, slave_sae_id) -> KeyContainer:
    """Post key

    Returns Key container data from the KME to the calling master SAE. Key container data contains one or more keys.
    The calling master SAE may supply Key request data to specify the requirement on Key container data.
    The slave SAE specified by the slave_SAE_ID parameter may subsequently request matching keys from a remote KME
    using key_ID identifiers from the returned Key container.

    :param body:
    :type body: dict | bytes
    :param slave_sae_id: URL-encoded SAE ID of slave SAE.
    :type slave_sae_id: str

    :rtype: KeyContainer
    """
    if connexion.request.is_json:
        body = KeyRequest.from_dict(connexion.request.get_json())

    # TODO handle body specified parameters

    return get_key(slave_sae_id, body.number or DEFAULT_NUMBER, body.size or key_size)


def post_key_with_key_i_ds(body, master_sae_id):
    """Post key with key IDs

    Returns Key container from the KME to the calling slave SAE. Key container contains keys matching those previously
    delivered to a remote master SAE based on the Key IDs supplied from the remote master SAE in response to its call
    to Get key. The KME shall reject the request with a 401 HTTP status code if the SAE ID of the requester was not
    an SAE ID supplied to the &#x27;Get key&#x27; method each time it was called resulting in the return of any of the
    Key IDs being requested.

    :param body: 
    :type body: dict | bytes
    :param master_sae_id: URL-encoded SAE ID of master SAE.
    :type master_sae_id: str

    :rtype: KeyContainer
    """
    if connexion.request.is_json:
        body = KeyIDs.from_dict(connexion.request.get_json())

    try:
        return KeyContainer([get(k.key_id) for k in body.key_i_ds]), 200
    except KeyNotFoundError:
        return Error("One or more keys specified are not found on KME"), 400
