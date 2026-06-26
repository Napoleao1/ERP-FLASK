from flask import Blueprint, jsonify, request

from app.controllers import (
    categoria_controller,
    produtos_controller,
    usuarios_controller,
)


api_bp = Blueprint('api', __name__, url_prefix="/api")


def _coagir(valor, conversor, campo):
    """Converte ``valor`` usando ``conversor`` (int/float).

    Retorna ``(ok, resultado_ou_mensagem)``. Em caso de falha, a mensagem
    aponta qual campo está com o tipo errado.
    """
    if valor is None:
        return True, None
    try:
        return True, conversor(valor)
    except (TypeError, ValueError):
        return False, f"O campo '{campo}' tem um valor inválido."


@api_bp.route("/produto", methods=["GET"])
def get_produto():
    """
    Lista os produtos ativos
    ---
    tags:
      - Produtos
    responses:
      200:
        description: Lista de produtos ativos
        schema:
          type: array
          items:
            type: object
    """
    produtos = produtos_controller.listar_todos_produtos()
    return jsonify([produto.to_dict() for produto in produtos]), 200


@api_bp.route("/produto/<int:id>", methods=["GET"])
def get_produto_por_id(id):
    """
    Busca um produto pelo ID
    ---
    tags:
      - Produtos
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do produto
    responses:
      200:
        description: Produto encontrado
      404:
        description: Produto não encontrado
    """
    produto = produtos_controller.obter_produto(id)
    return jsonify(produto.to_dict()), 200


@api_bp.route("/produto", methods=["POST"])
def criar_produto():
    """
    Cria um novo produto
    ---
    tags:
      - Produtos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome
            - preco
            - categoria_id
          properties:
            nome:
              type: string
              example: Notebook
            preco:
              type: number
              example: 2500.00
            categoria_id:
              type: integer
              example: 1
    responses:
      201:
        description: Produto criado com sucesso
      400:
        description: Dados inválidos
    """
    dados = request.get_json(silent=True) or {}

    ok, preco = _coagir(dados.get("preco"), float, "preco")
    if not ok:
        return jsonify({"erro": preco}), 400

    ok, categoria_id = _coagir(dados.get("categoria_id"), int, "categoria_id")
    if not ok:
        return jsonify({"erro": categoria_id}), 400

    sucesso, msg, produto = produtos_controller.salvar_produto(
        dados.get("nome"), preco or 0, categoria_id
    )

    if sucesso:
        return jsonify({"mensagem": msg, "produto": produto.to_dict()}), 201
    return jsonify({"erro": msg}), 400


@api_bp.route("/produto/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    """
    Atualiza um produto existente
    ---
    tags:
      - Produtos
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do produto
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: Notebook Gamer
            preco:
              type: number
              example: 3200.00
            categoria_id:
              type: integer
              example: 1
    responses:
      200:
        description: Produto atualizado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Produto não encontrado
    """
    dados = request.get_json(silent=True) or {}

    ok, preco = _coagir(dados.get("preco"), float, "preco")
    if not ok:
        return jsonify({"erro": preco}), 400

    ok, categoria_id = _coagir(dados.get("categoria_id"), int, "categoria_id")
    if not ok:
        return jsonify({"erro": categoria_id}), 400

    sucesso, msg, produto = produtos_controller.salvar_produto(
        dados.get("nome"), preco or 0, categoria_id, produto_id=id
    )

    if sucesso:
        return jsonify({"mensagem": msg, "produto": produto.to_dict()}), 200
    return jsonify({"erro": msg}), 400


@api_bp.route("/produto/<int:id>", methods=["DELETE"])
def deletar_produto(id):
    """
    Exclui (desativa) um produto
    ---
    tags:
      - Produtos
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do produto
    responses:
      200:
        description: Produto excluído com sucesso
      404:
        description: Produto não encontrado
    """
    sucesso, msg = produtos_controller.excluir_produto(id)
    if sucesso:
        return jsonify({"mensagem": msg}), 200
    return jsonify({"erro": msg}), 400


@api_bp.route("/categorias", methods=["GET"])
def get_categorias():
    """
    Lista as categorias ativas
    ---
    tags:
      - Categorias
    responses:
      200:
        description: Lista de categorias ativas
        schema:
          type: array
          items:
            type: object
    """
    categorias = categoria_controller.listar_todas_categorias()
    return jsonify([categoria.to_dict() for categoria in categorias]), 200


@api_bp.route("/categorias/<int:id>", methods=["GET"])
def get_categoria_por_id(id):
    """
    Busca uma categoria pelo ID
    ---
    tags:
      - Categorias
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da categoria
    responses:
      200:
        description: Categoria encontrada
      404:
        description: Categoria não encontrada
    """
    categoria = categoria_controller.obter_categoria(id)
    return jsonify(categoria.to_dict()), 200


@api_bp.route("/categorias", methods=["POST"])
def criar_categoria():
    """
    Cria uma nova categoria
    ---
    tags:
      - Categorias
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              example: Eletrônicos
    responses:
      201:
        description: Categoria criada com sucesso
      400:
        description: Dados inválidos
    """
    dados = request.get_json(silent=True) or {}
    sucesso, msg, categoria = categoria_controller.salvar_categoria(dados.get("nome"))

    if sucesso:
        return jsonify({"mensagem": msg, "categoria": categoria.to_dict()}), 201
    return jsonify({"erro": msg}), 400


@api_bp.route("/categorias/<int:id>", methods=["PUT"])
def atualizar_categoria(id):
    """
    Atualiza uma categoria existente
    ---
    tags:
      - Categorias
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da categoria
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              example: Eletrodomésticos
    responses:
      200:
        description: Categoria atualizada com sucesso
      400:
        description: Dados inválidos
      404:
        description: Categoria não encontrada
    """
    dados = request.get_json(silent=True) or {}
    sucesso, msg, categoria = categoria_controller.salvar_categoria(
        dados.get("nome"), categoria_id=id
    )

    if sucesso:
        return jsonify({"mensagem": msg, "categoria": categoria.to_dict()}), 200
    return jsonify({"erro": msg}), 400


@api_bp.route("/categorias/<int:id>", methods=["DELETE"])
def deletar_categoria(id):
    """
    Exclui (desativa) uma categoria
    ---
    tags:
      - Categorias
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID da categoria
    responses:
      200:
        description: Categoria excluída com sucesso
      400:
        description: Categoria possui produtos vinculados
      404:
        description: Categoria não encontrada
    """
    sucesso, msg = categoria_controller.excluir_categoria(id)
    if sucesso:
        return jsonify({"mensagem": msg}), 200
    return jsonify({"erro": msg}), 400


@api_bp.route("/usuarios", methods=["GET"])
def get_usuarios():
    """
    Lista os usuários ativos
    ---
    tags:
      - Usuários
    responses:
      200:
        description: Lista de usuários ativos
        schema:
          type: array
          items:
            type: object
    """
    usuarios = usuarios_controller.listar_todos_usuarios()
    return jsonify([usuario.to_dict() for usuario in usuarios]), 200


@api_bp.route("/usuarios/<int:id>", methods=["GET"])
def get_usuario_por_id(id):
    """
    Busca um usuário pelo ID
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do usuário
    responses:
      200:
        description: Usuário encontrado
      404:
        description: Usuário não encontrado
    """
    usuario = usuarios_controller.obter_usuario(id)
    return jsonify(usuario.to_dict()), 200


@api_bp.route("/usuarios", methods=["POST"])
def criar_usuario():
    """
    Cria um novo usuário
    ---
    tags:
      - Usuários
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome
            - email
            - senha
          properties:
            nome:
              type: string
              example: João da Silva
            email:
              type: string
              example: joao@email.com
            senha:
              type: string
              example: senha123
    responses:
      201:
        description: Usuário criado com sucesso
      400:
        description: Dados inválidos ou e-mail já cadastrado
    """
    dados = request.get_json(silent=True) or {}
    sucesso, msg, usuario = usuarios_controller.salvar_usuario(
        dados.get("nome"), dados.get("email"), dados.get("senha")
    )

    if sucesso:
        return jsonify({"mensagem": msg, "usuario": usuario.to_dict()}), 201
    return jsonify({"erro": msg}), 400


@api_bp.route("/usuarios/<int:id>", methods=["PUT"])
def atualizar_usuario(id):
    """
    Atualiza um usuário existente
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do usuário
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: João da Silva
            email:
              type: string
              example: joao@email.com
            senha:
              type: string
              description: Opcional. Informe apenas para trocar a senha.
              example: novaSenha123
    responses:
      200:
        description: Usuário atualizado com sucesso
      400:
        description: Dados inválidos ou e-mail já cadastrado
      404:
        description: Usuário não encontrado
    """
    dados = request.get_json(silent=True) or {}
    sucesso, msg, usuario = usuarios_controller.salvar_usuario(
        dados.get("nome"), dados.get("email"), dados.get("senha"), usuario_id=id
    )

    if sucesso:
        return jsonify({"mensagem": msg, "usuario": usuario.to_dict()}), 200
    return jsonify({"erro": msg}), 400


@api_bp.route("/usuarios/<int:id>", methods=["DELETE"])
def deletar_usuario(id):
    """
    Exclui (desativa) um usuário
    ---
    tags:
      - Usuários
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do usuário
    responses:
      200:
        description: Usuário excluído com sucesso
      404:
        description: Usuário não encontrado
    """
    sucesso, msg = usuarios_controller.excluir_usuario(id)
    if sucesso:
        return jsonify({"mensagem": msg}), 200
    return jsonify({"erro": msg}), 400
