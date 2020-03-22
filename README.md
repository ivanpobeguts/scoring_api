# Scoring API
Simple scoring api with declarative validation language.

Two serveces are avaliable:

get_score:
```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"account": "horns&hoofs", "login": "ivan", "method":
"online_score", "token":
"a971403885c6953b5e23b240c73df20ab5e682e00942a07d03e39ac5824a3d2da975b0e5d50b957ea464e8c25ced6b7fe2b2055f9de78002007280cafc377dfd",
"arguments": {"phone": "79175002040", "email": "stupnikov@otus.ru", "first_name": "Стансилав", "last_name": "Ступников", "birthday": "01.01.1999", "gender": 1}}' http://127.0.0.1:8080/method/

{"response": "{\"score\": 5.0}", "code": 200}
```

clients_interests:
```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"account": "horns&hoofs", "login": "ivan", "method": "clients_interests", "token": "a971403885c6953b5e23b240c73df20ab5e682e00942a07d03e39ac5824a3d2da975b0e5d50b957ea464e8c25ced6b7fe2b2055f9de78002007280cafc377dfd", 
"arguments": {"client_ids": [1,2,3,4], "date": "20.07.2017"}}' http://127.0.0.1:8080/method/

{"response": "{\"1\": [\"travel\", \"cinema\"], \"2\": [\"pets\", \"travel\"], \"3\": [\"hi-tech\", \"sport\"], \"4\": [\"cars\", \"geek\"]}", "code": 200}
```

## How to run server

Script requires python >= 3.7.

Run server with the following command:

```bash
$ python api.py --port <server port> --log <log path>
```

