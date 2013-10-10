API Documentation for all resources under `/api/games/`
-------------------------------------------------------

All API calls required for creation of, joining and managing games are documented below. As authentication happens entirely on the client, it is necessary for the frontend to include the 'OAuth-Token' header with all requests:

    - OAuth-Token: Google OAuth2 access token which has been authorised with scopes:
        - https://www.googleapis.com/auth/userinfo.email
        - https://www.googleapis.com/auth/userinfo.profile




### Action: Get a list of all currently open games ###

Used to retrieve a list of all currently open games to be displayed on the lobby/join game screen. This is not currently paginated so will return all games except those that meet the following criteria:

    - Those created more than one hour ago
    - Those already started
    - Those already finished

- URL: `/api/games/`
- Method: GET

- Response type: application/json
- Example Response:

    <pre><code>
    {'games': [
        {
            'uuid': '37gg957-t8t394-5a683sdf9-58g7',
            'name': 'This is a name',
            'created': '2013-09-05 19:59:37',
            'creator': '230492834097204978',
            'max_players': 4,
            'players': [
                {
                    'created': '2013-09-05 19:51:23',
                    'user_id': '230492834097204978',
                    'avatar': 'https://some.domain/some.image.jpg',
                    'email': 'somebody@somewhere.com',
                    'name': 'Alice Bob',
                },
                ...
            ]
        },
        {
            'uuid': '37gg957-t8t394-5a683sdf9-58g7',
            'name': 'This is a name',
            'created': '2013-09-05 19:59:37',
            'creator': '230492834097204978',
            'max_players': 4,
            'players': [
                {
                    'created': '2013-09-05 19:51:23',
                    'user_id': '230492834097204978',
                    'avatar': 'https://some.domain/some.image.jpg',
                    'email': 'somebody@somewhere.com',
                    'name': 'Alice Bob',
                },
                ...
            ]
        }
    ]}
    </code></pre>

- Error Responses:

    - 401: `{'error': '401 Unauthorized'}`
        - returned when we are unable to validate the user's OAuth token




### Action: Create a new game ###

Used to create a new game on behalf of the authorized user. `name` should be something descriptive you can use to identify your game in the lobby. `max_players` is the maximum number of players that should be allowed to join the game.

- URL: `/api/games/`
- Method: POST

- Payload type: application/x-www-form-urlencoded
- Payload params:

    - `name`: Descriptive name for the game (str: max 140 chars)
    - `max_players`: Maximum number of players allowed in the game (int: min 2, max 16)

- Response type: application/json
- Example Response:

    <pre><code>
    {'game':
        {
            'uuid': '37gg957-t8t394-5a683sdf9-58g7',
            'name': 'This is a name',
            'created': '2013-09-05 19:59:37',
            'creator': '230492834097204978',
            'max_players': 4,
            'players': [
                {
                    'created': '2013-09-05 19:51:23',
                    'user_id': '230492834097204978',
                    'avatar': 'https://some.domain/some.image.jpg',
                    'email': 'somebody@somewhere.com',
                    'name': 'Alice Bob',
                }
            ]
        }
    }
    </code></pre>

- Error Responses:

    - 400: `{'error': '400 Bad Request', 'reason': ['name', 'max_players']}`
        - returned when the data received from the client isn't valid, `reason` will contain a list of the field names that are not valid
    - 401: `{'error': '401 Unauthorized'}`
        - returned when we are unable to validate the user's OAuth token




### Action: Get details of a specific game ###

Fetch details of a single game from the API on behalf of the authorized user. Like the list endpoint, this endpoint is not restricted and can be used to query a game's data even long after it has finished (not sure there's a use case for this, but whatever)

- URL: `/api/games/<game.uuid>/`
- Method: GET

- Response type: application/json
- Example Response:

    <pre><code>
    {'game':
        {
            'uuid': '37gg957-t8t394-5a683sdf9-58g7',
            'name': 'This is a name',
            'created': '2013-09-05 19:59:37',
            'creator': '230492834097204978',
            'max_players': 4,
            'players': [
                {
                    'created': '2013-09-05 19:51:23',
                    'user_id': '230492834097204978',
                    'avatar': 'https://some.domain/some.image.jpg',
                    'email': 'somebody@somewhere.com',
                    'name': 'Alice Bob',
                },
                ...
            ]
        }
    }
    </code></pre>

- Error Responses:

    - 401: `{'error': '401 Unauthorized'}`
        - returned when we are unable to validate the user's OAuth token
    - 404: `{'error': 'game not found'}`
        - returned when the game id is not found in the database




### Action: Modify an existing game ###

Used to modify an existing game on behalf of the authorized user. `name` should be something descriptive you can use to identify your game in the lobby. `max_players` is the maximum number of players that should be allowed to join the game (cannot be less than the current number of players in the game). Only the creator of a game can modify it. You cannot modify the game via this API after it has started.

- URL: `/api/games/<game.uuid>/`
- Method: POST

- Payload type: application/x-www-form-urlencoded
- Payload params:

    - `name`: Descriptive name for the game (str: max 140 chars, optional)
    - `max_players`: Maximum number of players allowed in the game (int: min 2, max 16, optional)

- Response type: application/json
- Example Response:

    <pre><code>
    {'game':
        {
            'uuid': '37gg957-t8t394-5a683sdf9-58g7',
            'name': 'This is another name',
            'created': '2013-09-05 19:59:37',
            'creator': '230492834097204978',
            'max_players': 6,
            'players': [
                {
                    'created': '2013-09-05 19:51:23',
                    'user_id': '230492834097204978',
                    'avatar': 'https://some.domain/some.image.jpg',
                    'email': 'somebody@somewhere.com',
                    'name': 'Alice Bob',
                },
                ...
            ]
        }
    }
    </code></pre>

- Error Responses:

    - 400: `{'error': '400 Bad Request', 'reason': ['name', 'max_players']}`
        - returned when the data received from the client isn't valid, `reason` will contain a list of the field names that are not valid
    - 401: `{'error': '401 Unauthorized'}`
        - returned when we are unable to validate the user's OAuth token
    - 403: `{'error': '403 Forbidden'}`
        - returned when user attempting to make the modification is not the creator of the game




### Action: Delete an existing game ###

Used to delete an existing game on behalf of the authorized user. Only the creator of a game can delete it.

- URL: `/api/games/<game.uuid>/`
- Method: DELETE

- Response type: application/json
- Example Response:

    <pre><code>
    {'result': 'success'}
    </code></pre>

- Error Responses:

    - 401: `{'error': '401 Unauthorized'}`
        - returned when we are unable to validate the user's OAuth token
    - 403: `{'error': '403 Forbidden'}`
        - returned when user attempting to make the deletion is not the creator of the game




### Action: Join an existing game ###

Used to join an existing game on behalf of the authorized user. Players can join a game as long it is not full. You cannot join a game via this API after it has started.

- URL: `/api/games/<game.uuid>/rpc/join/`
- Method: POST

- Response type: application/json
- Example Response:

    <pre><code>
    {'game':
        {
            'uuid': '37gg957-t8t394-5a683sdf9-58g7',
            'name': 'This is another name',
            'created': '2013-09-05 19:59:37',
            'creator': '230492834097204978',
            'max_players': 6,
            'players': [
                {
                    'created': '2013-09-05 19:51:23',
                    'user_id': '230492834097204978',
                    'avatar': 'https://some.domain/some.image.jpg',
                    'email': 'somebody@somewhere.com',
                    'name': 'Alice Bob',
                },
                {
                    'created': '2013-09-04 14:40:34',
                    'user_id': '430598340958394857',
                    'avatar': 'https://some.domain/some.image.jpg',
                    'email': 'somebodyelse@somewhere.com',
                    'name': 'Robert Alicey',
                },
                ...
            ]
        }
    }
    </code></pre>

- Error Responses:

    - 401: `{'error': '401 Unauthorized'}`
        - returned when we are unable to validate the user's OAuth token
    - 403: `{'error': '403 Forbidden', 'reason': 'full'}`
        - returned when the user attempts to join a game that is already full
    - 403: `{'error': '403 Forbidden', 'reason': 'started'}`
        - returned when user attempting to join a game which has already started




### Action: Leave an existing game ###

Used to leave an existing game on behalf of the authorized user. Players can leave any game they are currently connected to.

- URL: `/api/games/<game.uuid>/rpc/leave/`
- Method: POST

- Response type: application/json
- Example Response:

    <pre><code>
    {'game':
        {
            'uuid': '37gg957-t8t394-5a683sdf9-58g7',
            'name': 'This is another name',
            'created': '2013-09-05 19:59:37',
            'creator': '230492834097204978',
            'max_players': 6,
            'players': [
                {
                    'created': '2013-09-05 19:51:23',
                    'user_id': '230492834097204978',
                    'avatar': 'https://some.domain/some.image.jpg',
                    'email': 'somebody@somewhere.com',
                    'name': 'Alice Bob',
                },
                ...
            ]
        }
    }
    </code></pre>

- Error Responses:

    - 401: `{'error': '401 Unauthorized'}`
        - returned when we are unable to validate the user's OAuth token
    - 403: `{'error': '403 Forbidden', 'reason': 'creator'}`
        - returned when the creator attempts to leave the game, creators can only delete games, not leave them
    - 403: `{'error': '403 Forbidden', 'reason': 'not in game'}`
        - returned when a user attemps to leave a game which they are not in
