from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from bd.models import AlertType


# ============================================================
# MACHINE SCHEMAS
# ============================================================

class MachineCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None


class MachineUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None


class MachineResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# MACHINE DATA SCHEMAS
# ============================================================

class MachineDataBase(BaseModel):
    machine_id: int
    vibration: float
    temperature: float
    energy_consumption: float
    recorded_at: datetime



class MachineDataResponse(MachineDataBase):
    id: int    

    class Config:
        from_attributes = True


# ============================================================
# ALERT SCHEMAS
# ============================================================

class AlertCreate(BaseModel):
    machine_id: int
    alert_type: AlertType
    probability: float = Field(..., ge=0, le=1)
    message: str = Field(..., min_length=5)


class AlertResponse(AlertCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


