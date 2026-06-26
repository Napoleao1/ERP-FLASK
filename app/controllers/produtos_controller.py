from app.extensions import db
from app.models import Categoria, Produto

def listar_todos_produtos():
    return Produto.query.filter_by(ativo=True).order_by(Produto.id.desc()).all()


def contar_produtos():
    return Produto.query.filter_by(ativo=True).count()


def listar_produtos_paginados(page=1, per_page=10):
    return (
        Produto.query.filter_by(ativo=True)
        .order_by(Produto.id.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )


def obter_produto(produto_id):
    return Produto.query.get_or_404(produto_id)


def salvar_produto(nome, preco, categoria_id, produto_id=None):
    if not nome or not nome.strip():
        return False, "O nome do produto é obrigatório.", None

    if preco <= 0:
        return False, "O preço deve ser maior que zero.", None

    categoria = Categoria.query.get(categoria_id)

    if not categoria:
        return False, "Categoria inválida.", None

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
        return True, mensagem, produto

    except Exception as e:
        db.session.rollback()
        return False, f"Erro interno: {str(e)}", None
    

def excluir_produto(produto_id):
    produto = obter_produto(produto_id)

    try:
        produto.ativo = False
        db.session.commit()

        return True, "Produto excluido com sucesso!"

    except Exception as e:
        db.session.rollback()
        return False, f"Erro ao excluir produto: {str(e)}"