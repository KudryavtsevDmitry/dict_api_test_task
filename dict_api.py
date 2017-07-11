from datetime import datetime

from flask import Flask
from flask import request, abort, jsonify, make_response

app = Flask(__name__)

data = {}


def json_abort(message,error_code):
    abort(make_response(jsonify(error_message=message), error_code))

def json_response(value=None):
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    return jsonify(result=value, time=now_time)


@app.route('/dictionary/<key>', methods=['GET', 'PUT', 'DELETE'])
def get_value(key):
    value = data.get(key)

    if request.method == 'GET' and value:
        return json_response(value=value)

    elif request.method == 'PUT' and value:
        js = request.get_json(silent=True)
        new_value = js.get('value')
        if new_value:
            data[key] = js['value']
            return json_response(value=data[key])
        else:
            json_abort("Value not found",404)

    elif request.method == 'DELETE':
            if value: del data[key]
            return json_response()

    json_abort("Key not found", 404)


@app.route('/dictionary', methods=['POST'])
def post_value():
    js = request.get_json(silent=True)

    if ('key' or 'value') not in js:
        json_abort("Not enough parameters.", 409)
    else:
        value = data.get(js['key'])

        if value:
            json_abort("Key already exist.",409)
        else:
            data[js['key']] = js['value']
            return json_response(value=js['value'])