# routers/simulator_control.py
from fastapi import APIRouter, HTTPException
from simulator import simulator
from bd.database import SessionLocal
from bd.models import Machine

routerSimuladorControl = APIRouter(prefix="/simulator", tags=["Simulator"])

@routerSimuladorControl.post("/start/")
async def start_machine_simulation(machine_id: int):
    # validar que exista la máquina
    db = SessionLocal()
    try:
        m = db.query(Machine).filter(Machine.id == machine_id).first()
    finally:
        db.close()
    if not m:
        raise HTTPException(status_code=404, detail="Machine not found")
    await simulator.start_machine(machine_id)
    return {"status": "started", "machine_id": machine_id}

@routerSimuladorControl.post("/stop/")
async def stop_machine_simulation(machine_id: int):
    await simulator.stop_machine(machine_id)
    return {"status": "stopped", "machine_id": machine_id}

@routerSimuladorControl.post("/start_all")
async def start_all_simulations():
    # opcional: iniciar para todas las máquinas existentes
    db = SessionLocal()
    try:
        machines = db.query(Machine.id).all()
        ids = [m[0] for m in machines]
    finally:
        db.close()
    await simulator.start_all(ids)
    return {"status": "started_all", "count": len(ids)}

@routerSimuladorControl.post("/stop_all")
async def stop_all_simulations():
    await simulator.stop_all()
    return {"status": "stopped_all"}
