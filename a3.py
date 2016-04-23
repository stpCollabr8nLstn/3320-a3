from init import app

import views, auth, api


if __name__ == '__main__':
    app.run(debug=True)
