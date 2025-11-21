# routers/machine_data.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from bd.database import get_db
from bd.models import MachineData, Machine
from bd.schemas import MachineDataBase, MachineDataResponse
from crud import machine_data

routerMachineData = APIRouter( tags=["Machine Data"])


# ============================================================
# CREATE DATA RECORD
# ============================================================
@routerMachineData.post("/new_machine_data", response_model=MachineDataResponse)
async def create_machine_data(data: MachineDataBase, session: Session = Depends(get_db)):
    return machine_data.create_machine_data(session, data)



# ============================================================
# GET ALL DATA (OPTIONAL FILTER BY MACHINE)
# ============================================================
@routerMachineData.get("/datas_machine/", response_model=list[MachineDataResponse])
async def get_all_data(
    machine_id: int,
    session: Session = Depends(get_db),
):
    return machine_data.get_machine_data_by_machine(session, machine_id)


# ============================================================
# GET SINGLE DATA ENTRY
# ============================================================
@routerMachineData.get("/get_data", response_model=MachineDataResponse)
async def get_data(data_id: int, session: Session = Depends(get_db)):
    return machine_data.get_machine_data(session, data_id)

    
