import uuid

from sdn_controller.database.orm import Kme

qos = {"max_bandwidth": 10, "min_bandwidth": 5, "jitter": 2, "ttl": 120, "clients_shared_path_enable": False,
       "clients_shared_keys_required": False}

fake_kme = Kme(kme_id=uuid.UUID('00000000-0000-0000-0000-000000000000'), ip="localhost", port=5000)
