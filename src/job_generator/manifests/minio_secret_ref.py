import os

_minio_secret = os.environ["MINIO_SECRET_NAME"]

endpoint = {
    "name": "ENDPOINT",
    "valueFrom": {
        "secretKeyRef": {
            "name": _minio_secret,
            "key": "endpoint",
            "optional": False
        }
    }
}

access_key = {
    "name": "ACCESS_KEY",
    "valueFrom": {
        "secretKeyRef": {
            "name": _minio_secret,
            "key": "access_key",
            "optional": False
        }
    }
}

secret_key = {
    "name": "SECRET_KEY",
    "valueFrom": {
        "secretKeyRef": {
            "name": _minio_secret,
            "key": "secret_key",
            "optional": False
        }
    }
}
