from pydantic import BaseModel
from typing import List


class HabitacionSimple(BaseModel):
    id: int
    tipo: str
    tarifa_base: float
    cantidad: int

    class Config:
        from_attributes = True


class HotelSimple(BaseModel):
    id: int
    nombre: str
    ubicacion: str
    cupo_max: int
    habitaciones: List[HabitacionSimple] = []

    class Config:
        from_attributes = True


class HabitacionOut(BaseModel):
    id: int
    tipo: str
    tarifa_base: float
    cantidad: int
    disponibles: int
    tarifa_temporada: float

    class Config:
        from_attributes = True


class HotelOut(BaseModel):
    id: int
    nombre: str
    ubicacion: str
    cupo_max: int
    habitaciones: List[HabitacionOut] = []

    class Config:
        from_attributes = True


class BusquedaIn(BaseModel):
    fecha_entrada: str   # YYYY-MM-DD
    fecha_salida: str    # YYYY-MM-DD
    num_personas: int


class ReservaIn(BaseModel):
    habitacion_id: int
    fecha_entrada: str
    fecha_salida: str
    num_personas: int


class ReservaOut(BaseModel):
    id: int
    habitacion_id: int
    fecha_entrada: str
    fecha_salida: str
    num_personas: int
    tarifa_total: float

    class Config:
        from_attributes = True
