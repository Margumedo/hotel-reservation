from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

from .database import Base

class Hotel(Base):
    __tablename__ = "hoteles"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    ubicacion = Column(String, nullable=False)
    cupo_max = Column(Integer, nullable=False)  # cupo máximo por habitación
    activo = Column(Boolean, default=True)
    habitaciones = relationship("Habitacion", back_populates="hotel")

class Habitacion(Base):
    __tablename__ = "habitaciones"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hoteles.id"), nullable=False)
    tipo = Column(String, nullable=False)  # estandar, premium, vip
    tarifa_base = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False)  # indica cuántas habitaciones de este tipo existen
    hotel = relationship("Hotel", back_populates="habitaciones")
    reservas = relationship("Reserva", back_populates="habitacion")

class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)
    habitacion_id = Column(Integer, ForeignKey("habitaciones.id"), nullable=False)
    fecha_entrada = Column(String, nullable=False)  # YYYY-MM-DD (simplificado)
    fecha_salida = Column(String, nullable=False)   # YYYY-MM-DD
    num_personas = Column(Integer, nullable=False)
    tarifa_total = Column(Float, nullable=False)
    habitacion = relationship("Habitacion", back_populates="reservas")
