"""Object detection endpoints.

- POST /api/detect  — detect objects in a single uploaded image (handy for testing)
- WS   /ws/detect   — realtime stream: client sends JPEG frames, server replies
                      with detections for each one.
"""

import logging

from fastapi import APIRouter, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.concurrency import run_in_threadpool

from app.services.detector import get_detector

logger = logging.getLogger("intellisight.detect")
router = APIRouter()


@router.post("/api/detect", tags=["detection"], summary="Detect objects in an uploaded image")
async def http_detect(file: UploadFile = File(...)) -> dict:
    data = await file.read()
    # Run the (blocking) model in a thread so the event loop stays responsive.
    return await run_in_threadpool(get_detector().detect_jpeg, data)


@router.websocket("/ws/detect")
async def ws_detect(websocket: WebSocket) -> None:
    await websocket.accept()
    logger.info("detection client connected")
    detector = get_detector()
    try:
        while True:
            frame = await websocket.receive_bytes()
            result = await run_in_threadpool(detector.detect_jpeg, frame)
            await websocket.send_json(result)
    except WebSocketDisconnect:
        logger.info("detection client disconnected")
    except Exception:
        logger.exception("detection socket error")
        try:
            await websocket.close()
        except RuntimeError:
            pass
