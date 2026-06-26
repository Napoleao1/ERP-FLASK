from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user

from app.controllers import (produtos_controller, categoria_controller, usuarios_controller)


web_bp = Blueprint("web", __name__)

ROTAS_PUBLICAS = {"web.login_view"}


@web_bp.before_request
def exigir_login():
    if request.endpoint in ROTAS_PUBLICAS:
        return
    if not current_user.is_authenticated:
        return redirect(url_for("web.login_view"))


@web_bp.route("/login", methods=["GET", "POST"])
def login_view():
    if current_user.is_authenticated:
        return redirect(url_for("web.dashboard_view"))

    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = usuarios_controller.autenticar(email, senha)

        if usuario:
            login_user(usuario)
            flash(f"Bem-vindo, {usuario.nome}!", "success")
            destino = request.args.get("next")
            return redirect(destino or url_for("web.dashboard_view"))

        flash("E-mail ou senha inválidos.", "danger")

    return render_template("login.html")


@web_bp.route("/logout")
def logout_view():
    logout_user()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("web.login_view"))


@web_bp.route("/")
def dashboard_view():
    total_produtos = produtos_controller.contar_produtos()
    total_categorias = categoria_controller.contar_categorias()
    total_usuarios = usuarios_controller.contar_usuarios()

    return render_template(
        "dashboard.html",
        total_produtos=total_produtos,
        total_categorias=total_categorias,
        total_usuarios=total_usuarios,
    )


@web_bp.route("/produtos")
def listar_produtos_view():
    page = request.args.get("page", 1, type=int)
    paginacao = produtos_controller.listar_produtos_paginados(page=page)
    return render_template("produtos/listar.html", paginacao=paginacao)

@web_bp.route("/produto/novo", methods=["GET", "POST"])
def novo_produto_view():
    categorias = categoria_controller.listar_todas_categorias()

    if request.method == "POST":
        nome = request.form.get("nome")
        preco = float(request.form.get("preco", 0))
        categoria_id = int(request.form.get("categoria_id", 0))

        sucesso, msg, _ = produtos_controller.salvar_produto(nome, preco, categoria_id)
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

        sucesso, msg, _ = produtos_controller.salvar_produto(nome, preco, categoria_id, produto_id = id)

        flash(msg, "success" if sucesso else "danger")

        if sucesso:
            return redirect(url_for("web.listar_produtos_view"))
        
    return render_template("produtos/form.html", produto=produto, categorias=categorias)
        


@web_bp.route("/produtos/excluir/<int:id>", methods=["POST"])
def excluir_produto_view(id):
    sucesso, msg = produtos_controller.excluir_produto(id)
    flash(msg, "success" if sucesso else "danger")
    return redirect(url_for("web.listar_produtos_view"))


@web_bp.route("/categorias")
def listar_categorias_view():
    page = request.args.get("page", 1, type=int)
    paginacao = categoria_controller.listar_categorias_paginadas(page=page)
    return render_template("categorias/listar.html", paginacao=paginacao)
    

@web_bp.route("/categorias/novo", methods=["GET", "POST"])
def nova_categoria_view():
    if request.method == "POST":
        nome = request.form.get("nome_categoria")
        
        sucesso, msg, _ = categoria_controller.salvar_categoria(nome)

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

        sucesso, msg, _ = categoria_controller.salvar_categoria(nome, categoria_id=id)

        flash(msg, "success" if sucesso else "danger")

        if sucesso:
            return redirect(url_for("web.listar_categorias_view"))
    
    return render_template("categorias/form.html", categoria=categoria)


@web_bp.route("/usuarios")
def listar_usuarios_view():
    page = request.args.get("page", 1, type=int)
    paginacao = usuarios_controller.listar_usuarios_paginados(page=page)
    return render_template("usuarios/listar.html", paginacao=paginacao)



@web_bp.route("/usuarios/novo", methods=["GET", "POST"])
def novo_usuario_view():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        
        sucesso, msg, _ = usuarios_controller.salvar_usuario(nome, email, senha)
        
        flash(msg, "success" if sucesso else "danger")
        
        if sucesso:
            return redirect(url_for("web.listar_usuarios_view"))
        
    return render_template("usuarios/form.html", usuario = None)


@web_bp.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
def editar_usuario_view(id):
    usuario = usuarios_controller.obter_usuario(id)
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        
        sucesso, msg, _ = usuarios_controller.salvar_usuario(nome, email, senha, usuario_id=id)
        
        flash(msg, "success" if sucesso else "danger")
        
        if sucesso:
            return redirect(url_for("web.listar_usuarios_view"))
        
    return render_template("usuarios/form.html", usuario = usuario)


@web_bp.route("/usuarios/excluir/<int:id>", methods=["POST"])
def excluir_usuario_view(id):
    sucesso, msg = usuarios_controller.excluir_usuario(id)
    
    flash(msg, "success" if sucesso else "danger")
    return redirect(url_for("web.listar_usuarios_view"))