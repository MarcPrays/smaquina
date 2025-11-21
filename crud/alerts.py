from sqlalchemy.orm import Session
from bd.models import Alert
from bd.schemas import AlertCreate


# ============================
# CREATE ALERT
# ============================
def create_alert(db: Session, data: AlertCreate):
    new_alert = Alert(
        machine_id=data.machine_id,
        alert_type=data.alert_type,
        probability=data.probability,
        message=data.message
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return new_alert


# ============================
# GET ALERTS BY MACHINE
# ============================
def get_alerts_by_machine(db: Session, machine_id: int):
    return db.query(Alert).filter(Alert.machine_id == machine_id).all()


# ============================
# GET ONE ALERT
# ============================
def get_alert(db: Session, alert_id: int):
    return db.query(Alert).filter(Alert.id == alert_id).first()


# ============================
# DELETE ALERT
# ============================
def delete_alert(db: Session, alert_id: int):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return False

    db.delete(alert)
    db.commit()
    return True
