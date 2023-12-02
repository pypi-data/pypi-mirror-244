from .tcp_proto_base import TcpProtoBase
from .sym_enc_base import SymEncBase
from .tcp_simple_proto import TcpSimpleProto
from .tcp_callback_base import TcpCallbackBase
from .tcp_client import TcpClient


class TransLocalClientCallback(TcpCallbackBase):
    def __init__(self, symenc: SymEncBase,  session) -> None:
        self.enc = symenc
        self.session = session

    async def on_msg(self, session, data: bytes):
        data = self.enc.decode(data[4:])
        await self.session.send_msg(data)

    async def on_close(self, session):
        self.session.close()


class TransLocalServerCallback(TcpCallbackBase):
    def __init__(self, server_host, server_port, symenc: SymEncBase = SymEncBase()) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.enc = symenc

    async def on_connect(self, session):
        client = TcpClient(self.server_host,
                           self.server_port,
                           TransLocalClientCallback(
                               self.enc, session),
                           TcpSimpleProto())
        client.start()
        session.extra_info = client

    async def on_close(self, session):
        session.extra_info.close()

    async def on_msg(self, session, data: bytes):
        if not session.extra_info:
            session.close()
            return
        await session.extra_info.send_msg(self.enc.encode(data))


class TransServerClientCallback(TcpCallbackBase):
    def __init__(self, symenc: SymEncBase,  session) -> None:
        self.enc = symenc
        self.session = session

    async def on_msg(self, session, data: bytes):
        await self.session.send_msg(self.enc.encode(data))

    async def on_close(self, session):
        self.session.close()


class TransServerCallback(TcpCallbackBase):
    def __init__(self, server_host, server_port, symenc: SymEncBase = SymEncBase()) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.enc = symenc

    async def on_connect(self, session):
        client = TcpClient(self.server_host,
                           self.server_port,
                           TransServerClientCallback(
                               self.enc, session),
                           TcpProtoBase())
        client.start()
        session.extra_info = client

    async def on_close(self, session):
        session.extra_info.close()

    async def on_msg(self, session, data: bytes):
        if not session.extra_info:
            session.close()
            return
        await session.extra_info.send_msg(self.enc.decode(data[4:]))
