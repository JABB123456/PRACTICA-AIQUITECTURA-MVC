import json
import uuid
from pathlib import Path

from .movimiento import Movimiento


class MovimientoRepositorio:
    """Persiste movimientos financieros en un archivo JSON plano (sin base de datos)."""

    def __init__(self, ruta_archivo: Path):
        self._ruta = ruta_archivo
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        if not self._ruta.exists():
            self._escribir([])

    def _leer(self) -> list[dict]:
        with self._ruta.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _escribir(self, datos: list[dict]) -> None:
        with self._ruta.open("w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    def listar(self) -> list[Movimiento]:
        return [Movimiento.from_dict(d) for d in self._leer()]

    def obtener(self, movimiento_id: str) -> Movimiento | None:
        for d in self._leer():
            if d["id"] == movimiento_id:
                return Movimiento.from_dict(d)
        return None

    def crear(self, movimiento: Movimiento) -> Movimiento:
        movimiento.id = str(uuid.uuid4())
        datos = self._leer()
        datos.append(movimiento.to_dict())
        self._escribir(datos)
        return movimiento

    def actualizar(self, movimiento: Movimiento) -> Movimiento | None:
        datos = self._leer()
        for i, d in enumerate(datos):
            if d["id"] == movimiento.id:
                datos[i] = movimiento.to_dict()
                self._escribir(datos)
                return movimiento
        return None

    def eliminar(self, movimiento_id: str) -> bool:
        datos = self._leer()
        nuevos_datos = [d for d in datos if d["id"] != movimiento_id]
        if len(nuevos_datos) == len(datos):
            return False
        self._escribir(nuevos_datos)
        return True
