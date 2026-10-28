from .database import SessionLocal
from .models import Hotel, Habitacion

HOTELES = [
    {
        "nombre": "Hotel Barranquilla",
        "ubicacion": "Barranquilla",
        "cupo_max": 4,
        "habitaciones": [
            {"tipo": "estandar", "tarifa_base": 150, "cantidad": 30},
            {"tipo": "premium",  "tarifa_base": 280, "cantidad": 3},
        ],
    },
    {
        "nombre": "Hotel Cali",
        "ubicacion": "Cali",
        "cupo_max": 6,
        "habitaciones": [
            {"tipo": "premium", "tarifa_base": 280, "cantidad": 20},
            {"tipo": "vip",     "tarifa_base": 500, "cantidad": 2},
        ],
    },
    {
        "nombre": "Hotel Cartagena",
        "ubicacion": "Cartagena",
        "cupo_max": 8,
        "habitaciones": [
            {"tipo": "estandar", "tarifa_base": 150, "cantidad": 10},
            {"tipo": "premium",  "tarifa_base": 280, "cantidad": 1},
        ],
    },
    {
        "nombre": "Hotel Bogota",
        "ubicacion": "Bogota",
        "cupo_max": 6,
        "habitaciones": [
            {"tipo": "estandar", "tarifa_base": 150, "cantidad": 20},
            {"tipo": "premium",  "tarifa_base": 280, "cantidad": 20},
            {"tipo": "vip",      "tarifa_base": 500, "cantidad": 2},
        ],
    },
]


def seed():
    db = SessionLocal()
    try:
        if db.query(Hotel).count() > 0:
            return
        for data in HOTELES:
            hotel = Hotel(
                nombre=data["nombre"],
                ubicacion=data["ubicacion"],
                cupo_max=data["cupo_max"],
            )
            db.add(hotel)
            db.flush()
            for h in data["habitaciones"]:
                db.add(Habitacion(
                    hotel_id=hotel.id,
                    tipo=h["tipo"],
                    tarifa_base=h["tarifa_base"],
                    cantidad=h["cantidad"],
                ))
        db.commit()
    finally:
        db.close()
