from flask_restful import Resource, reqparse
from models import Transferencia, Estoque
from app import db

class TransferResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('produto_id', type=int, required=True)
        parser.add_argument('quantidade', type=int, required=True)
        parser.add_argument('loja_origem_id', type=int, required=True)
        parser.add_argument('loja_destino_id', type=int, required=True)
        args = parser.parse_args()

        transferencia = Transferencia(produto_id=args['produto_id'], quantidade=args['quantidade'], loja_origem_id=args['loja_origem_id'], loja_destino_id=args['loja_destino_id'])
        db.session.add(transferencia)

        estoque_origem = Estoque.query.filter_by(loja_id=args['loja_origem_id'], produto_id=args['produto_id']).first()
        estoque_destino = Estoque.query.filter_by(loja_id=args['loja_destino_id'], produto_id=args['produto_id']).first()

        if estoque_origem and estoque_origem.quantidade >= args['quantidade']:
            estoque_origem.quantidade -= args['quantidade']
            if estoque_destino:
                estoque_destino.quantidade += args['quantidade']
            else:
                estoque_destino = Estoque(loja_id=args['loja_destino_id'], produto_id=args['produto_id'], quantidade=args['quantidade'])
                db.session.add(estoque_destino)
            
            transferencia.status = 'Completa'
            db.session.commit()
            return {'message': 'Transferência realizada com sucesso'}, 200
        else:
            transferencia.status = 'Falhou'
            db.session.commit()
            return {'message': 'Estoque insuficiente na loja de origem'}, 400
