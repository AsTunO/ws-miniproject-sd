from flask_restful import Resource, reqparse
from models import Estoque
from app import db, mongo

class StockResource(Resource):
    def get(self, produto_id):
        estoques = Estoque.query.filter_by(produto_id=produto_id).all()
        response = [{'loja_id': estoque.loja_id, 'quantidade': estoque.quantidade} for estoque in estoques]
        
        # Sincronizar dados offline do MongoDB se existirem
        offline_estoques = mongo.db.estoques_offline.find({'produto_id': produto_id})
        for offline_estoque in offline_estoques:
            response.append({'loja_id': offline_estoque['loja_id'], 'quantidade': offline_estoque['quantidade']})
        
        return response, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('loja_id', type=int, required=True)
        parser.add_argument('produto_id', type=int, required=True)
        parser.add_argument('quantidade', type=int, required=True)
        args = parser.parse_args()

        estoque = Estoque.query.filter_by(loja_id=args['loja_id'], produto_id=args['produto_id']).first()
        if estoque:
            estoque.quantidade = args['quantidade']
        else:
            estoque = Estoque(loja_id=args['loja_id'], produto_id=args['produto_id'], quantidade=args['quantidade'])
            db.session.add(estoque)

        db.session.commit()
        return {'message': 'Estoque atualizado com sucesso'}, 200
