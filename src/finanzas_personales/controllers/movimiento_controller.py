from datetime import date

from ..models import Movimiento, MovimientoRepositorio
from ..models.movimiento import TIPOS_VALIDOS


class ValidacionError(Exception):
    """Datos de un movimiento inválidos."""


class MovimientoController:
    """Orquesta las operaciones CRUD entre el repositorio y las vistas."""

    def __init__(self, repositorio: MovimientoRepositorio):
        self._repositorio = repositorio

    def listar(self) -> list[Movimiento]:
        return sorted(self._repositorio.listar(), key=lambda m: m.fecha, reverse=True)

    def obtener(self, movimiento_id: str) -> Movimiento | None:
        return self._repositorio.obtener(movimiento_id)

    def crear(self, datos_formulario: dict) -> Movimiento:
        datos = self._validar(datos_formulario)
        movimiento = Movimiento(id="", **datos)
        return self._repositorio.crear(movimiento)

    def actualizar(self, movimiento_id: str, datos_formulario: dict) -> Movimiento:
        if self._repositorio.obtener(movimiento_id) is None:
            raise ValidacionError("El movimiento no existe.")
        datos = self._validar(datos_formulario)
        movimiento = Movimiento(id=movimiento_id, **datos)
        return self._repositorio.actualizar(movimiento)

    def eliminar(self, movimiento_id: str) -> bool:
        return self._repositorio.eliminar(movimiento_id)

    def resumen(self) -> dict:
        movimientos = self._repositorio.listar()
        ingresos = sum(m.monto for m in movimientos if m.tipo == "ingreso")
        gastos = sum(m.monto for m in movimientos if m.tipo == "gasto")
        return {
            "ingresos": ingresos,
            "gastos": gastos,
            "balance": ingresos - gastos,
        }

    def _validar(self, datos_formulario: dict) -> dict:
        descripcion = (datos_formulario.get("descripcion") or "").strip()
        categoria = (datos_formulario.get("categoria") or "").strip()
        tipo = (datos_formulario.get("tipo") or "").strip()
        fecha = (datos_formulario.get("fecha") or "").strip() or date.today().isoformat()
        monto_str = (datos_formulario.get("monto") or "").strip()

        if not descripcion:
            raise ValidacionError("La descripción es obligatoria.")
        if not categoria:
            raise ValidacionError("La categoría es obligatoria.")
        if tipo not in TIPOS_VALIDOS:
            raise ValidacionError(f"El tipo debe ser uno de: {', '.join(TIPOS_VALIDOS)}.")
        try:
            monto = float(monto_str)
        except ValueError:
            raise ValidacionError("El monto debe ser un número.")
        if monto <= 0:
            raise ValidacionError("El monto debe ser mayor que cero.")
        try:
            date.fromisoformat(fecha)
        except ValueError:
            raise ValidacionError("La fecha debe tener el formato AAAA-MM-DD.")

        return {
            "descripcion": descripcion,
            "monto": monto,
            "tipo": tipo,
            "categoria": categoria,
            "fecha": fecha,
        }
