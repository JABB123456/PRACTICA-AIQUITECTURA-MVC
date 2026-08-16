# PRACTICA-AIQUITECTURA-MVC
CREANANDO UN REPOSITORIO CON ARQUITECTURA MVC

## Finanzas Personales

Aplicación web (Flask) con arquitectura MVC para llevar el control de movimientos
financieros personales (ingresos y gastos) mediante operaciones CRUD. No usa base
de datos: los datos se persisten en un archivo JSON plano (`data/movimientos.json`).

Gestión de dependencias con [uv](https://docs.astral.sh/uv/).

### Estructura (MVC)

```
src/finanzas_personales/
  models/       # Movimiento (entidad) + MovimientoRepositorio (persistencia JSON)
  controllers/  # MovimientoController (validación y orquestación CRUD)
  views/        # Blueprint de Flask (rutas) + templates/ y static/
  app.py        # Application factory
```

### Uso

```bash
uv sync
uv run finanzas-personales
```

La app queda disponible en http://127.0.0.1:5000

### Tests

```bash
uv run python -m unittest discover -s tests
```
