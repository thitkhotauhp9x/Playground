import asyncio
import logging
from asyncio import Queue

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

log_router = APIRouter(prefix="/logs", tags=["Logs Viewer"])

log_queue: Queue = Queue()


class QueueLogHandler(logging.Handler):
    def emit(self, record):
        try:
            log_entry = self.format(record)

            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.call_soon_threadsafe(log_queue.put_nowait, log_entry)
        except Exception:
            self.handleError(record)


async def log_streamer():
    while True:
        log_entry = await log_queue.get()
        yield f"data: {log_entry}\n\n"


@log_router.get("/stream")
async def stream_logs():
    """Endpoint stream trực tiếp log từ RAM tại /logs/stream"""
    return StreamingResponse(log_streamer(), media_type="text/event-stream")
