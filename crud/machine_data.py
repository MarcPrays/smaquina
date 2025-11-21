from sqlalchemy.orm import Session
from bd.models import MachineData
from bd.schemas import MachineDataBase


# ============================
# CREATE
# ============================
def create_machine_data(db: Session, data: MachineDataBase):
    new_data = MachineData(
        machine_id=data.machine_id,
        vibration=data.vibration,
        temperature=data.temperature,
        energy_consumption=data.energy_consumption,
        recorded_at=data.recorded_at
    )

    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


# ============================
# GET DATA BY MACHINE
# ============================
def get_machine_data_by_machine(db: Session, machine_id: int, limit: int = 100):
    return (
        db.query(MachineData)
        .filter(MachineData.machine_id == machine_id)
        .order_by(MachineData.recorded_at.desc())
        .limit(limit)
        .all()
    )


# ============================
# GET ONE ENTRY
# ============================
def get_machine_data(db: Session, data_id: int):
    return db.query(MachineData).filter(MachineData.id == data_id).first()


# ============================
# DELETE ENTRY
# ============================
def delete_machine_data(db: Session, data_id: int):
    data = db.query(MachineData).filter(MachineData.id == data_id).first()
    if not data:
        return False

    db.delete(data)
    db.commit()
    return True
