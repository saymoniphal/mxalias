from mxalias.alias import app


def main():
    app.secret_key = app.config['SECRET_KEY']
    app.db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.run(host=app.config['HOST'], port=int(app.config['PORT']), debug=True)


if __name__ == "__main__":
    main()
