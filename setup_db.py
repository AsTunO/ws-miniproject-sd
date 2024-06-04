from app import create_app, db
from models import Produto, Estoque

app = create_app()

with app.app_context():
    db.create_all()  # Cria todas as tabelas

    # Popula a tabela Produto
    produto1 = Produto(nome='Produto 1', descricao='Descrição do Produto 1', preco=10.0)
    produto2 = Produto(nome='Produto 2', descricao='Descrição do Produto 2', preco=20.0)
    db.session.add(produto1)
    db.session.add(produto2)
    
    # Popula a tabela Estoque
    estoque1 = Estoque(loja_id=1, produto_id=1, quantidade=100)
    estoque2 = Estoque(loja_id=2, produto_id=2, quantidade=200)
    db.session.add(estoque1)
    db.session.add(estoque2)

    db.session.commit()
    print("Banco de dados configurado e populado com sucesso!")
