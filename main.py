from app import flask_app


if __name__ == '__main__':
    context = {"users": "users.json",
               "devices": "devices.json",
               "log": False}
    fa = flask_app(context, key="adas")
    fa.app.run(host='0.0.0.0', debug=True)
