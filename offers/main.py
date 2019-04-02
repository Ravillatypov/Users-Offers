#!/usr/bin/env python
from sanic import Sanic
from sanic_motor import BaseModel, ObjectId
from sanic.response import json
from os import environ
from datetime import datetime
from aiohttp import ClientSession

app = Sanic('offers')

db_settings = environ.get('DB_URI', 'mongodb://127.0.0.1:27017/offers')
url_for_user_api = environ.get('USER_API', 'http://users:8000/user/')
app.config.update({'MOTOR_URI': db_settings})

BaseModel.init_app(app)


async def is_user_exist(user_id):
    """return True if user exist on service `users`"""
    async with ClientSession() as session:
        async with session.get(url_for_user_api + user_id) as resp:
            return resp.status == 200


class Offers(BaseModel):
    __coll__ = 'offers'
    __unique_fields__ = ['user_id, title']

    def get_dict(self):
        return {'id': str(self.id), 'user_id': self.user_id, 'title': self.title,
                'text': self.text, 'created_at': self.created_at}

    @classmethod
    async def create(self, user_id, title, text, created_at):
        is_unique = await self.is_unique(doc={'user_id': user_id, 'title': title})
        if is_unique and await is_user_exist(user_id):
            result = await self.insert_one({'user_id': user_id, 'title': title, 'text': text, 'created_at': created_at})
            return str(result.inserted_id)
        return False


@app.route('/offer/create', methods=['POST'])
async def create_offer(request):
    """create offer"""
    user_id = request.json.get('user_id', '')
    title = request.json.get('title', '').strip()
    text = request.json.get('text', '').strip()
    created_at = request.json.get('created_at', datetime.utcnow())
    if user_id and title and text:
        offer_id = await Offers.create(user_id, title, text, created_at)
        if offer_id:
            return json({'offer_id': offer_id}, status=201)
    return json({'error': 'user_id, title and text required'}, status=400)


@app.route('/offer', methods=['POST'])
async def get_offers(request):
    """get offer or offers"""
    user_id = request.json.get('user_id', '')
    offer_id = request.json.get('offer_id', '')
    if offer_id:
        offer = await Offers.find_one({'_id': ObjectId(offer_id)})
        if offer:
            return json(offer.get_dict(), status=200)
    elif user_id:
        offers = await Offers.find({'user_id': user_id})
    else:
        offers = await Offers.find()
    if offers.count():
        result = [i.get_dict() for i in offers]
        return json(result, status=200)
    return json([], status=200)

if __name__ == '__main__':
    is_debug = environ.get('DEBUG', True)
    app.run(host='0.0.0.0', port=8000, debug=is_debug, workers=4)
