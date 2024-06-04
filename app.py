from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_pymongo import PyMongo
from config import Config

db = SQLAlchemy()
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    mongo.init_app(app)
    api = Api(app)

    from resources.stock import StockResource
    from resources.transfer import TransferResource
    from resources.sync import SyncResource

    api.add_resource(StockResource, '/estoque/<int:produto_id>')
    api.add_resource(TransferResource, '/transferencia')
    api.add_resource(SyncResource, '/sync')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
