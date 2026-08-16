import json
import tempfile
import unittest
from pathlib import Path

from finanzas_personales.app import create_app


class TestCrudMovimientos(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        ruta_datos = Path(self._tmpdir.name) / "movimientos.json"
        self.app = create_app(ruta_datos)
        self.ruta_datos = ruta_datos
        self.client = self.app.test_client()

    def tearDown(self):
        self._tmpdir.cleanup()

    def _leer_datos(self):
        return json.loads(self.ruta_datos.read_text(encoding="utf-8"))

    def test_index_vacio(self):
        respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)

    def test_crear_movimiento_valido(self):
        respuesta = self.client.post(
            "/movimientos/nuevo",
            data={
                "descripcion": "Salario",
                "monto": "1500",
                "tipo": "ingreso",
                "categoria": "trabajo",
                "fecha": "2026-08-01",
            },
            follow_redirects=True,
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(b"Salario", respuesta.data)
        self.assertEqual(len(self._leer_datos()), 1)

    def test_crear_movimiento_invalido(self):
        respuesta = self.client.post(
            "/movimientos/nuevo",
            data={"descripcion": "", "monto": "abc", "tipo": "x", "categoria": ""},
        )
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(len(self._leer_datos()), 0)

    def test_actualizar_movimiento(self):
        self.client.post(
            "/movimientos/nuevo",
            data={
                "descripcion": "Salario",
                "monto": "1500",
                "tipo": "ingreso",
                "categoria": "trabajo",
                "fecha": "2026-08-01",
            },
        )
        movimiento_id = self._leer_datos()[0]["id"]

        respuesta = self.client.post(
            f"/movimientos/{movimiento_id}/editar",
            data={
                "descripcion": "Salario ajustado",
                "monto": "1600",
                "tipo": "ingreso",
                "categoria": "trabajo",
                "fecha": "2026-08-01",
            },
            follow_redirects=True,
        )
        self.assertIn(b"Salario ajustado", respuesta.data)

    def test_eliminar_movimiento(self):
        self.client.post(
            "/movimientos/nuevo",
            data={
                "descripcion": "Salario",
                "monto": "1500",
                "tipo": "ingreso",
                "categoria": "trabajo",
                "fecha": "2026-08-01",
            },
        )
        movimiento_id = self._leer_datos()[0]["id"]

        self.client.post(f"/movimientos/{movimiento_id}/eliminar")
        self.assertEqual(len(self._leer_datos()), 0)

    def test_resumen_calcula_balance(self):
        self.client.post(
            "/movimientos/nuevo",
            data={"descripcion": "Salario", "monto": "1000", "tipo": "ingreso", "categoria": "trabajo", "fecha": "2026-08-01"},
        )
        self.client.post(
            "/movimientos/nuevo",
            data={"descripcion": "Renta", "monto": "400", "tipo": "gasto", "categoria": "vivienda", "fecha": "2026-08-02"},
        )
        controller = self.app.config["MOVIMIENTO_CONTROLLER"]
        resumen = controller.resumen()
        self.assertEqual(resumen["ingresos"], 1000)
        self.assertEqual(resumen["gastos"], 400)
        self.assertEqual(resumen["balance"], 600)


if __name__ == "__main__":
    unittest.main()
