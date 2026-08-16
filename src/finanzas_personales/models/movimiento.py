from dataclasses import dataclass, asdict

TIPOS_VALIDOS = ("ingreso", "gasto")

CATEGORIAS_SUGERIDAS = (
    "trabajo",
    "inversiones pasivas",
    "vivienda",
    "comida",
    "transporte",
    "salud",
    "entretenimiento",
    "ahorro",
    "otros",
)


@dataclass
class Movimiento:
    id: str
    descripcion: str
    monto: float
    tipo: str
    categoria: str
    fecha: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Movimiento":
        return cls(
            id=data["id"],
            descripcion=data["descripcion"],
            monto=float(data["monto"]),
            tipo=data["tipo"],
            categoria=data["categoria"],
            fecha=data["fecha"],
        )
