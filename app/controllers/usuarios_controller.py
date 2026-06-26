from sqlalchemy.exc import IntegrityError


from app.extensions import db
from app.models import Usuario

def listar_todos_usuarios():
    return Usuario.query.filter_by(ativo=True).order_by(Usuario.id.desc()).all()


def contar_usuarios():
    return Usuario.query.filter_by(ativo=True).count()


def listar_usuarios_paginados(page=1, per_page=10):
    return (
        Usuario.query.filter_by(ativo=True)
        .order_by(Usuario.id.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )


def obter_usuario(usuario_id):
    return Usuario.query.get_or_404(usuario_id)


def autenticar(email, senha):
    if not email or not senha:
        return None
    usuario = Usuario.query.filter_by(email=email, ativo=True).first()
    if usuario and usuario.checar_senha(senha):
        return usuario
    return None


def salvar_usuario(nome, email, senha=None, usuario_id=None):
    if not nome or not email:
        return False, "Nome e E-mail são campos obrigatórios.", None

    try:
        if usuario_id:
            usuario = obter_usuario(usuario_id)
            usuario.nome = nome
            usuario.email = email

            if senha and senha.strip():
                usuario.set_senha(senha)

            mensagem = "Usuário atualizado com sucesso!"
        else:
            if not senha:
                return False, "A senha é obrigatória para novos usuários.", None

            usuario = Usuario(nome=nome, email=email)
            usuario.set_senha(senha)
            db.session.add(usuario)
            mensagem = "Usuário cadastrado com sucesso!"

        db.session.commit()
        return True, mensagem, usuario

    except IntegrityError:
        db.session.rollback()
        return False, "Erro: Este e-mail já está cadastrado.", None

    except Exception as e:
        db.session.rollback()
        return False, f"Erro interno: {str(e)}", None


def excluir_usuario(usuario_id):
    usuario = obter_usuario(usuario_id)
    try:
        usuario.ativo = False
        db.session.commit()
        return True, "Usuário excluído com sucesso!"
    except Exception as e:
        db.session.rollback()
        return False, f"Erro ao excluir usuário: {str(e)}"
