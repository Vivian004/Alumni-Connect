from flask import jsonify
import requests
import json
# import string
# import random

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s : %(name)s : %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_login():
    url = "http://localhost:5000/api/auth/login/"

    # Valid User
    username_valid = "testuser"
    password_valid = "test"

    # Invalid User
    username_invalid = "invaliduser"
    password_invalid = "pwdinvalid"

    # Additional headers
    headers = {"Content-Type": "application/json"}

    # Body
    payload_user_invalid = {
        "username": username_invalid,
        "passwd": password_invalid,
    }
    payload_pwd_wrong = {
        "username": username_valid,
        "passwd": password_valid,
    }
    payload_valid = {
        "username": "testuser",
        "passwd": "test",
    }

    # Username not exist
    res0 = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload_user_invalid))
    assert res0.status_code == 401

    # Password not correct
    res1 = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload_pwd_wrong))
    assert res1.status_code == 401

    # Login successfully
    res2 = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload_valid))
    assert res2.status_code == 200


if __name__ == "__main__":
    test_login()
