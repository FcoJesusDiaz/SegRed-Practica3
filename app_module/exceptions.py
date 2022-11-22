#!/usr/bin/env python3
"""
Custom exceptions classes and json dictionary of errors used for the API class inicialization

Authors:
    - Francisco Jesús Díaz Pellejero
    - Miguel de las Heras Fuentes
"""

from werkzeug import exceptions


class BadRequestUserPass(exceptions.BadRequest):
    pass

class BadRequestAuthHeader(exceptions.BadRequest):
    pass

class BadRequestContent(exceptions.BadRequest):
    pass

class BadRequestJson(exceptions.BadRequest):
    pass

class UserDoesNotExist(exceptions.Unauthorized):
    pass

class UnauthorizedHeader(exceptions.Unauthorized):
    pass

class UnauthorizedToken(exceptions.Unauthorized):
    pass

class WrongPass(exceptions.Unauthorized):
    pass

class UserAlreadyExists(exceptions.Conflict):
    pass

class FileAlreadyExists(exceptions.Conflict):
    pass

class FileNotFound(exceptions.NotFound):
    pass


ERRORS = {
    'BadRequestUserPass': {
        'message': "Could not handle request: parameters 'username' and 'password' not specified or bad json message",
        'status': 400
    },
    'BadRequestAuthHeader': {
        'message': "Incorrect authorization header syntax. It should be 'Authorization: token <token>'",
        'status': 400
    },
    'BadRequestContent': {
        'message': "Could not handle request: 'doc_content' parameter not scpecified or incorrect json message",
        'status': 400
    },
    'BadRequestJson': {
        'message': "The content must be a json string",
        'status': 400
    },
    'UnauthorizedToken':{
        'message': "Incorrect token",
        'status': 401,
    },
    'UnauthorizedHeader': {
        'message': "Did not include Authorization header",
        'status': 401
    },
    'UserDoesNotExist':{
        'message': "User does not exist",
        'status': 401,
    },
    'WrongPass':{
        'message': "Incorrect password",
        'status': 401,
    },
    'NotFound':{
        'message': "Resource not found",
        'status': 404,
    },
    'FileNotFound':{
        'message': "File does not exist",
        'status': 404,
    },
    'MethodNotAllowed': {
        'message': "Method not allowed",
        'status': 405,
    },
    'UserAlreadyExists':{
        'message': "User already exists",
        'status': 409,
    },
    'FileAlreadyExists':{
        'message': "File already exists",
        'status': 409,
    },
}