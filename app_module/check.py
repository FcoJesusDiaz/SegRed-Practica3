#!/usr/bin/env python3
"""
Module used for checking correct input from user

Authors:
    - Francisco Jesús Díaz Pellejero
    - Miguel de las Heras Fuentes
"""

import json
import os

from flask import request
from app_module import entry as e
from app_module import exceptions


def password(entry, passwd):
    fields = entry.split("$")
    salt = fields[2]
    hash_pw = fields[3].strip()
    digest = e.generate_hash(salt, passwd)

    return hash_pw == digest.hex()


def auth_header():
    """Correct syntax: Authorization: token <token>"""
    auth_head = request.headers.get("Authorization")
    token = None

    if not auth_head:
        raise exceptions.UnauthorizedHeader

    if len(auth_head.split()) != 2 or auth_head.split()[0] != "token":
        raise exceptions.BadRequestAuthHeader

    token = auth_head.split()[1]

    return auth_head, token


def file_exists(file_path):
    if not os.path.isfile(file_path):
        raise exceptions.FileNotFound


def json_content(content):
    content_json = None

    if not content:
        raise exceptions.BadRequestContent

    try:
        content_json = json.loads(content)
    except ValueError:
        raise exceptions.BadRequestJson

    return content_json