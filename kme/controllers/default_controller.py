from typing import Final
from urllib.parse import unquote as url_decode
from uuid import uuid4 as get_id

from ..models.error import Error
from ..models.key import Key
from ..models.key_container import KeyContainer
from ..models.key_i_ds import KeyIDs
from ..models.key_request import KeyRequest
from ..models.status import Status


def id_gen() -> str:
    return str(get_id())


default_number: Final[int] = 1
default_key_size: Final[int] = 64  # TODO
kme_id: Final[str] = id_gen()


def gen(size: int) -> Key:
    # TODO This in an example key!
    return Key(
        key_ID="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        key="OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA="
    )


def get(key_id: str) -> Key:
    # TODO This in an example key!
    return Key(
        key_ID="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        key="OeGMPxh1+2RpJpNCYixWHFLYRubpOKCw94FcCI7VdJA="
    )


class KeyNotFoundError(Exception):
    pass


def get_key(slave_sae_id: str, number: int, size: int) -> KeyContainer:
    """Get key

    Returns Key container data from the kme to the calling master SAE. Key container data contains one or more keys.
    The calling master SAE may supply Key request data to specify the requirement on Key container data.
    The slave SAE specified by the slave_SAE_ID parameter may subsequently request matching keys from a remote kme
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


def get_key_with_key_i_ds(master_sae_id, key_id) -> KeyContainer | tuple[Error, int]:
    """Get key with key IDs

    Returns Key container from the kme to the calling slave SAE. Key container contains keys matching those previously
    delivered to a remote master SAE based on the Key IDs supplied from the remote master SAE in response to its
    call to Get key. The kme shall reject the request with a 401 HTTP status code if the SAE ID of the requester
    was not an SAE ID supplied to the &#x27;Get key&#x27; method each time it was called resulting in the return
    of any of the Key IDs being requested.

    :param master_sae_id: URL-encoded SAE ID of master SAE.
    :type master_sae_id: str
    :param key_id: single key ID
    :type key_id: 

    :rtype: KeyContainer
    """
    try:
        return KeyContainer([get(key_id)])
    except KeyNotFoundError:
        return Error("One or more keys specified are not found on kme"), 400


def get_status(slave_sae_id: str) -> Status | tuple[Error | int]:
    """Get status

    Returns Status from a kme to the calling SAE.
    Status contains information on keys available to be requested by a master SAE for a specified slave SAE.

    :param slave_sae_id: URL-encoded SAE ID of slave SAE.
    :type slave_sae_id: str

    :rtype: Status
    """
    return Status(
        source_KME_ID=kme_id,
        target_KME_ID="TODO",
        master_SAE_ID="TODO",
        slave_SAE_ID=url_decode(slave_sae_id),
        key_size=default_key_size,
        stored_key_count=-1,
        max_key_count=-1,
        max_key_per_request=-1,
        max_key_size=-1,
        min_key_size=-1,
        max_SAE_ID_count=-1
    )


def post_key(body, slave_sae_id) -> KeyContainer | tuple[Error, int]:
    """Post key

    Returns Key container data from the kme to the calling master SAE. Key container data contains one or more keys.
    The calling master SAE may supply Key request data to specify the requirement on Key container data.
    The slave SAE specified by the slave_SAE_ID parameter may subsequently request matching keys from a remote kme
    using key_ID identifiers from the returned Key container.

    :param body:
    :type body: dict | bytes
    :param slave_sae_id: URL-encoded SAE ID of slave SAE.
    :type slave_sae_id: str

    :rtype: KeyContainer
    """
    key_request: Final[KeyRequest] = KeyRequest.from_dict(body)

    # TODO handle body specified parameters
    if key_request.extension_mandatory:
        return Error("Field 'extension_mandatory' is not empty and the server shall handle it, but it is not able to "
                     "do it."), 503

    return get_key(slave_sae_id, key_request.number, key_request.size)


def post_key_with_key_i_ds(body, master_sae_id) -> KeyContainer | tuple[Error, int]:
    """Post key with key IDs

    Returns Key container from the kme to the calling slave SAE. Key container contains keys matching those previously
    delivered to a remote master SAE based on the Key IDs supplied from the remote master SAE in response to its call
    to Get key. The kme shall reject the request with a 401 HTTP status code if the SAE ID of the requester was not
    an SAE ID supplied to the &#x27;Get key&#x27; method each time it was called resulting in the return of any of the
    Key IDs being requested.

    :param body: 
    :type body: dict | bytes
    :param master_sae_id: URL-encoded SAE ID of master SAE.
    :type master_sae_id: str

    :rtype: KeyContainer
    """
    key_ids: Final[KeyIDs] = KeyIDs.from_dict(body)

    try:
        return KeyContainer([get(k.key_ID) for k in key_ids.key_IDs])
    except KeyNotFoundError:
        return Error("One or more keys specified are not found on kme"), 400