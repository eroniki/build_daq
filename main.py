from app import flask_app


def main():
    fa = flask_app("asda")
    fa.app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
