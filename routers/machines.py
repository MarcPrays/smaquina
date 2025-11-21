# routers/machines.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from bd.database import get_db
from bd.models import Machine
from crud import machines
from bd.schemas import (
    MachineCreate,
    MachineUpdate,
    MachineResponse
)

import os
import shutil
from fastapi import File, Form, UploadFile



routerMachines = APIRouter(tags=["Machines"])


# ============================================================
# CREATE
# ============================================================
@routerMachines.post("/new_machine", response_model=MachineResponse)
async def create_machine_with_image(
    name: str = Form(...),
    description: str = Form(None),
    image: UploadFile = File(None),
    session: Session = Depends(get_db)
):
    # Guardar la imagen
    file_path = None

    if image:
        upload_dir = "uploads/machines"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = f"{upload_dir}/{image.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    # Llamar al CRUD
    data = MachineCreate(name=name, description=description)
    return machines.create_machine(session, data, image_url=file_path)



# ============================================================
# READ ALL
# ============================================================
@routerMachines.get("/machines", response_model=list[MachineResponse])
async def get_machines(session: Session = Depends(get_db)):
    return machines.get_machines(session)
    

# ============================================================
# READ ONE
# ============================================================
@routerMachines.get("/get_machine/", response_model=MachineResponse)
async def get_machine(machine_id: int, session: Session = Depends(get_db)):
    return machines.get_machine(session, machine_id)
    

# ============================================================
# UPDATE
# ============================================================
@routerMachines.put("/update_machine/", response_model=MachineResponse)
async def update_machine(
    machine_id: int,
    machine_data: MachineUpdate,
    session: Session = Depends(get_db)
):
    return machines.update_machine(session, machine_id, machine_data)
    

# ============================================================
# DELETE
# ============================================================
@routerMachines.delete("/delete_machine/")
async def delete_machine(machine_id: int, session: Session = Depends(get_db)):
    return machines.delete_machine(session, machine_id)

