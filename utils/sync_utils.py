from app import mongo, db
from models import Estoque

def sincronizar_dados():
    estoques_offline = mongo.db.estoques_offline.find()
    for item in estoques_offline:
        estoque = Estoque.query.filter_by(loja_id=item['loja_id'], produto_id=item['produto_id']).first()
        if estoque:
            estoque.quantidade = item['quantidade']
        else:
            estoque = Estoque(loja_id=item['loja_id'], produto_id=item['produto_id'], quantidade=item['quantidade'])
            db.session.add(estoque)
        
        db.session.commit()
        mongo.db.estoques_offline.delete_one({'_id': item['_id']})
