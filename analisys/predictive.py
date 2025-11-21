# analysis/predictive.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from bd.models import MachineData, Alert, AlertType
from bd.schemas import AlertCreate


# ============================
# Reglas básicas (umbral fijo)
# ============================
THRESHOLDS = {
    "temperature": 80.0,       # ºC
    "vibration": 3.5,          # g
    "energy_consumption": 700  # W
}


def analyze_data_point(db: Session, data_point: MachineData):
    """
    Analiza un nuevo punto de datos usando:
    - Reglas por umbrales
    - Desviación estándar para detectar anormalidades

    Si se detecta un problema, se genera una alerta en BD.
    """

    machine_id = data_point.machine_id

    # =====================================================
    # 1. REGLAS POR UMBRAL (detección inmediata)
    # =====================================================
    triggered = []

    if data_point.temperature > THRESHOLDS["temperature"]:
        triggered.append(("temperatura alta", 0.8))

    if data_point.vibration > THRESHOLDS["vibration"]:
        triggered.append(("vibración excesiva", 0.75))

    if data_point.energy_consumption > THRESHOLDS["energy_consumption"]:
        triggered.append(("consumo energético anormal", 0.7))


    # =====================================================
    # 2. DESVIACIÓN ESTÁNDAR (anomalías estadísticas)
    # =====================================================
    stats = db.query(
        func.avg(MachineData.temperature),
        func.stddev(MachineData.temperature),
        func.avg(MachineData.vibration),
        func.stddev(MachineData.vibration),
        func.avg(MachineData.energy_consumption),
        func.stddev(MachineData.energy_consumption),
    ).filter(
        MachineData.machine_id == machine_id
    ).first()

    (
        avg_t, std_t,
        avg_v, std_v,
        avg_e, std_e
    ) = stats

    # Evita cálculos si muy pocos datos
    if std_t is not None and data_point.temperature > avg_t + 2 * std_t:
        triggered.append(("temperatura fuera del comportamiento normal", 0.65))

    if std_v is not None and data_point.vibration > avg_v + 2 * std_v:
        triggered.append(("vibración fuera del comportamiento normal", 0.60))

    if std_e is not None and data_point.energy_consumption > avg_e + 2 * std_e:
        triggered.append(("energía fuera del comportamiento normal", 0.60))


    # =====================================================
    # 3. SI NO HAY ANOMALÍAS → retorna (estado estable)
    # =====================================================
    if not triggered:
        return None


    # =====================================================
    # 4. TOMAR EL EVENTO MÁS CRÍTICO
    # =====================================================
    message, prob = sorted(triggered, key=lambda x: x[1], reverse=True)[0]

    alert_type = AlertType.critical if prob > 0.75 else AlertType.warning

    # =====================================================
    # 5. CREAR ALERTA EN BD
    # =====================================================
    alert = Alert(
        machine_id=machine_id,
        alert_type=alert_type,
        probability=prob,
        message=message
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)


    return alert
