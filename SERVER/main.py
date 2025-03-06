from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict
from graph import Graph
from entities import EventGraph
import uvicorn
from logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_message(self, message: dict, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)

manager = ConnectionManager()
graph = Graph()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    logger.info(f"New Client Connected: {client_id}")
    try:
        while True:
            data = await websocket.receive_json()
            try:
                question = data.get('question')
                chat_id = data.get('chat_id', client_id)
                user_name = data.get('user_name', 'User')
                is_search = data.get('is_search', False)

                start_time = datetime.now()

                await manager.send_message(
                    {
                        "status": "Processing",
                        "step": "Bắt đầu",
                        "message": "Đang bắt đầu xử lý câu hỏi...",
                        "next_step": "check_question"
                    },
                    client_id
                )

                # Stream từng bước từ graph.run
                async for event in graph.run(question, chat_id, user_name, is_search):
                    # Parse event đến các đối tượng EventGraph
                    event_obj = EventGraph(**event)

                    # Lấy thông tin từ event
                    node_name = event_obj.in_node if hasattr(event_obj, 'in_node') else 'Unknown'
                    output = event_obj.output if hasattr(event_obj, 'output') else ''
                    next_state = event_obj.next_state if hasattr(event_obj, 'next_state') else ''

                    # Gửi thông tin chi tiết về từng bước
                    status_message = {
                        "status": "Processing",
                        "step": node_name,
                        "message": f"Đang xử lý tại bước: {node_name}",
                        "next_step": next_state,
                        "timestamp": datetime.now().isoformat()
                    }

                    # Safe logging to avoid Unicode errors
                    try:
                        logger.info(f"Processing step: {node_name} -> {next_state}")
                    except Exception as log_error:
                        logger.error(f"Error logging processing step: {str(log_error)}")

                    await manager.send_message(status_message, client_id)

                    # Nếu đây là node cuối cùng và có output
                    if node_name in ["Đang tạo câu trả lời", "Đã xảy ra lỗi"] and output:
                        end_time = datetime.now()
                        processing_time = (end_time - start_time).total_seconds()
                        response = {
                            "status": "Completed",
                            "message": output,
                            "time": processing_time,
                            "chat_id": chat_id,
                            "used_search": is_search,
                            "step": "completed"
                        }
                        logger.info(f"Completed in {processing_time:.2f}s")
                        await manager.send_message(response, client_id)
                        break

            except Exception as e:
                error_response = {
                    "status": "Error",
                    "error": str(e),
                    "chat_id": data.get('chat_id', client_id),
                    "step": "error"
                }
                logger.error(f"Error processing request: {str(e)}")
                await manager.send_message(error_response, client_id)

    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info(f"Client Disconnected: {client_id}")

if __name__ == "__main__":
    import sys
    # Force UTF-8 encoding for console output
    if sys.stdout.encoding != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    uvicorn.run(app, host="127.0.0.1", port=8000)
