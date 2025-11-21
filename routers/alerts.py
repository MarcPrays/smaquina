# routers/alerts.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from bd.database import get_db
from bd.models import Alert, Machine
from bd.schemas import AlertResponse, AlertCreate
from crud import alerts

routerAlerts = APIRouter(tags=["Alerts"])


# ============================================================
# CREATE ALERT
# ============================================================
@routerAlerts.post("/new_alert", response_model=AlertResponse)
async def create_alert(data: AlertCreate, session: Session = Depends(get_db)):
    return alerts.create_alert(session, data)


# ============================================================
# GET ALL ALERTS
# ============================================================
@routerAlerts.get("/alerts_machine/", response_model=list[AlertResponse])
async def get_alerts(
    machine_id: int,
    session: Session = Depends(get_db),
):
    return alerts.get_alerts_by_machine(session, machine_id)


# ============================================================
# GET ONE ALERT
# ============================================================
@routerAlerts.get("/get_alert/", response_model=AlertResponse)
async def get_alert(alert_id: int, session: Session = Depends(get_db)):
    return alerts.get_alert(session, alert_id)

