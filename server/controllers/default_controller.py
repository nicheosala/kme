import connexion
from server.models.key import Key

from server.models.key_container import KeyContainer  # noqa: E501
from server.models.key_i_ds import KeyIDs  # noqa: E501
from server.models.key_request import KeyRequest  # noqa: E501
from server.models.status import Status  # noqa: E501

keys: list[Key] = [Key('first'), Key('secnd')]


def get_key(slave_sae_id, number=None, size=None) -> KeyContainer:  # noqa: E501
    """Get key

    Returns Key container data from the KME to the calling master SAE. Key container data contains one or more keys. The calling master SAE may supply Key request data to specify the requirement on Key container data. The slave SAE specified by the slave_SAE_ID parameter may subsequently request matching keys from a remote KME using key_ID identifiers from the returned Key container. # noqa: E501

    :param slave_sae_id: URL-encoded SAE ID of slave SAE.
    :type slave_sae_id: str
    :param number: Number of keys requested, default value is 1
    :type number: int
    :param size: Size of each key in bits, default value is defined as key_size in Status data format
    :type size: int

    :rtype: KeyContainer
    """
    return KeyContainer(keys)


def get_key_with_key_i_ds(master_sae_id, key_id):  # noqa: E501
    """Get key with key IDs

    Returns Key container from the KME to the calling slave SAE. Key container contains keys matching those previously delivered to a remote master SAE based on the Key IDs supplied from the remote master SAE in response to its call to Get key. The KME shall reject the request with a 401 HTTP status code if the SAE ID of the requestor was not an SAE ID supplied to the &#x27;Get key&#x27; method each time it was called resulting in the return of any of the Key IDs being requested. # noqa: E501

    :param master_sae_id: URL-encoded SAE ID of master SAE.
    :type master_sae_id: str
    :param key_id: single key ID
    :type key_id: 

    :rtype: KeyContainer
    """
    return 'do some magic!'


def get_status(slave_sae_id):  # noqa: E501
    """Get status

    Returns Status from a KME to the calling SAE. Status contains information on keys available to be requested by a master SAE for a specified slave SAE. # noqa: E501

    :param slave_sae_id: URL-encoded SAE ID of slave SAE.
    :type slave_sae_id: str

    :rtype: Status
    """
    return 'do some magic!'


def post_key(body, slave_sae_id):  # noqa: E501
    """Post key

    Returns Key container data from the KME to the calling master SAE. Key container data contains one or more keys. The calling master SAE may supply Key request data to specify the requirement on Key container data. The slave SAE specified by the slave_SAE_ID parameter may subsequently request matching keys from a remote KME using key_ID identifiers from the returned Key container. # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param slave_sae_id: URL-encoded SAE ID of slave SAE.
    :type slave_sae_id: str

    :rtype: KeyContainer
    """
    if connexion.request.is_json:
        body = KeyRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def post_key_with_key_i_ds(body, master_sae_id):  # noqa: E501
    """Post key with key IDs

    Returns Key container from the KME to the calling slave SAE. Key container contains keys matching those previously delivered to a remote master SAE based on the Key IDs supplied from the remote master SAE in response to its call to Get key. The KME shall reject the request with a 401 HTTP status code if the SAE ID of the requestor was not an SAE ID supplied to the &#x27;Get key&#x27; method each time it was called resulting in the return of any of the Key IDs being requested. # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param master_sae_id: URL-encoded SAE ID of master SAE.
    :type master_sae_id: str

    :rtype: KeyContainer
    """
    if connexion.request.is_json:
        body = KeyIDs.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
