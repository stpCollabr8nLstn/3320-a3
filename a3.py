from init import app

import views, auth, api


if __name__ == '__main__':
    socketio.run(debug=True)
