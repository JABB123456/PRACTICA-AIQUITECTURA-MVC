from pathlib import Path

from flask import Flask

from .controllers import MovimientoController
from .models import MovimientoRepositorio
from .views import movimientos_bp

RUTA_DATOS_POR_DEFECTO = Path(__file__).resolve().parent.parent.parent / "data" / "movimientos.json"


def create_app(ruta_datos: Path = RUTA_DATOS_POR_DEFECTO) -> Flask:
    app = Flask(__name__)
    app.secret_key = "clave-de-desarrollo-finanzas-personales"

    repositorio = MovimientoRepositorio(ruta_datos)
    app.config["MOVIMIENTO_CONTROLLER"] = MovimientoController(repositorio)

    app.register_blueprint(movimientos_bp)

    return app
