import enum
from sqlalchemy import Column, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text, DECIMAL, func
from bd.database import Base
from sqlalchemy.orm import relationship



"""
TABLES

- machine
- machine_data
- alerts

"""

class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())

    # Relaciones
    data = relationship("MachineData", back_populates="machine", cascade="all, delete")
    alerts = relationship("Alert", back_populates="machine", cascade="all, delete")

class MachineData(Base):
    __tablename__ = "machine_data"

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey("machines.id", ondelete="CASCADE"), nullable=False)

    vibration = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    energy_consumption = Column(Float, nullable=False)
    recorded_at = Column(DateTime, nullable=False)

    # Relación inversa
    machine = relationship("Machine", back_populates="data")

class AlertType(str, enum.Enum):
    warning = "advertencia"
    critical = "critico"
    stable = "estable"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey("machines.id", ondelete="CASCADE"), nullable=False)

    alert_type = Column(Enum(AlertType), nullable=False)
    probability = Column(Float, nullable=False)
    message = Column(Text)
    created_at = Column(DateTime, default=func.now())

    # Relación inversa
    machine = relationship("Machine", back_populates="alerts")





