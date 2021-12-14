from typing import Final

from immutabledict import immutabledict
from webtest import TestApp
from webtest import TestResponse as Response  # Renamed in order to avoid pytest warnings

from kme.models.error import Error, UnsupportedMandatoryExtensionParameterError
from kme.models.key_container import KeyContainer
from kme.models.key_i_ds import KeyIDs
from kme.models.key_i_ds_key_i_ds import KeyIDsKeyIDs
from kme.models.key_request import KeyRequest

base_url: Final[str] = "/api/v1/keys"


class TestDefaultController:
    """DefaultController integration test stubs"""

    def test_get_key(self, test_app: TestApp) -> None:
        """Test case for get_key"""
        slave_sae_id: Final[str] = 'slave_sae_id_example'
        number: Final[int] = 2

        response: Final[Response] = test_app.get(
            url=f'{base_url}/{slave_sae_id}/enc_keys',
            params={'number': number}
        )

        key_container: Final[KeyContainer] = \
            KeyContainer.from_json(response.json_body)

        assert response.status_int == 200
        assert len(key_container.keys) == number

    def test_get_key_with_key_i_ds(self, test_app: TestApp) -> None:
        """Test case for get_key_with_key_i_ds"""
        master_sae_id: Final[str] = "master_sae_id_example"
        key_id: Final[str] = "bc490419-7d60-487f-adc1-4ddcc177c139"

        response: Final[Response] = test_app.get(
            url=f'{base_url}/{master_sae_id}/dec_keys',
            params={"key_ID": key_id}
        )

        key_container: Final[KeyContainer] = \
            KeyContainer.from_json(response.json_body)

        assert response.status_int == 200
        assert len(key_container.keys) == 1
        # TODO

    def test_get_status(self, test_app: TestApp) -> None:
        """Test case for get_status"""
        slave_sae_id: Final[str] = 'slave_sae_id_example'

        response: Final[Response] = test_app.get(
            url=f'{base_url}/{slave_sae_id}/status',
        )

        assert response.status_int == 200

    def test_post_key(self, test_app: TestApp) -> None:
        """Test case for post_key"""
        number: Final[int] = 5
        key_request: Final[KeyRequest] = KeyRequest(number=number)
        slave_sae_id: Final[str] = 'slave_sae_id_example'

        response: Final[Response] = test_app.post(
            url=f'{base_url}/{slave_sae_id}/enc_keys',
            params=key_request.json_string,
            content_type='application/json'
        )

        key_container: Final[KeyContainer] = \
            KeyContainer.from_json(response.json_body)

        assert response.status_int == 200
        assert len(key_container.keys) == number

    def test_post_key_with_key_i_ds(self, test_app: TestApp) -> None:
        """Test case for post_key_with_key_i_ds"""
        key_ids: Final[KeyIDs] = KeyIDs(key_IDs=tuple([KeyIDsKeyIDs(key_ID="bc490419-7d60-487f-adc1-4ddcc177c139")]))
        master_sae_id: Final[str] = 'master_sae_id_example'

        response: Final[Response] = test_app.post(
            url=f'{base_url}/{master_sae_id}/dec_keys',
            params=key_ids.json_string,
            content_type='application/json'
        )

        key_container: Final[KeyContainer] = \
            KeyContainer.from_json(response.json_body)

        assert response.status_int == 200
        assert len(key_container.keys) == len(key_ids.key_IDs)

    def test_post_key_non_empty_extension_mandatory(self, test_app: TestApp) -> None:
        """Test case for post_key with non-empty 'extension_mandatory' parameter."""
        key_request: Final[KeyRequest] = KeyRequest(extension_mandatory=(immutabledict({"ciao": "mamma"}),))
        slave_sae_id: Final[str] = 'slave_sae_id_example'

        response: Final[Response] = test_app.post(
            url=f'{base_url}/{slave_sae_id}/enc_keys',
            params=key_request.json_string,
            content_type='application/json',
            expect_errors=True
        )

        error: Final[Error] = \
            Error.from_json(response.json_body)

        assert response.status_int == 400
        assert error.message == UnsupportedMandatoryExtensionParameterError().message
