from fastapi import APIRouter
import platform
import socket

router = APIRouter()


@router.get("/system")
def system_info():
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_version": platform.version(),
    }
