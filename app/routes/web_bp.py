from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.controllers import (produtos_controller, categoria_controller)

web_bp = Blueprint("web", __name__)

@web_bp.route("/")
def index():
    return redirect(url_for("web.listar_produtos_view"))

# ROTAS DE PRODUTOS

@web_bp.route("/produtos")
def listar_produtos_view():
    produtos = produtos_controller.listar_todos_produtos()
    return render_template("produtos/listar.html", produtos=produtos)

@web_bp.route("/produto/novo", methods=["GET", "POST"])
def novo_produto_view():
    categorias = categoria_controller.listar_todas_categorias()

    if request.method == "POST":
        nome = request.form.get("nome")
        preco = float(request.form.get("preco", 0))
        categoria_id = int(request.form.get("categoria_id", 0))

        sucesso, msg = produtos_controller.salvar_produto(nome, preco, categoria_id)
        flash(msg, "success" if sucesso else "danger")

        if sucesso:
            return redirect(url_for("web.listar_produtos_view"))
        
    return render_template("produtos/form.html", produto=None, categorias=categorias)

@web_bp.route("/produtos/editar/<int:id>", methods=["GET", "POST"])
def editar_produto_view(id):
    produto = produtos_controller.obter_produto(id)
    categorias = categoria_controller.listar_todas_categorias()

    if request.method == "POST":
        nome = request.form.get("nome")
        preco = float(request.form.get("preco", 0))
        categoria_id = int(request.form.get("categoria_id", 0))

        sucesso, msg = produtos_controller.salvar_produto(nome, preco, categoria_id, produto_id = id)

        flash(msg, "success" if sucesso else "danger")

        if sucesso:
            return redirect(url_for("web.listar_produtos_view"))
        
    return render_template("produtos/form.html", produto=produto, categorias=categorias)
        


@web_bp.route("/produtos/excluir/<int:id>", methods=["POST"])
def excluir_produto_view(id):
    sucesso, msg = produtos_controller.excluir_produto(id)
    flash(msg, "success" if sucesso else "danger")
    return redirect(url_for("web.listar_produtos_view"))


# ROTAS DE CATEGORIAS

@web_bp.route("/categorias")
def listar_categorias_view():
    categorias = categoria_controller.listar_todas_categorias()
    return render_template("categorias/listar.html", categorias=categorias)
    

@web_bp.route("/categorias/novo", methods=["GET", "POST"])
def nova_categoria_view():
    if request.method == "POST":
        nome = request.form.get("nome_categoria")
        
        sucesso, msg = categoria_controller.salvar_categoria(nome)

        flash(msg, "success" if sucesso else "danger")

        if sucesso:
            return redirect(url_for('web.listar_categorias_view'))

    return render_template("categorias/form.html", categoria=None)


@web_bp.route("/categorias/excluir/<int:id>", methods=["POST"])
def excluir_categoria_view(id):
    sucesso, msg = categoria_controller.excluir_categoria(id)
    flash(msg, "success" if sucesso else "danger")
    return redirect(url_for("web.listar_categorias_view"))


@web_bp.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
def editar_categoria_view(id):
    categoria = categoria_controller.obter_categoria(id)

    if request.method == "POST":
        nome = request.form.get("nome_categoria")

        sucesso, msg = categoria_controller.salvar_categoria(nome, categoria_id=id)

        flash(msg, "success" if sucesso else "danger")

        if sucesso:
            return redirect(url_for("web.listar_categorias_view"))
    
    return render_template("categorias/form.html", categoria=categoria)