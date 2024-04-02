# Noughts and Crosses 

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


## Development information

### Development time
The first working prototype of the project took about two hours, then I spent two more hours adding multiple user support.

### Database
I choose to use SQLite because it was easier to setup as a prototype. But it can easily changed to other SQL database changing the `SQLALCHEMY_DATABASE_URL` constant at the config file.

### Config file
All project constants are stored in the [app/config.py](app/config.py) file. 
This file should load this information from environment variables to ease with the setup of multiple environments (development, staging, production) as to prevent publishing sensitive information.

### Other user games
If we try to interact with the game of another user, the API will fail with a 404 not found error.
This is to "hide" other user information (A forbidden error would imply the requested game exists).

### Possible improvements

#### Multiplayer options
Can be implemented adding a nullable second userId to the game, and disabling the "IA" when not null

#### IA plays first
Should separate the IA behavior into another function and called if requested on game creation

#### Real IAs
Could be defined an abstract base class for the IA and implement subclasses with different behaviors.
When creating the game, the user should select the specific behavior for the game.
