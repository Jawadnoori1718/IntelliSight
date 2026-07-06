"""Text recognition (OCR) endpoints.

- POST /api/ocr  — read text in a single uploaded image
- WS   /ws/ocr   — send JPEG frames, receive recognised text blocks
"""

import logging

from fastapi import APIRouter, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.concurrency import run_in_threadpool

from app.services.ocr import get_ocr

logger = logging.getLogger("intellisight.ocr")
router = APIRouter()


@router.post("/api/ocr", tags=["ocr"], summary="Read text in an uploaded image")
async def http_ocr(file: UploadFile = File(...)) -> dict:
    data = await file.read()
    return await run_in_threadpool(get_ocr().read_jpeg, data)


@router.websocket("/ws/ocr")
async def ws_ocr(websocket: WebSocket) -> None:
    await websocket.accept()
    logger.info("ocr client connected")
    ocr = get_ocr()
    try:
        while True:
            frame = await websocket.receive_bytes()
            result = await run_in_threadpool(ocr.read_jpeg, frame)
            await websocket.send_json(result)
    except WebSocketDisconnect:
        logger.info("ocr client disconnected")
    except Exception:
        logger.exception("ocr socket error")
        try:
            await websocket.close()
        except RuntimeError:
            pass
