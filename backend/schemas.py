from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from models import EstadoFactura


# Schemas de Cliente
class ClienteBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    empresa: Optional[str] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    empresa: Optional[str] = None


class Cliente(ClienteBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Schemas de Factura
class FacturaBase(BaseModel):
    numero_factura: str
    cliente_id: int
    monto: float = Field(gt=0)
    fecha_vencimiento: datetime
    descripcion: Optional[str] = None
    notas: Optional[str] = None


class FacturaCreate(FacturaBase):
    pass


class FacturaUpdate(BaseModel):
    numero_factura: Optional[str] = None
    monto: Optional[float] = Field(None, gt=0)
    fecha_vencimiento: Optional[datetime] = None
    estado: Optional[EstadoFactura] = None
    descripcion: Optional[str] = None
    notas: Optional[str] = None


class EmailLogSimple(BaseModel):
    id: int
    destinatario: str
    asunto: str
    enviado_at: datetime
    estado: str
    
    class Config:
        from_attributes = True


class Factura(FacturaBase):
    id: int
    fecha_emision: datetime
    estado: EstadoFactura
    created_at: datetime
    updated_at: datetime
    cliente: Cliente
    emails_enviados: List[EmailLogSimple] = []
    
    class Config:
        from_attributes = True


# Schema para estadísticas del dashboard
class DashboardStats(BaseModel):
    total_facturas: int
    facturas_pendientes: int
    facturas_vencidas: int
    facturas_pagadas: int
    monto_total_pendiente: float
    monto_total_vencido: float


# Schema para alertas
class Alerta(BaseModel):
    factura_id: int
    numero_factura: str
    cliente: str
    monto: float
    fecha_vencimiento: datetime
    dias_hasta_vencimiento: int
    tipo: str  # "proxima_vencer" o "vencida"
    mensaje: str


# Schema para envío de email
class EnviarEmailRequest(BaseModel):
    factura_id: int
    asunto: str
    cuerpo: str
