from typing import Final
from urllib.parse import unquote as url_decode

from kme.errors import UnsupportedMandatoryExtensionParameterError, SizeNotMultipleOfEightError
from kme.model import Key, KeyContainer, KeyIDs, KeyIDsKeyIDs, KeyRequest, Status


# TODO for default value of size: "default value is defined as key_size in Status data format". See also KeyRequest.
def get_key(slave_sae_id: str, number: int = 1, size: int = 64) -> KeyContainer:
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
    new_keys: Final[tuple[Key, ...]] = tuple(Key.generate(
        size,
        frozenset((url_decode(slave_sae_id)))
    ) for _ in range(number))

    return KeyContainer(new_keys)


def get_key_with_key_i_ds(master_sae_id, key_id) -> KeyContainer:
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
    keys: Final[tuple[Key, ...]] = Key.get(key_id, url_decode(master_sae_id)),
    return KeyContainer(keys)


def get_status(slave_sae_id: str) -> Status:
    """Get status

    Returns Status from a kme to the calling SAE.
    Status contains information on keys available to be requested by a master SAE for a specified slave SAE.

    :param slave_sae_id: URL-encoded SAE ID of slave SAE.
    :type slave_sae_id: str

    :rtype: Status
    """
    return Status(
        source_KME_ID="TODO",
        target_KME_ID="TODO",
        master_SAE_ID="TODO",
        slave_SAE_ID=url_decode(slave_sae_id),
        key_size=64,
        stored_key_count=-1,
        max_key_count=-1,
        max_key_per_request=-1,
        max_key_size=-1,
        min_key_size=-1,
        max_SAE_ID_count=-1
    )


def post_key(body, slave_sae_id) -> KeyContainer:
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
    key_request: Final[KeyRequest] = KeyRequest.from_json(body)

    # TODO handle body specified parameters
    if (key_request.extension_mandatory and
            any(ext not in key_request.supported_extension_parameters for ext in key_request.extension_mandatory)):
        raise UnsupportedMandatoryExtensionParameterError

    if key_request.size % 8 != 0:
        raise SizeNotMultipleOfEightError

    new_keys: Final[tuple[Key, ...]] = tuple(Key.generate(
        key_request.size,
        frozenset((url_decode(slave_sae_id), *key_request.additional_slave_SAE_IDs)),
        *key_request.extension_mandatory,
        *key_request.extension_optional
    ) for _ in range(key_request.number))

    return KeyContainer(new_keys)


def post_key_with_key_i_ds(body, master_sae_id) -> KeyContainer:
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
    key_ids: Final[tuple[KeyIDsKeyIDs, ...]] = KeyIDs.from_json(body).key_IDs
    keys: Final[tuple[Key, ...]] = tuple(Key.get(k.key_ID, url_decode(master_sae_id)) for k in key_ids)

    return KeyContainer(keys)
