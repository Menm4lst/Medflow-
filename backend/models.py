from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum


class EstadoFactura(str, enum.Enum):
    PENDIENTE = "Pendiente"
    EN_SEGUIMIENTO = "En seguimiento"
    PAGADA = "Pagada"
    VENCIDA = "Vencida"


class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefono = Column(String, nullable=True)
    empresa = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    facturas = relationship("Factura", back_populates="cliente")


class Factura(Base):
    __tablename__ = "facturas"
    
    id = Column(Integer, primary_key=True, index=True)
    numero_factura = Column(String, unique=True, nullable=False, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    monto = Column(Float, nullable=False)
    fecha_emision = Column(DateTime, default=datetime.utcnow)
    fecha_vencimiento = Column(DateTime, nullable=False)
    estado = Column(Enum(EstadoFactura), default=EstadoFactura.PENDIENTE)
    descripcion = Column(Text, nullable=True)
    notas = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    cliente = relationship("Cliente", back_populates="facturas")
    emails_enviados = relationship("EmailLog", back_populates="factura", cascade="all, delete-orphan")


class EmailLog(Base):
    __tablename__ = "email_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    destinatario = Column(String, nullable=False)
    asunto = Column(String, nullable=False)
    cuerpo = Column(Text, nullable=False)
    enviado_at = Column(DateTime, default=datetime.utcnow)
    estado = Column(String, default="Enviado")  # Enviado, Error, Pendiente
    
    factura = relationship("Factura", back_populates="emails_enviados")
