from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from bd.database import Base, engine
from routers.machines import routerMachines
from routers.machine_data import routerMachineData
from routers.alerts import routerAlerts

from routers.realtime import routerRealtime
from routers.simulator_control import routerSimuladorControl

# import simulator singleton
from simulator import simulator


app = FastAPI(
    title="Monitoreo de Maquinas API",
    description="API para monitoreo, predicción y alertas de maquinaria industrial",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ============================================================
# REGISTRO DE ROUTERS
# ============================================================

app.include_router(routerMachines)
app.include_router(routerMachineData)
app.include_router(routerAlerts)
app.include_router(routerRealtime)
app.include_router(routerSimuladorControl)

# ============================================================
# ENDPOINT RAÍZ
# ============================================================

# Opcional: arrancar simulación automática al iniciar la app
@app.on_event("startup")
async def startup_event():
    # Si quieres que arranque todo automáticamente:
    # await simulator.start_all([1,2,3])  # pasar ids que tengas
    pass

@app.on_event("shutdown")
async def shutdown_event():
    await simulator.stop_all()



Base.metadata.create_all(bind=engine)
