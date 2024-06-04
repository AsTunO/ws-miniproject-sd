from flask_restful import Resource
from utils.sync_utils import sincronizar_dados

class SyncResource(Resource):
    def post(self):
        sincronizar_dados()
        return {'message': 'Sincronização concluída com sucesso'}, 200
