# third-party imports
import werkzeug.serving
from socketio.server import SocketIOServer

# local imports
from app import app


@werkzeug.serving.run_with_reloader
def run_dev_server():
    app.debug = True
    app.secret_key = 'development_key'
    port = 6020
    SocketIOServer(('0.0.0.0', port), app, resource="socket.io").serve_forever()

if __name__ == "__main__":
    run_dev_server()
