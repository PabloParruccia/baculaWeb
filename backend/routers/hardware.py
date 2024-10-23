from fastapi import FastAPI, Body ,HTTPException,status,Query,Depends,File,APIRouter
from fastapi.responses import HTMLResponse,JSONResponse

import subprocess
import psutil
from schemas.hardware import ServerStatus
route_hardware = APIRouter()


def check_service_status(service_name: str) -> str:
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', service_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return "activo"
        else:
            return "inactivo"
    except Exception as e:
        return f"error: {e}"

def check_service_status(service_name: str) -> str:
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', service_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return "activo"
        else:
            return "inactivo"
    except Exception as e:
        return f"error: {e}"

@route_hardware.get("/server-status", response_model=ServerStatus, tags=['Comandos'], status_code=status.HTTP_200_OK)
def get_server_status():
    # Obtén el uso del disco
    disk_usage = psutil.disk_usage('/')
    disk_percent = disk_usage.percent

    # Obtén el uso de la CPU
    cpu_usage = psutil.cpu_percent(interval=1)

    # Obtén el uso de la RAM
    ram_usage = psutil.virtual_memory().percent

    # Verifica el estado del servicio Bacula
    bacula_status = check_service_status('bacula-fd')

    print(f"Disk usage: {disk_usage}, CPU usage: {cpu_usage}%, RAM usage: {ram_usage}%")

    return ServerStatus(
        disk=int(disk_percent),
        cpu=int(cpu_usage),
        ram=int(ram_usage),
        bacula=bacula_status
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(route_hardware, host='0.0.0.0', port=8000)