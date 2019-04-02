#!/usr/bin/env python
from sanic import Sanic
from sanic_motor import BaseModel, ObjectId
from sanic.response import json
from os import environ
from hashlib import sha224
from datetime import datetime

app = Sanic('users')

db_settings = environ.get('DB_URI', 'mongodb://127.0.0.1:27017/users')
secret_key = environ.get('SECRET_KEY', '1sert$rfbt8#7n*51$(8')
app.config.update({'MOTOR_URI': db_settings})

BaseModel.init_app(app)


def get_password_hash(password):
    """return password hash"""
    pass_secret = password + secret_key
    return sha224(pass_secret.encode()).hexdigest()


class User(BaseModel):
    __coll__ = 'users'
    __unique_fields__ = ['username']

    def check_password(self, password):
        return self.password == get_password_hash(password)

    def get_dict(self):
        return {'id': str(self.id), 'username': self.username, 'created_at': self.created_at}


@app.route('/user/registry', methods=['POST'])
async def registry(request):
    """create new user"""
    username = request.json.get('username', '').strip().lower()
    password = request.json.get('password', '').strip()
    created_at = request.json.get('created_at', datetime.utcnow())
    if username and password:
        password_hash = get_password_hash(password)
        is_uniq = await User.is_unique(doc={'username': username})
        if is_uniq in (True, None):
            result = await User.insert_one({'username': username, 'password': password_hash, 'created_at': created_at})
            return json({'user_id': str(result.inserted_id)}, status=201)
        return json({'error': 'username must be unique'}, status=400)
    return json({'error': 'username and password is required fields'}, status=400)


@app.route('/user/auth', methods=['POST'])
async def auth(request):
    """authenticate user by username & password"""
    username = request.json.get('username', '').strip().lower()
    password = request.json.get('password', '').strip()
    if username and password:
        user = await User.find_one({'username': username})
        if not user:
            return json({'error': 'User with this username not found'}, status=404)
        if user.check_password(password):
            return json(user.get_dict(), status=200)
    return json({'error': 'username and password is required fields'}, status=401)


@app.route('/user/<user_id>', methods=['GET'])
async def get_user(request, user_id):
    """return user object"""
    user = await User.find_one({'_id': ObjectId(user_id)})
    if not user:
        return json({'status': 'failure'}, status=404)
    return json(user.get_dict(), status=200)

if __name__ == '__main__':
    is_debug = environ.get('DEBUG', True)
    app.run(host='0.0.0.0', port=8000, debug=is_debug, workers=4)
