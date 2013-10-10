Architecture Notes
==================


Architecture overview
---------------------

<pre><code>
Client (Javascript/Cloud Storage)
        ʌ           ʌ
        |           |
        |           |
        |           |
        |           |
        |           v
        |   SockJS Server (Tornado/Compute Engine)
        |           ʌ
        |           |
        |           |
        |           |
        |           |
        |           v
        |   PubSub Server (Redis/Compute Engine)
        |           ʌ
        |           |
        |           |
        |           |
        |           |
        v           v
REST API (Django/Appengine)
</code></pre>


Communication overview
----------------------

MMOTD clients will have 2 primary means of in-game communications, a regular old REST API and a shiny websocket (sockJS) connection.

In any case where a client requires either an acknowledgement of a request or an immediate response from the server, the REST API should be used.  This API is a fairly standard JSON API (accepts application/x-www-form-urlencoded data) which will perform functions such as creating and managing games and performing user authentication.

Other communications which do not require immediate ack can be sent via the socket, this includes data such as in-game/in-lobby chat messages and direct client-to-client comms when the game is running (not sure exactly what data we'll need yet).

Server can push events to connected clients via Redis and the websocket connections in response to anything that happens server side, e.g. Notifying players when someone joins or leaves a game, notifying all waiting players if a new game has been created etc.


(Still to be decided/figured out) When a game is created the server will spin up a new thread on appengine which will listen to all data from the channel the clients are communicating on.  Initially this will not have much of a purpose but will be used for out-of-band operations such as cheating detection and responding directly to/marshalling/processing of socket data as it travels between the clients.

**TL;DR:**

    - Client-Server synchronous comms via REST API
    - Client-Server asynchronous comms via sockJS
    - Server-Server communication via Redis PubSub
