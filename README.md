# Users-Offers

## deploy
```
git clone https://github.com/Ravillatypov/Users-Offers.git
cd Users-Offers
docker-compose up
```
## Users
```
Users {
    username: str,
    password: str,
    created_at: int
}
```

- create user: `curl -XPOST http://127.0.0.1:8000/user/registry -d '{"username": "username", "password": "somepass"}'`
- authenticate user: `curl -XPOST http://127.0.0.1:8000/user/auth -d '{"username": "username", "password": "somepass"}'`
- get user object: `curl -XGET http://127.0.0.1:8000/user/{user_id}`


## Offers
```
Offer {
    user_id: int,
    title: str,
	text: str,
    created_at: int
}
```
- create offer: `curl -XPOST http://127.0.0.1:8001/offer/create -d '{"user_id": "user id", "title": "offer title", "text": "offer text"}'`
- get offer by id: `curl -XPOST http://127.0.0.1:8001/offer -d '{"offer_id": "offer id"}'`
- get offers by user: `curl -XPOST http://127.0.0.1:8001/offer -d '{"user_id": "user id"}'`
- get all offers: `curl -XPOST http://127.0.0.1:8001/offer`
