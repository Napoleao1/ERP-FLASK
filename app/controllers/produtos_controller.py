from app.extensions import db
from app.models import Categoria, Produto

def listar_todos_produtos():
    return Produto.query.order_by(Produto.id.desc()).all()


def obter_produto(produto_id):
    return Produto.query.get_or_404(produto_id)


def salvar_produto(nome, preco, categoria_id, produto_id=None):
    if not nome or not nome.strip():
        return False, "O nome do produto é obrigatório."
    
    if preco <= 0:
        return False, "O preço deve ser maior que zero."
    
    categoria = Categoria.query.get(categoria_id)

    if not categoria:
        return False, "Categoria inválida."
    
    try:

        if produto_id:
            produto = obter_produto(produto_id)
            produto.nome = nome.strip()
            produto.preco = preco
            produto.categoria_id = categoria_id

            mensagem = "Produto atualizado com sucesso!"
        
        else:
            produto = Produto(nome=nome.strip(), preco=preco, categoria_id=categoria.id)
            db.session.add(produto)
            mensagem = "Produto cadastrado com sucesso!"

        db.session.commit()
        return True, mensagem

    except Exception as e:
        db.session.rollback()
        return False, f"Erro interno: {str(e)}"
    

def excluir_produto(produto_id):
    produto = obter_produto(produto_id)

    try:
        db.session.delete(produto)
        db.session.commit()

        return True, "Produto excluido com sucesso!"

    except Exception as e:
        db.session.rollback()
        return False, f"Erro ao excluir produto: {str(e)}"