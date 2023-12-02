import asyncio
import json
from .runner import is_process_closed, regist_client, unregist_client
import logging
from .tcp_proto_base import TcpProtoBase
from .tcp_session_mgr import TcpSessionMgr
from .tcp_callback_base import TcpCallbackBase


class TcpClient:
    def __init__(self,
                 host: str,
                 port: int,
                 cb: TcpCallbackBase,
                 proto: TcpProtoBase,
                 heartbeat_interval: float = 0,
                 max_no_msg_count: int = 0,
                 loop=None):
        self.loop = loop or asyncio.get_running_loop()
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.reconnect_delay = 0
        self.session_mgr = TcpSessionMgr(cb,
                                         proto,
                                         heartbeat_interval,
                                         max_no_msg_count)
        self.send_buffer = []
        self._open_connection = asyncio.open_connection

    async def _start(self):
        while True:
            try:
                if is_process_closed():
                    return
                self.reader, self.writer = await self._open_connection(self.host, self.port)
                if not regist_client(self):
                    return
                await self.session_mgr.on_new_session(self.reader, self.writer, self.send_buffer)
            except Exception as e:
                logging.error(
                    f"连接[{self.host}:{self.port}]失败!异常:{e.with_traceback(None)}")
            self.send_buffer.clear()
            unregist_client(self)
            if self.reconnect_delay <= 0:
                break
            await asyncio.sleep(self.reconnect_delay, loop=self.loop)

    def start(self):
        self.read_task = self.loop.create_task(self._start())
        self.send_buffer.clear()

    def close(self, unregist=True):
        if hasattr(self, "read_task"):
            self.read_task.cancel()
        self.session_mgr.close()
        self.send_buffer.clear()
        if unregist:
            unregist_client(self)

    async def send_msg(self, data: bytes):
        if is_process_closed():
            return

        if not self.writer:
            self.send_buffer.append(data)
            return

        if self.writer.is_closing():
            return

        for session in self.session_mgr.sessions.values():
            await session.send_msg(data)

    async def send_json(self, data: dict):
        return await self.send_msg(json.dumps(data).encode())

    def enable_auto_reconnect(self, retry_interval: float):
        self.reconnect_delay = retry_interval

    def distable_auto_reconnect(self):
        self.reconnect_delay = 0
