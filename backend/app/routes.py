from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from .database import get_db
from .models import Hotel, Habitacion, Reserva
from .schemas import BusquedaIn, HotelOut, HotelSimple, HabitacionOut, ReservaIn, ReservaOut

router = APIRouter()

MESES_ALTA = {2, 4, 7, 8, 12}

MULTIPLICADOR = {
    "alta":  {"estandar": 1.5, "premium": 2.0, "vip": 3.0},
    "baja":  {"estandar": 1.0, "premium": 1.0, "vip": 1.0},
}


def get_temporada(fecha: str) -> str:
    mes = date.fromisoformat(fecha).month
    return "alta" if mes in MESES_ALTA else "baja"


def habitaciones_ocupadas(db: Session, habitacion_id: int, fecha_entrada: str, fecha_salida: str) -> int:
    return db.query(Reserva).filter(
        Reserva.habitacion_id == habitacion_id,
        Reserva.fecha_entrada < fecha_salida,
        Reserva.fecha_salida > fecha_entrada,
    ).count()


@router.get("/hoteles", response_model=list[HotelSimple])
def listar_hoteles(db: Session = Depends(get_db)):
    return db.query(Hotel).filter(Hotel.activo == True).all()


@router.post("/buscar", response_model=list[HotelOut])
def buscar_disponibilidad(busqueda: BusquedaIn, db: Session = Depends(get_db)):
    temporada = get_temporada(busqueda.fecha_entrada)
    hoteles = db.query(Hotel).filter(Hotel.activo == True).all()

    resultado = []
    for hotel in hoteles:
        if hotel.cupo_max < busqueda.num_personas:
            continue

        habitaciones_disponibles = []
        for hab in hotel.habitaciones:
            ocupadas = habitaciones_ocupadas(db, hab.id, busqueda.fecha_entrada, busqueda.fecha_salida)
            disponibles = hab.cantidad - ocupadas
            if disponibles <= 0:
                continue
            factor = MULTIPLICADOR[temporada][hab.tipo]
            hab_out = HabitacionOut(
                id=hab.id,
                tipo=hab.tipo,
                tarifa_base=hab.tarifa_base,
                cantidad=hab.cantidad,
                disponibles=disponibles,
                tarifa_temporada=round(hab.tarifa_base * factor, 2),
            )
            habitaciones_disponibles.append(hab_out)

        if habitaciones_disponibles:
            resultado.append(HotelOut(
                id=hotel.id,
                nombre=hotel.nombre,
                ubicacion=hotel.ubicacion,
                cupo_max=hotel.cupo_max,
                habitaciones=habitaciones_disponibles,
            ))

    return resultado


@router.post("/reservas", response_model=ReservaOut)
def crear_reserva(reserva: ReservaIn, db: Session = Depends(get_db)):
    hab = db.query(Habitacion).filter(Habitacion.id == reserva.habitacion_id).first()
    if not hab:
        raise HTTPException(status_code=404, detail="Habitacion no encontrada")

    if hab.hotel.cupo_max < reserva.num_personas:
        raise HTTPException(status_code=400, detail="El numero de personas supera el cupo maximo")

    ocupadas = habitaciones_ocupadas(db, hab.id, reserva.fecha_entrada, reserva.fecha_salida)
    if ocupadas >= hab.cantidad:
        raise HTTPException(status_code=400, detail="Sin disponibilidad para esas fechas")

    temporada = get_temporada(reserva.fecha_entrada)
    factor = MULTIPLICADOR[temporada][hab.tipo]
    dias = (date.fromisoformat(reserva.fecha_salida) - date.fromisoformat(reserva.fecha_entrada)).days
    tarifa_total = round(hab.tarifa_base * factor * dias, 2)

    nueva_reserva = Reserva(
        habitacion_id=reserva.habitacion_id,
        fecha_entrada=reserva.fecha_entrada,
        fecha_salida=reserva.fecha_salida,
        num_personas=reserva.num_personas,
        tarifa_total=tarifa_total,
    )
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    return nueva_reserva
