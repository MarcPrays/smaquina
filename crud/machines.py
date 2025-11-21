# crud/machines.py

from sqlalchemy.orm import Session
from bd.models import Machine
from bd.schemas import MachineCreate, MachineUpdate


# ============================
# CREATE
# ============================
def create_machine(db: Session, machine_data: MachineCreate, image_url: str = None):
    new_machine = Machine(
        name=machine_data.name,
        description=machine_data.description,
        image_url=image_url
    )
    db.add(new_machine)
    db.commit()
    db.refresh(new_machine)
    return new_machine



# ============================
# READ (GET ALL)
# ============================
def get_machines(db: Session):
    return db.query(Machine).all()


# ============================
# READ (GET ONE)
# ============================
def get_machine(db: Session, machine_id: int):
    return db.query(Machine).filter(Machine.id == machine_id).first()


# ============================
# UPDATE
# ============================
def update_machine(db: Session, machine_id: int, machine_data: MachineUpdate):
    machine = db.query(Machine).filter(Machine.id == machine_id).first()

    if not machine:
        return None

    if machine_data.name is not None:
        machine.name = machine_data.name

    if machine_data.description is not None:
        machine.description = machine_data.description

    db.commit()
    db.refresh(machine)
    return machine


# ============================
# DELETE
# ============================
def delete_machine(db: Session, machine_id: int):
    machine = db.query(Machine).filter(Machine.id == machine_id).first()

    if not machine:
        return False

    db.delete(machine)
    db.commit()
    return True
