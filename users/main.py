#!/usr/bin/env python
from sanic import Sanic
from sanic_motor import BaseModel
from sanic.response import json
from os import environ

app = Sanic('users')

db_settings = environ.get('DB_URI', 'mongodb://127.0.0.1:27017/users')
app.config.update({'MOTOR_URI': db_settings})

BaseModel.init_app(app)


class User(BaseModel):
    __coll__ = 'users'
    __unique_fields__ = ['username']


@app.route('/user/registry', methods=['POST'])
async def registry(request):
    return json({'status': 'ok'}, status=201)


@app.route('/user/auth', methods=['POST'])
async def auth(request):
    return json({'status': 'ok'}, status=200)


@app.route('/user/<user_id>', methods=['GET'])
async def get_user(request, user_id=None):
    return json({'status': 'ok'}, status=200)


@app.route('/user', methods=['GET'])
async def get_user_list(request):
    return json({'status': 'ok'}, status=200)

if __name__ == '__main__':
    is_debug = environ.get('DEBUG', True)
    app.run(host='0.0.0.0', port=8000, debug=is_debug, workers=4)
