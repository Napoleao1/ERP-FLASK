from app.extensions import db
from app.models import Categoria, Produto


def listar_todos_produtos():
    return Produto.query.order_by(Produto.id.desc()).all()