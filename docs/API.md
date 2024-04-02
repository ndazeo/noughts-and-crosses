## Create a new user

A [POST to /users/](http://127.0.0.1:8000/docs#/games/create_user_users__post) creates a new user.
The body of the POST must contain the username and password.


## Create a new game

A [POST to /games/](http://127.0.0.1:8000/docs#/games/create_game_games__post) creates a new game of Noughts and Crosses.
This call returns a game object where the ID can be found.

## Make a move

A [POST to /games/{id}/moves](http://127.0.0.1:8000/docs#/games/make_move_games__id__moves_post)
allows to make the next move in the game {id} by specifying in the body the co-ordinates to move on. e.g. {"x": 1, "y": 1} would denote a move to the middle square by the requesting player, and returns the new state of the board after the computer has made its random move in turn.

## View a game

A [GET to /games/{id}/](http://127.0.0.1:8000/docs#/games/get_games__id__get)
returns the game {id} with all the moves, chronologically ordered.
It also informs if the game is finished and, if there is one, the winner.

## View all games

A [GET to /games/](http://127.0.0.1:8000/docs#/games/get_all_games_games__get)
returns all games with all the moves, chronologically ordered.
It accepts two optional query params to paginate results: skip (default 0) and limit (default 10).

## View as a borad

A [GET to /games/{id}/board](http://127.0.0.1:8000/docs#/games/get_games__id__get)
returns a "graphical" like array of array showing the board for the game {id}.
