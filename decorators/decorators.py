# decorators.py

from flask import jsonify, request
from marshmallow import ValidationError
from functools import wraps
from flask import jsonify, abort, make_response,request


def required_params(schema):
    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                schema.load(request.get_json())
            except ValidationError as err:
                error = {
                    "status": "error",
                    "messages": err.messages
                }
                return jsonify(error), 403
            return fn(*args, **kwargs)

        return wrapper
    return decorator


def api_key_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        key = "1234"
        print("the key is",key)
        print("from headers",request.headers.get('api-key'))
        if  request.headers.get('api-key') == key:
            return function(*args, **kwargs)
        else:
            abort(make_response(jsonify(message="API key required"), 403))
    return decorated_function
