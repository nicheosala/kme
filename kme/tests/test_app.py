from typing import Final, Any
from uuid import UUID

from fastapi.testclient import TestClient as Client
from requests import Response

from kme.model import Error
from kme.errors import UnsupportedMandatoryExtensionParameterError
from kme.model import KeyContainer, KeyRequest, KeyIDs, KeyIDsKeyIDs
from kme.configs import TestConfig


class TestApp:
    """DefaultController integration test stubs"""

    def test_get_key(self, client: Client) -> None:
        """Test case for get_key"""
        slave_sae_id: Final[str] = 'slave_sae_id_example'
        number: Final[int] = 2

        response: Final[Response] = client.get(
            url=f'{TestConfig.BASE_URL}/{slave_sae_id}/enc_keys')

        key_container: Final[KeyContainer] = KeyContainer(**response.json())

        assert response.status_code == 200
        assert len(key_container.keys) == 1

    def test_get_key_with_key_i_ds(self, client: Client) -> None:
        """Test case for get_key_with_key_i_ds"""
        master_sae_id: Final[str] = "master_sae_id_example"
        key_id: Final[str] = "bc490419-7d60-487f-adc1-4ddcc177c139"

        response: Final[Response] = client.get(
            url=f'{TestConfig.BASE_URL}/{master_sae_id}/dec_keys',
            params={"key_ID": key_id}
        )

        key_container: Final[KeyContainer] = KeyContainer(**response.json())

        assert response.status_code == 200
        assert len(key_container.keys) == 1

    def test_get_status(self, client: Client) -> None:
        """Test case for get_status"""
        slave_sae_id: Final[str] = 'slave_sae_id_example'

        response: Final[Response] = client.get(
            url=f'{TestConfig.BASE_URL}/{slave_sae_id}/status',
        )

        assert response.status_code == 200

    def test_post_key(self, client: Client) -> None:
        """Test case for post_key"""
        number: Final[int] = 5
        key_request: Final[KeyRequest] = KeyRequest(number=number)
        slave_sae_id: Final[str] = 'slave_sae_id_example'

        response: Final[Response] = client.post(
            url=f'{TestConfig.BASE_URL}/{slave_sae_id}/enc_keys',
            data=key_request.json(exclude_none=True),
        )

        key_container: Final[KeyContainer] = KeyContainer(**response.json())

        assert response.status_code == 200
        assert len(key_container.keys) == number

    def test_post_key_with_key_i_ds(self, client: Client) -> None:
        """Test case for post_key_with_key_i_ds"""
        key_ids: Final[KeyIDs] = KeyIDs(
            key_IDs=tuple([KeyIDsKeyIDs(
                key_ID=UUID("bc490419-7d60-487f-adc1-4ddcc177c139"))]))
        master_sae_id: Final[str] = 'master_sae_id_example'

        response: Final[Response] = client.post(
            url=f'{TestConfig.BASE_URL}/{master_sae_id}/dec_keys',
            data=key_ids.json(),
        )

        key_container: Final[KeyContainer] = KeyContainer(**response.json())

        assert response.status_code == 200
        assert len(key_container.keys) == len(key_ids.key_IDs)

    def test_post_key_non_empty_extension_mandatory(self, client: Client) \
            -> None:
        """Test case for post_key with non-empty 'extension_mandatory'
        parameter. """
        extension_mandatory: Final[tuple[dict[str, Any], ...]] = \
            ({"ciao": "mamma"},)
        key_request: Final[KeyRequest] = KeyRequest(
            extension_mandatory=extension_mandatory
        )
        slave_sae_id: Final[str] = 'slave_sae_id_example'

        response: Final[Response] = client.post(
            url=f'{TestConfig.BASE_URL}/{slave_sae_id}/enc_keys',
            data=key_request.json(),
        )

        error: Final[Error] = Error(**response.json())

        assert response.status_code == 400
        assert error.message == \
               UnsupportedMandatoryExtensionParameterError.detail
