endpoint = {
    "name": "ENDPOINT",
    "valueFrom": {
        "secretKeyRef": {
            "name": "secret3",
            "key": "endpoint",
            "optional": False
        }
    }
}

access_key = {
    "name": "ACCESS_KEY",
    "valueFrom": {
        "secretKeyRef": {
            "name": "secret3",
            "key": "access_key",
            "optional": False
        }
    }
}

secret_key = {
    "name": "SECRET_KEY",
    "valueFrom": {
        "secretKeyRef": {
            "name": "secret3",
            "key": "secret_key",
            "optional": False
        }
    }
}
