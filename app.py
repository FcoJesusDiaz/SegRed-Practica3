#!/usr/bin/env python3

import exceptions


from pickle import NONE
from telnetlib import NOP
from flask import Flask, request
from flask_restful import Resource, Api
from secrets import token_urlsafe, token_hex
from hashlib import pbkdf2_hmac
from threading import Timer, Lock
import os

import json


# --------------------------------------------------------GLOBAL VARIABLES--------------------------------------------------------#
ROOT_DIR = "database/"
g_tokens = {}
lock = Lock()


# --------------------------------------------------------API INICIALIZATION--------------------------------------------------------#
app = Flask(__name__)
api = Api(app, errors=exceptions.ERRORS)


app.config['SERVER_NAME'] = 'myserver.local:5000'


# --------------------------------------------------------METHODS--------------------------------------------------------#
def retrieve_entry(user):
    with open('shadow.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            existing_user = line.split(":")[0]
            if user == existing_user:
                return line
    return ''


def generate_hash(salt, text):
    return pbkdf2_hmac('sha512', text.encode(), salt.encode(), 10000)


def get_req_args(*args):
    results = [None] * len(args)
    i = 0

    # Get json data
    json_obj = request.get_json(silent=True, force=True)

    if json_obj:
        for arg in args:
            results[i] = json_obj.get(arg)
            i = i + 1
        return tuple(results)

    # Get form data
    for arg in args:
        results[i] = request.form.get(arg)
        if not results[i]:
            break
        i = i + 1

    return tuple(results)


def check_auth_header():
    auth_header = request.headers.get("Authorization")
    token = None

    if not auth_header:
        raise exceptions.UnauthorizedHeader

    if len(auth_header.split()) != 2 or auth_header.split()[0] != "token":
        raise exceptions.BadRequestAuthHeader

    token = auth_header.split()[1]

    return auth_header, token


def revokeToken(token):
    # Mutex is necessary here because dict.pop operation is not thread safe
    with lock:
        g_tokens.pop(token)


# --------------------------------------------------------CLASSES--------------------------------------------------------#
@api.resource('/version', methods=["GET"], provide_automatic_options=False)
class Version(Resource):
    def get(self):
        return {'version': '1.0'}


@api.resource("/signup", methods=["POST"])
class Signup(Resource):
    def post(self):
        user, passwd = get_req_args("username", "password")

        if None in (user, passwd):
            raise exceptions.BadRequestUserPass

        if retrieve_entry(user):
            raise exceptions.UserAlreadyExists
        
        os.mkdir(f"{ROOT_DIR}{user}")

        self.add_entry(user, passwd)
        token = token_urlsafe(40)
        g_tokens[token] = user
        Timer(300.0, revokeToken, [token]).start()
        return {'access token': token, 'warning': 'all tokens expire after 5 minutes'}


    def add_entry(self, user, passwd):
        with open('shadow.txt', 'a') as file:
            salt = token_hex(16)
            digest = generate_hash(salt, passwd)
            new_entry = user + ":$6$" + salt + "$" + digest.hex() + "\n"
            file.write(new_entry)



@api.resource("/login", methods=["POST"])
class Login(Resource):
    def post(self):
        user, passwd = get_req_args("username", "password")

        if None in (user, passwd):
            raise exceptions.BadRequestUserPass

        entry = retrieve_entry(user)
        if not entry:
            raise exceptions.UserDoesNotExist
  
        if not self.check_password(entry, passwd):
            raise exceptions.WrongPass

        token = token_urlsafe(40)
        g_tokens[token] = user
        Timer(300.0, revokeToken, [token]).start()
        return {'access token': token, 'warning': 'all tokens expire after 5 minutes'}


    def check_password(self, entry, passwd):
        fields = entry.split("$")
        salt = fields[2]
        hash_pw = fields[3].strip()
        digest = generate_hash(salt, passwd)

        return hash_pw == digest.hex()


@api.resource("/<string:username>/<string:doc_id>", methods=["GET", "POST", "PUT", "DELETE"])
class UserDocuments(Resource):
    
    def __init__(self):
        super().__init__()
        self.auth_header, self.token = check_auth_header()
        
    
    def check_user(self, username):
        if g_tokens.get(self.token) != username:
            raise exceptions.UnauthorizedToken()


    def get(self, username, doc_id):
        self.check_user(username)
        file_path = f"{ROOT_DIR}{username}/{doc_id}"
        
        self.check_file_exists(file_path)

        with open(file_path) as file:
            data = json.load(file)
        return data


    def post(self, username, doc_id):
        self.check_user(username)
        content = self.check_content()

        file_path = f"{ROOT_DIR}{username}/{doc_id}"

        if os.path.isfile(file_path):
            raise exceptions.FileAlreadyExists


        self.write_file(file_path, content)

        return {"size": os.path.getsize(file_path)}


    def put(self, username, doc_id):
        self.check_user(username)
        content = self.check_content()
        file_path = f"{ROOT_DIR}{username}/{doc_id}"
        
        self.check_file_exists(file_path)
        self.write_file(file_path, content)

        return {"size": os.path.getsize(file_path)}
        
    
    def delete(self, username, doc_id):
        self.check_user(username)
        file_path = f"{ROOT_DIR}{username}/{doc_id}"
        self.check_file_exists(file_path)
        os.remove(file_path)
        return {}


    def check_content(self):
        content = get_req_args("doc_content")[0] # Tuples with one element return (val, ) so indexing is neccessary here
        content_json = None

        if not content:
            raise exceptions.BadRequestContent

        try:
            content_json = json.loads(content)
        except ValueError:
            raise exceptions.BadRequestJson

        return content_json


    def write_file(self, file_path, contents):
        with open(file_path, "w") as file:
            json.dump(contents, file)


    def check_file_exists(self, file_path):
        if not os.path.isfile(file_path):
            raise exceptions.FileNotFound



@api.resource("/<string:username>/_all_docs", methods=["GET"])
class AllDocuments(Resource):
    
    def __init__(self):
        super().__init__()
        self.auth_header, self.token = check_auth_header()

    def check_user(self, username):
        if g_tokens.get(self.token) != username:
            raise exceptions.UnauthorizedToken()
    
    
    def get(self, username):
        self.check_user(username)
        all_content = {}
        dir_path = f"{ROOT_DIR}{username}"
        files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

        for file in files:
            with open(f"{dir_path}/{file}", "r") as fp:
                all_content.update({file:json.load(fp)})

        return all_content


if __name__ == '__main__':
    app.run(debug=True, ssl_context=("domain.crt", "domain.key"))
