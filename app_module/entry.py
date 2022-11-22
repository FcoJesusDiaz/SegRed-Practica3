#!/usr/bin/env python3

"""
Module for adding or retrieving entries in the shadow.txt file.

Authors:
    - Francisco Jesús Díaz Pellejero
    - Miguel de las Heras Fuentes
"""

from secrets import token_hex
from hashlib import pbkdf2_hmac


def generate_hash(salt, text):
    """SHA512 + 10000 iterations of Password-Based Key Derivation Function for maximum security"""
    return pbkdf2_hmac('sha512', text.encode(), salt.encode(), 10000)


def add(user, passwd):
    with open('shadow.txt', 'a') as file:
        salt = token_hex(16)
        digest = generate_hash(salt, passwd)
        new_entry = user + ":$6$" + salt + "$" + digest.hex() + "\n"
        file.write(new_entry)


def retrieve(user):
    """ Check if the user exists in the shadow.txt file and retrieves its entry"""
    with open('shadow.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            existing_user = line.split(":")[0]
            if user == existing_user:
                return line
    return ''