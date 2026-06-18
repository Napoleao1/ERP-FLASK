from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.controllers import(produtos_controller)

web_bp = Blueprint("web", __name__)

@web_bp.route("/")
def index():
    return redirect(url_for("web.listar_produtos_view"))



@web_bp.route("/produtos")
def listar_produtos_view():
    produtos = produtos_controller.listar_todos_produtos()
    return render_template("produtos/listar.html", produtos=produtos)