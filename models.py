from app import db

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    preco = db.Column(db.Float, nullable=False)

class Estoque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loja_id = db.Column(db.Integer, nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

class Transferencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    loja_origem_id = db.Column(db.Integer, nullable=False)
    loja_destino_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='Pendente')
