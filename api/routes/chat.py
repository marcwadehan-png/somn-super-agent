"""
Somn API Server - 对话路由
支持同步对话、SSE流式输出、WebSocket实时通信
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from datetime import datetime
from typing import Optional

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


def register_chat_routes(app, app_state):
    """注册对话相关路由"""

    # ── 同步对话 ──

    @app.post("/api/v1/chat", tags=["对话"])
    async def chat(request_body: dict):
        """
        同步对话接口

        请求体:
        {
            "message": "用户消息",
            "session_id": "可选会话ID",
            "context": {},
            "industry": "可选行业",
            "stream": false
        }
        """
        message = request_body.get("message", "").strip()
        if not message:
            return _error_response("消息不能为空", "EMPTY_MESSAGE")

        session_id = request_body.get("session_id") or str(uuid.uuid4())[:8]
        context = request_body.get("context", {})
        industry = request_body.get("industry")

        start = time.time()
        try:
            agent = app_state.get_agent_core()
            if context:
                agent_ctx = context.copy()
            else:
                agent_ctx = {}
            if industry:
                agent_ctx["industry"] = industry

            response = await asyncio.to_thread(
                agent.process_input, message, agent_ctx
            )

            elapsed = (time.time() - start) * 1000

            # 提取回复文本 — AgentResponse 是 dataclass，有 content/message/success 字段
            # 注意：content 默认=""，message 才是实际回复，需按优先级正确提取
            reply = ""
            _resp_type = type(response).__name__
            _resp_content = getattr(response, 'content', '[N/A]') if not isinstance(response, dict) else '[dict]'
            _resp_message = getattr(response, 'message', '[N/A]') if not isinstance(response, dict) else '[dict]'
            if isinstance(response, dict):
                reply = response.get("response", response.get("reply", response.get("message", str(response))))
            elif hasattr(response, 'message') and response.message:
                reply = response.message
            elif hasattr(response, 'content') and response.content:
                reply = response.content
            elif isinstance(response, str):
                reply = response
            else:
                reply = str(response) if not isinstance(response, type(None)) else ""

            return {
                "success": True,
                "message": "对话完成",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "session_id": session_id,
                    "reply": reply,
                    "wisdom_insights": [],
                    "confidence": 0.85,
                    "processing_time_ms": round(elapsed, 1),
                    "metadata": {
                        "raw_type": _resp_type,
                        "resp_content": str(_resp_content)[:100],
                        "resp_message": str(_resp_message)[:100],
                        "reply_source": "message" if (hasattr(response, 'message') and response.message) else ("content" if (hasattr(response, 'content') and response.content) else "other")
                    },
                }
            }
        except Exception as e:
            logger.error(f"对话处理失败: {e}", exc_info=True)
            return _error_response("对话处理失败", "CHAT_ERROR")

    # ── SSE 流式对话 ──

    @app.get("/api/v1/chat/stream", tags=["对话"])
    async def chat_stream(message: str, session_id: Optional[str] = None):
        """SSE 流式对话 (使用 SomnCore)"""
        from fastapi.responses import StreamingResponse

        if not message.strip():
            return _error_response("消息不能为空", "EMPTY_MESSAGE")

        sid = session_id or str(uuid.uuid4())[:8]

        async def event_generator():
            try:
                core = app_state.get_somn_core()

                # 思考阶段
                yield _sse_chunk("thinking", "正在分析您的需求...", sid)

                start = time.time()

                # SomnCore 方法名是 analyze_requirement，需要 LLM 初始化
                try:
                    result = await asyncio.to_thread(
                        core.analyze_requirement, message
                    )
                except Exception as core_err:
                    logger.warning(f"SSE: SomnCore 失败 ({core_err})，降级到 AgentCore")
                    result = None

                elapsed = (time.time() - start) * 1000

                # 提取回复 — result 可能是 dict 或 None (降级后)
                reply = ""
                if result is None:
                    # 降级到 AgentCore
                    try:
                        agent = app_state.get_agent_core()
                        agent_resp = await asyncio.to_thread(
                            agent.process_input, message
                        )
                        if hasattr(agent_resp, 'content'):
                            reply = agent_resp.content
                        elif hasattr(agent_resp, 'message'):
                            reply = agent_resp.message
                        elif isinstance(agent_resp, str):
                            reply = agent_resp
                        else:
                            reply = str(agent_resp)
                    except Exception as agent_err:
                        reply = f"处理失败: {agent_err}"
                elif isinstance(result, dict):
                    reply = result.get("response", result.get("reply", json.dumps(result, ensure_ascii=False)))
                elif isinstance(result, str):
                    reply = result
                else:
                    reply = str(result)

                # 分块输出
                chunk_size = 50
                for i in range(0, len(reply), chunk_size):
                    yield _sse_chunk("text", reply[i:i + chunk_size], sid)
                    await asyncio.sleep(0.02)

                yield _sse_chunk("done", json.dumps({
                    "session_id": sid,
                    "processing_time_ms": round(elapsed, 1),
                }), sid)

            except Exception as e:
                logger.error(f"流式对话失败: {e}", exc_info=True)
                yield _sse_chunk("error", "处理失败", sid)

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )

    # ── WebSocket 实时通信 ──

    @app.websocket("/api/v1/ws")
    async def websocket_chat(websocket):
        """WebSocket 实时对话"""
        await websocket.accept()
        logger.info("WebSocket 客户端已连接")

        try:
            while True:
                data = await websocket.receive_text()
                try:
                    msg = json.loads(data)
                    msg_type = msg.get("type", "chat")
                    content = msg.get("content", "")

                    if msg_type == "ping":
                        await websocket.send_text(json.dumps({
                            "type": "pong",
                            "timestamp": datetime.now().isoformat(),
                        }))
                        continue

                    if msg_type == "chat" and content:
                        sid = msg.get("session_id", str(uuid.uuid4())[:8])
                        await websocket.send_text(json.dumps({
                            "type": "status",
                            "content": "正在处理...",
                            "session_id": sid,
                        }))

                        try:
                            agent = app_state.get_agent_core()
                            start = time.time()
                            result = await asyncio.to_thread(
                                agent.process_input, content
                            )
                            elapsed = (time.time() - start) * 1000

                            # AgentResponse 是 dataclass
                            if hasattr(result, 'content'):
                                reply = result.content
                            elif hasattr(result, 'message'):
                                reply = result.message
                            elif isinstance(result, dict):
                                reply = result.get("response", result.get("reply", str(result)))
                            elif isinstance(result, str):
                                reply = result
                            else:
                                reply = str(result)

                            await websocket.send_text(json.dumps({
                                "type": "reply",
                                "content": reply,
                                "session_id": sid,
                                "processing_time_ms": round(elapsed, 1),
                            }))

                        except Exception as e:
                            logger.error(f"WebSocket 聊天处理失败: {e}", exc_info=True)
                            await websocket.send_text(json.dumps({
                                "type": "error",
                                "content": "处理消息时发生内部错误",
                                "session_id": sid,
                            }))

                except json.JSONDecodeError:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "content": "无效的JSON格式",
                    }))

        except WebSocketDisconnect:
            logger.info("WebSocket 客户端正常断开")
        except Exception as e:
            logger.error(f"WebSocket 异常: {e}", exc_info=True)
        finally:
            logger.info("WebSocket 客户端已断开")


def _sse_chunk(chunk_type: str, content: str, session_id: str) -> str:
    """构造SSE数据块"""
    data = json.dumps({
        "chunk_type": chunk_type,
        "content": content,
        "session_id": session_id,
    }, ensure_ascii=False)
    return f"data: {data}\n\n"


def _error_response(error: str, code: str) -> dict:
    """构造错误响应"""
    from ..utils import error_response
    return error_response(error, code)
