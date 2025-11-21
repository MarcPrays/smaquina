# routers/realtime.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from typing import Dict, List
import json

routerRealtime = APIRouter(prefix="/realtime", tags=["Realtime"])

class WSManager:
    """
    Manager simple para websockets.
    Mantiene conexiones por machine_id.
    """
    def __init__(self):
        # mapping: machine_id -> list of websocket connections
        self.active: Dict[int, List[WebSocket]] = {}

    async def connect(self, machine_id: int, websocket: WebSocket):
        await websocket.accept()
        conns = self.active.get(machine_id, [])
        conns.append(websocket)
        self.active[machine_id] = conns

    def disconnect(self, machine_id: int, websocket: WebSocket):
        conns = self.active.get(machine_id, [])
        if websocket in conns:
            conns.remove(websocket)
            self.active[machine_id] = conns

    async def broadcast_machine(self, machine_id: int, payload: dict):
        """Enviar payload JSON a todos los sockets suscritos a machine_id."""
        conns = self.active.get(machine_id, [])
        if not conns:
            return
        text = json.dumps({
            "machine_id": machine_id,
            "data": {
                "temperature": payload["temperature"],
                "vibration": payload["vibration"],
                "energy_consumption": payload["energy_consumption"],
                "recorded_at": payload["recorded_at"].isoformat()
            }
        }, default=str)
        for ws in list(conns):
            try:
                await ws.send_text(text)
            except Exception:
                # si falla, desconectar
                await self._safe_disconnect(machine_id, ws)

    async def _safe_disconnect(self, machine_id: int, ws: WebSocket):
        try:
            await ws.close()
        except Exception:
            pass
        self.disconnect(machine_id, ws)


# instancia global
ws_manager = WSManager()


@routerRealtime.websocket("/machine/")
async def machine_ws(websocket: WebSocket, machine_id: int):
    """
    WebSocket endpoint para suscribirse a lecturas de la máquina con id=machine_id.
    - Conectar desde Angular: new WebSocket("ws://localhost:8000/realtime/machine/1")
    """
    try:
        await ws_manager.connect(machine_id, websocket)
        while True:
            # Espera mensajes del cliente si quieres soporte bidireccional.
            # Para solo emitir lecturas, simplemente espera pings o duerme.
            data = await websocket.receive_text()
            # opcional: procesar mensajes del cliente
            # Aquí no hacemos nada con data, pero podrías permitir "start", "stop", etc.
            # Por ejemplo, si cliente envía "ping" responder:
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(machine_id, websocket)
