import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from config import DevelopmentConfig, ProductionConfig, TestingConfig

app = Flask(__name__)


def get_multiple_configs():
    """
    Allows multiple configs.
    If using Powershell, you need to setup FLASK_ENV environment variable like:
        $env:FLASK_ENV = 'prod'
    then you can run from your venv:
        flask --app app run
    """

    current_config = os.environ['FLASK_ENV']

    if current_config == 'dev':
        app.config.from_object(DevelopmentConfig)
    elif current_config == 'test':
        app.config.from_object(TestingConfig)
    elif current_config == 'prod':
        app.config.from_object(ProductionConfig)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config.from_object(get_multiple_configs())
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
