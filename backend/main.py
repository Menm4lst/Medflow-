from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
import models
import schemas
from database import engine, get_db
from email_service import enviar_email, generar_email_recordatorio

# Crear las tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FacturaFlow - Gestor de Facturación")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============= ENDPOINTS DE CLIENTES =============

@app.post("/api/clientes/", response_model=schemas.Cliente)
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


@app.get("/api/clientes/", response_model=List[schemas.Cliente])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).offset(skip).limit(limit).all()
    return clientes


@app.get("/api/clientes/{cliente_id}", response_model=schemas.Cliente)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@app.put("/api/clientes/{cliente_id}", response_model=schemas.Cliente)
def actualizar_cliente(
    cliente_id: int,
    cliente_update: schemas.ClienteUpdate,
    db: Session = Depends(get_db)
):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    for key, value in cliente_update.model_dump(exclude_unset=True).items():
        setattr(db_cliente, key, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


@app.delete("/api/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    db.delete(cliente)
    db.commit()
    return {"message": "Cliente eliminado exitosamente"}


# ============= ENDPOINTS DE FACTURAS =============

@app.post("/api/facturas/", response_model=schemas.Factura)
def crear_factura(factura: schemas.FacturaCreate, db: Session = Depends(get_db)):
    # Verificar que el cliente existe
    cliente = db.query(models.Cliente).filter(models.Cliente.id == factura.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Verificar que el número de factura no exista
    factura_existente = db.query(models.Factura).filter(
        models.Factura.numero_factura == factura.numero_factura
    ).first()
    if factura_existente:
        raise HTTPException(status_code=400, detail="El número de factura ya existe")
    
    db_factura = models.Factura(**factura.model_dump())
    db.add(db_factura)
    db.commit()
    db.refresh(db_factura)
    return db_factura


@app.get("/api/facturas/", response_model=List[schemas.Factura])
def listar_facturas(
    estado: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Factura)
    
    if estado:
        query = query.filter(models.Factura.estado == estado)
    
    facturas = query.order_by(models.Factura.fecha_vencimiento.desc()).offset(skip).limit(limit).all()
    return facturas


@app.get("/api/facturas/{factura_id}", response_model=schemas.Factura)
def obtener_factura(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura


@app.put("/api/facturas/{factura_id}", response_model=schemas.Factura)
def actualizar_factura(
    factura_id: int,
    factura_update: schemas.FacturaUpdate,
    db: Session = Depends(get_db)
):
    db_factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if not db_factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    for key, value in factura_update.model_dump(exclude_unset=True).items():
        setattr(db_factura, key, value)
    
    db_factura.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_factura)
    return db_factura


@app.delete("/api/facturas/{factura_id}")
def eliminar_factura(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    db.delete(factura)
    db.commit()
    return {"message": "Factura eliminada exitosamente"}


# ============= DASHBOARD Y ESTADÍSTICAS =============

@app.get("/api/dashboard/stats", response_model=schemas.DashboardStats)
def obtener_estadisticas(db: Session = Depends(get_db)):
    total_facturas = db.query(models.Factura).count()
    
    facturas_pendientes = db.query(models.Factura).filter(
        models.Factura.estado == models.EstadoFactura.PENDIENTE
    ).count()
    
    facturas_vencidas = db.query(models.Factura).filter(
        models.Factura.estado == models.EstadoFactura.VENCIDA
    ).count()
    
    facturas_pagadas = db.query(models.Factura).filter(
        models.Factura.estado == models.EstadoFactura.PAGADA
    ).count()
    
    # Calcular montos
    monto_pendiente = db.query(models.Factura).filter(
        models.Factura.estado.in_([models.EstadoFactura.PENDIENTE, models.EstadoFactura.EN_SEGUIMIENTO])
    ).with_entities(models.Factura.monto).all()
    monto_total_pendiente = sum(m[0] for m in monto_pendiente)
    
    monto_vencido = db.query(models.Factura).filter(
        models.Factura.estado == models.EstadoFactura.VENCIDA
    ).with_entities(models.Factura.monto).all()
    monto_total_vencido = sum(m[0] for m in monto_vencido)
    
    return {
        "total_facturas": total_facturas,
        "facturas_pendientes": facturas_pendientes,
        "facturas_vencidas": facturas_vencidas,
        "facturas_pagadas": facturas_pagadas,
        "monto_total_pendiente": monto_total_pendiente,
        "monto_total_vencido": monto_total_vencido
    }


# ============= SISTEMA DE ALERTAS =============

@app.get("/api/alertas/", response_model=List[schemas.Alerta])
def obtener_alertas(db: Session = Depends(get_db)):
    alertas = []
    hoy = datetime.utcnow()
    
    # Facturas próximas a vencer (5 días)
    facturas_por_vencer = db.query(models.Factura).filter(
        models.Factura.estado.in_([models.EstadoFactura.PENDIENTE, models.EstadoFactura.EN_SEGUIMIENTO]),
        models.Factura.fecha_vencimiento > hoy,
        models.Factura.fecha_vencimiento <= hoy + timedelta(days=5)
    ).all()
    
    for factura in facturas_por_vencer:
        dias = (factura.fecha_vencimiento - hoy).days
        alertas.append({
            "factura_id": factura.id,
            "numero_factura": factura.numero_factura,
            "cliente": factura.cliente.nombre,
            "monto": factura.monto,
            "fecha_vencimiento": factura.fecha_vencimiento,
            "dias_hasta_vencimiento": dias,
            "tipo": "proxima_vencer",
            "mensaje": f"Factura vence en {dias} días"
        })
    
    # Facturas vencidas
    facturas_vencidas = db.query(models.Factura).filter(
        models.Factura.estado != models.EstadoFactura.PAGADA,
        models.Factura.fecha_vencimiento < hoy
    ).all()
    
    for factura in facturas_vencidas:
        dias = (hoy - factura.fecha_vencimiento).days
        # Actualizar estado si no está como vencida
        if factura.estado != models.EstadoFactura.VENCIDA:
            factura.estado = models.EstadoFactura.VENCIDA
            db.commit()
        
        alertas.append({
            "factura_id": factura.id,
            "numero_factura": factura.numero_factura,
            "cliente": factura.cliente.nombre,
            "monto": factura.monto,
            "fecha_vencimiento": factura.fecha_vencimiento,
            "dias_hasta_vencimiento": -dias,
            "tipo": "vencida",
            "mensaje": f"Factura vencida hace {dias} días"
        })
    
    return alertas


# ============= SISTEMA DE EMAILS =============

@app.post("/api/emails/enviar")
async def enviar_email_factura(
    request: schemas.EnviarEmailRequest,
    db: Session = Depends(get_db)
):
    factura = db.query(models.Factura).filter(models.Factura.id == request.factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    # Enviar email
    exito = await enviar_email(
        destinatario=factura.cliente.email,
        asunto=request.asunto,
        cuerpo=request.cuerpo
    )
    
    # Registrar en log
    email_log = models.EmailLog(
        factura_id=factura.id,
        destinatario=factura.cliente.email,
        asunto=request.asunto,
        cuerpo=request.cuerpo,
        estado="Enviado" if exito else "Error"
    )
    db.add(email_log)
    
    # Actualizar estado de factura si estaba pendiente
    if factura.estado == models.EstadoFactura.PENDIENTE:
        factura.estado = models.EstadoFactura.EN_SEGUIMIENTO
    
    db.commit()
    
    if not exito:
        return {"message": "Error al enviar email", "success": False}
    
    return {"message": "Email enviado exitosamente", "success": True}


@app.post("/api/emails/recordatorio/{factura_id}")
async def enviar_recordatorio(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    # Calcular días hasta vencimiento
    dias = (factura.fecha_vencimiento - datetime.utcnow()).days
    
    # Generar email
    asunto, cuerpo = generar_email_recordatorio(
        factura.numero_factura,
        factura.cliente.nombre,
        factura.monto,
        dias
    )
    
    # Enviar
    exito = await enviar_email(
        destinatario=factura.cliente.email,
        asunto=asunto,
        cuerpo=cuerpo
    )
    
    # Registrar
    email_log = models.EmailLog(
        factura_id=factura.id,
        destinatario=factura.cliente.email,
        asunto=asunto,
        cuerpo=cuerpo,
        estado="Enviado" if exito else "Error"
    )
    db.add(email_log)
    
    if factura.estado == models.EstadoFactura.PENDIENTE:
        factura.estado = models.EstadoFactura.EN_SEGUIMIENTO
    
    db.commit()
    
    if not exito:
        return {"message": "Error al enviar recordatorio", "success": False}
    
    return {"message": "Recordatorio enviado exitosamente", "success": True}


@app.get("/api/emails/{factura_id}", response_model=List[schemas.EmailLogSimple])
def obtener_emails_factura(factura_id: int, db: Session = Depends(get_db)):
    emails = db.query(models.EmailLog).filter(
        models.EmailLog.factura_id == factura_id
    ).order_by(models.EmailLog.enviado_at.desc()).all()
    return emails


@app.get("/")
def root():
    return {"message": "FacturaFlow - API activa"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
