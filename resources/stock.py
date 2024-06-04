from flask_restful import Resource, reqparse
from models import Estoque
from app import create_app, db

class StockResource(Resource):
    def get(self, produto_id=None):
        app = create_app()  # Importe o create_app aqui para evitar importações circulares

        with app.app_context():  # Garanta que você está dentro do contexto do aplicativo Flask
            if produto_id:
                estoque = Estoque.query.filter_by(produto_id=produto_id).first()
                if estoque:
                    return {'loja_id': estoque.loja_id, 'quantidade': estoque.quantidade}, 200
                else:
                    return {'message': 'Produto não encontrado'}, 404
            else:
                estoques = Estoque.query.all()
                response = [{'loja_id': estoque.loja_id, 'produto_id': estoque.produto_id, 'quantidade': estoque.quantidade} for estoque in estoques]
                return response, 200

    def post(self):
        app = create_app()  # Importe o create_app aqui para evitar importações circulares

        with app.app_context():  # Garanta que você está dentro do contexto do aplicativo Flask
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
