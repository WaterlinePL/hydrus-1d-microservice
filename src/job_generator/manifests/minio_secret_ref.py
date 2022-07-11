minio_secret = "minio-secret"

endpoint = {
    "name": "ENDPOINT",
    "valueFrom": {
        "secretKeyRef": {
            "name": minio_secret,
            "key": "endpoint",
            "optional": False
        }
    }
}

access_key = {
    "name": "ACCESS_KEY",
    "valueFrom": {
        "secretKeyRef": {
            "name": minio_secret,
            "key": "access_key",
            "optional": False
        }
    }
}

secret_key = {
    "name": "SECRET_KEY",
    "valueFrom": {
        "secretKeyRef": {
            "name": minio_secret,
            "key": "secret_key",
            "optional": False
        }
    }
}
