from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from ..controllers.movimiento_controller import ValidacionError
from ..models.movimiento import TIPOS_VALIDOS

bp = Blueprint("movimientos", __name__)


def _controller():
    return current_app.config["MOVIMIENTO_CONTROLLER"]


@bp.get("/")
def index():
    movimientos = _controller().listar()
    resumen = _controller().resumen()
    return render_template("index.html", movimientos=movimientos, resumen=resumen)


@bp.get("/movimientos/nuevo")
def nuevo():
    return render_template("formulario.html", movimiento=None, tipos=TIPOS_VALIDOS)


@bp.post("/movimientos/nuevo")
def crear():
    try:
        _controller().crear(request.form)
        flash("Movimiento creado correctamente.", "exito")
        return redirect(url_for("movimientos.index"))
    except ValidacionError as e:
        flash(str(e), "error")
        return render_template("formulario.html", movimiento=request.form, tipos=TIPOS_VALIDOS), 400


@bp.get("/movimientos/<movimiento_id>/editar")
def editar(movimiento_id):
    movimiento = _controller().obtener(movimiento_id)
    if movimiento is None:
        flash("El movimiento no existe.", "error")
        return redirect(url_for("movimientos.index"))
    return render_template("formulario.html", movimiento=movimiento, tipos=TIPOS_VALIDOS)


@bp.post("/movimientos/<movimiento_id>/editar")
def actualizar(movimiento_id):
    try:
        _controller().actualizar(movimiento_id, request.form)
        flash("Movimiento actualizado correctamente.", "exito")
        return redirect(url_for("movimientos.index"))
    except ValidacionError as e:
        flash(str(e), "error")
        return render_template("formulario.html", movimiento=request.form, tipos=TIPOS_VALIDOS), 400


@bp.post("/movimientos/<movimiento_id>/eliminar")
def eliminar(movimiento_id):
    if _controller().eliminar(movimiento_id):
        flash("Movimiento eliminado.", "exito")
    else:
        flash("El movimiento no existe.", "error")
    return redirect(url_for("movimientos.index"))
