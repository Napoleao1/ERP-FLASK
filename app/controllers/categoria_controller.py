from app.extensions import db
from app.models import Categoria

def listar_todas_categorias():
    return Categoria.query.order_by(Categoria.id.desc()).all()


def obter_categoria(categoria_id):
    return Categoria.query.get_or_404(categoria_id)


def salvar_categoria(nome, categoria_id=None):
    if not nome or not nome.strip():
        return False, "O nome da categoria é obrigatório."
    
    try:
        if categoria_id:
            categoria = obter_categoria(categoria_id)
            categoria.nome = nome.strip()
            mensagem = "Categoria atualizada com sucesso!"
        else:
            categoria = Categoria(nome=nome.strip())
            db.session.add(categoria)
            mensagem = "Categoria adicionada com sucesso!"
        
        db.session.commit()
        return True, mensagem

    except Exception as e:
        db.session.rollback()
        return False, f"Erro interno: {str(e)}"
    
def excluir_categoria(categoria_id):
    categoria = obter_categoria(categoria_id)

    if categoria.produtos:
        return False, "Não é possivel excluir uma categoria que possui produtos vinculados"
    
    try:
        db.session.delete(categoria)
        db.session.commit()
        return True, "Categoria excluida com sucesso!"
    except Exception as e :
        db.session.rollback()
        return False, f"Erro ao excluir categoria: {str(e)}"
    