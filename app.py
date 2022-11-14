#!/usr/bin/env python3

from pickle import NONE
from telnetlib import NOP
from flask import Flask, request
from flask_restful import Resource, Api
from secrets import token_urlsafe, token_hex
from hashlib import pbkdf2_hmac


from werkzeug import exceptions

app = Flask(__name__)

# This domain name works if 'myserver.local' is added to the 127.0.0.1 ip address line
# in the /etc/hosts file'
#app.config['SERVER_NAME'] = 'myserver.local:5000'


errors = {
    'BadRequest': {
        'message': "Could not handle request, the parameters must be 'username' and 'password'",
        'status': 400
    },
    'Unauthorized':{
        'message': "Incorrect username or password",
        'status': 401,
    },
    'NotFound':{
        'message': "Url not found",
        'status': 404,
    },
    'MethodNotAllowed': {
        'message': "Method not allowed",
        'status': 405,
    },
    'Conflict':{
        'message': "User already exists",
        'status': 409,
    },
}


def retrieve_entry(user):
    with open('shadow.txt', 'r') as file:
        line = file.readline()
        existing_user = line.split(":")[0]
        if user == existing_user:
            return line
    return ''

def generate_hash(salt, text):
    return pbkdf2_hmac('sha512', text.encode(), salt.encode(), 10000)


api = Api(app, errors=errors)


@api.resource('/version', methods=["GET"], provide_automatic_options=False)
class Version(Resource):
    def get(self):
        return {'version': '1.0'}


@api.resource("/signup", methods=["POST"])
class Signup(Resource):
    def post(self):
        user = request.form.get('username')
        passwd = request.form.get('password')

        if None in (user, passwd):
            raise exceptions.BadRequest()

        if retrieve_entry(user):
            raise exceptions.Conflict()

        self.add_entry(user, passwd)
        token = token_urlsafe(40)
        return {'access token': token}


    def add_entry(self, user, passwd):
        with open('shadow.txt', 'a') as file:
            salt = token_hex(16)
            digest = generate_hash(salt, passwd)
            new_entry = user + ":$6$" + salt + "$" + digest.hex() + "\n"
            file.write(new_entry)



@api.resource("/login", methods=["POST"])
class Login(Resource):
    def post(self):
        user = request.form.get('username')
        passwd = request.form.get('password')

        if None in (user, passwd):
            raise exceptions.BadRequest()

        entry = retrieve_entry(user)
        if not entry:
            raise exceptions.Unauthorized()
        
        if not self.check_password(entry, passwd):
            raise exceptions.Unauthorized()
        
        token = token_urlsafe(40)
        return {'access token': token}
    

    def check_password(self, entry, passwd):
        fields = entry.split("$")
        salt = fields[2]
        hash_pw = fields[3].strip()
        digest = generate_hash(salt, passwd)

        return hash_pw == digest.hex()


@api.resource("/<string:username>/<string:doc_id>", methods=["GET", "POST", "PUT", "DELETE"])
class UserDocuments(Resource):


    def get(self, username, doc_id):
        if not retrieve_entry(username):
            raise exceptions.Unauthorized()
        
        print(f"Usuario: {username}. Doc: {doc_id}")

    def post(self, username, doc_id):
        NOP

    def put(self, username, doc_id):
        NOP
    
    def delete(self, username, doc_id):
        NOP


if __name__ == '__main__':
    #Add ssl_context='adhoc' for https
    app.run(debug=True)
