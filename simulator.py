# simulator.py
import asyncio
import random
from datetime import datetime
from typing import Dict, Optional

# IMPORTS PARA ESCRIBIR EN BD (sin bloquear el loop)
from bd.database import SessionLocal   # asume que tienes SessionLocal en bd.database
from crud.machine_data import create_machine_data
from bd.schemas import MachineDataBase
from analisys.predictive import analyze_data_point


# IMPORT PARA EMITIR A WEBSOCKETS
# Vamos a importar el manager si existe (routers/realtime.py definirá WSManager)
try:
    from routers.realtime import ws_manager
except Exception:
    ws_manager = None

class Simulator:
    """
    Simula lecturas para máquinas registradas en la BD.
    - genera valores de temperature, vibration, energy cada N segundos por máquina.
    - guarda en BD usando create_machine_data (función CRUD sincronica) dentro de un hilo.
    - emite evento via WebSocket (si ws_manager está presente).
    """

    def __init__(self, interval: float = 1.0):
        self.interval = interval  # segundos entre lecturas por máquina
        self._tasks: Dict[int, asyncio.Task] = {}
        self._running = False

    async def _run_for_machine(self, machine_id: int):
        """Loop que genera datos para una máquina específica."""
        while self._running and machine_id in self._tasks:
            reading = self._generate_reading(machine_id)
            # Guarda en BD (operación bloqueante) dentro de hilo con asyncio.to_thread
            await asyncio.to_thread(self._save_reading_db, reading)
            # Emite por WebSocket (si manager disponible)
            if ws_manager:
                await ws_manager.broadcast_machine(machine_id, reading)
            await asyncio.sleep(self.interval)

    def _generate_reading(self, machine_id: int) -> dict:
        """Genera una lectura realista simulada."""
        # Puedes ajustar los rangos según el tipo de máquina
        temperature = round(random.uniform(40.0, 95.0), 2)         # °C
        vibration = round(random.uniform(0.05, 5.0), 3)            # g o mm/s según escala
        energy = round(random.uniform(50.0, 800.0), 2)             # W o kW
        ts = datetime.utcnow()
        data = {
            "machine_id": machine_id,
            "temperature": temperature,
            "vibration": vibration,
            "energy_consumption": energy,
            "recorded_at": ts
        }
        return data

    def _save_reading_db(self, reading: dict):
        """
        Función que corre en hilo (sync) para usar tu CRUD sync que maneja Session.
        Crea una SessionLocal, llama a create_machine_data(db, schema).
        """
        db = SessionLocal()
        try:
            schema = MachineDataBase(
                machine_id=reading["machine_id"],
                vibration=reading["vibration"],
                temperature=reading["temperature"],
                energy_consumption=reading["energy_consumption"],
                recorded_at=reading["recorded_at"]
            )
            # Guarda en la base de datos
            created = create_machine_data(db, schema)

            # ANALISIS PREDICTIVO AQUÍ
            # created es un modelo MachineData ya guardado y refrescado
            analyze_data_point(db, created)
        except Exception as e:
            # aquí podrías loggear error
            print("Error guardando lectura simulada:", e)
        finally:
            db.close()

    async def start_machine(self, machine_id: int):
        """Inicia la simulación para una máquina concreta (si no está ya iniciada)."""
        if machine_id in self._tasks:
            return
        self._running = True
        task = asyncio.create_task(self._run_for_machine(machine_id))
        self._tasks[machine_id] = task

    async def stop_machine(self, machine_id: int):
        """Detiene la simulación para una máquina concreta."""
        if machine_id in self._tasks:
            # cancelar tarea
            task = self._tasks.pop(machine_id)
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    async def start_all(self, machine_ids: Optional[list] = None):
        """Inicia simulación para cada id de machine; si no se pasa ids intentará simular para [1..n] o dejar neutral."""
        self._running = True
        if machine_ids:
            for mid in machine_ids:
                if mid not in self._tasks:
                    await self.start_machine(mid)

    async def stop_all(self):
        """Detiene todas las simulaciones."""
        self._running = False
        for mid in list(self._tasks.keys()):
            await self.stop_machine(mid)

# instancia global (importable)
simulator = Simulator(interval=30.0)
