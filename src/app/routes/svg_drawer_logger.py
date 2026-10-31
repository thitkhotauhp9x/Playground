from fastapi import APIRouter

from app.libs.loggers.in_memory_handler import log_storage

log_router = APIRouter(prefix="/logs", tags=["Logs Viewer"])


@log_router.get("/stream")
async def stream_logs():
    recent_logs = list(log_storage)[-10000:]
    return {"total": len(log_storage), "logs": recent_logs}
