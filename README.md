A web service that allows a user to play against a computer via a REST API. The API allows the user to create a new game, make the next move in a game, and list all games previously played.

## Requirements
 
 * python v3.9+
 * pip

## Install dependencies

```
pip install -r requirements.txt
```

## Start test server

```
uvicorn app.main:app --reload
```

## Swagger UI interactive documentation

An automatic interactive API documentation can be found at: [http://127.0.0.1:8000/docs]

## How to use it

More information can be found [here](docs/API.md)
