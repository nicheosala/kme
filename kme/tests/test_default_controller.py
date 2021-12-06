from typing import Final

from webtest import TestApp
from webtest import TestResponse as Response  # Renamed in order to avoid pytest warnings

from kme.models.key_container import KeyContainer
from kme.models.key_i_ds import KeyIDs
from kme.models.key_i_ds_key_i_ds import KeyIDsKeyIDs
from kme.models.key_request import KeyRequest
from kme.models.status import Status

base_url: Final[str] = "/api/v1/keys"


class TestDefaultController:
    """DefaultController integration test stubs"""

    def test_get_key(self, test_app: TestApp) -> None:
        """Test case for get_key"""
        slave_sae_id: Final[str] = 'slave_sae_id_example'
        number: Final[int] = 2
        size: Final[int] = 2

        response: Final[Response] = test_app.get(
            url=f'{base_url}/{slave_sae_id}/enc_keys',
            params={'number': number, 'size': size}
        )

        key_container: Final[KeyContainer] = \
            KeyContainer.from_json(response.json_body)

        assert response.status_int == 200
        assert len(key_container.keys) == number
        # assert all(len(k.key) == size for k in key_container.keys)
        # TODO

    def test_get_key_with_key_i_ds(self, test_app: TestApp) -> None:
        """Test case for get_key_with_key_i_ds"""
        master_sae_id: Final[str] = "master_sae_id_example"
        key_id: Final[str] = "example_uuid_key_id"

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

        status: Final[Status] = \
            Status.from_json(response.json_body)

        assert response.status_int == 200
        # TODO

    def test_post_key(self, test_app: TestApp) -> None:
        """Test case for post_key"""
        key_request: Final[KeyRequest] = KeyRequest()  # TODO
        slave_sae_id: Final[str] = 'slave_sae_id_example'

        response: Final[Response] = test_app.post(
            url=f'{base_url}/{slave_sae_id}/enc_keys',
            params=str(key_request),
            content_type='application/json'
        )

        key_container: Final[KeyContainer] = \
            KeyContainer.from_json(response.json_body)

        assert response.status_int == 200
        # TODO

    def test_post_key_with_key_i_ds(self, test_app: TestApp) -> None:
        """Test case for post_key_with_key_i_ds"""
        key_ids: Final[KeyIDs] = KeyIDs(key_IDs=[KeyIDsKeyIDs(key_ID="todo")])  # TODO
        master_sae_id: Final[str] = 'master_sae_id_example'

        response: Final[Response] = test_app.post(
            url=f'{base_url}/{master_sae_id}/dec_keys',
            params=str(key_ids),
            content_type='application/json'
        )

        key_container: Final[KeyContainer] = \
            KeyContainer.from_json(response.json_body)

        assert response.status_int == 200
        # TODO
