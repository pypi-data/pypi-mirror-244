import logging
import asyncio
import json
from typing import Callable
from .tcp_callback_base import TcpCallbackBase

wait_futures = {}
max_serial_id = 0


def gen_serial_id():
    global max_serial_id
    max_serial_id += 1
    return max_serial_id


class JsonHandler(TcpCallbackBase):
    def __init__(self, ) -> None:
        self._handlers = {}

    def regist_handler(self, fn):
        self._handlers[fn.__name__] = fn

    async def on_msg(self, session, data: bytes):
        id = session.id
        json_data = data[4:].decode('utf8')
        logging.info(json_data)
        try:
            data: dict = json.loads(json_data)
        except Exception as e:
            logging.error(e.with_traceback(None))
            logging.error(f"Error data = {json_data}")
            return

        func_name = data.get("name")
        args = data.get("args")

        # 检查参数
        if func_name is None or args is None:
            return

        # 检查是否是返回值
        fu: asyncio.Future = wait_futures.get(func_name)
        if fu is not None:
            del wait_futures[func_name]
            if fu.cancelled():
                return
            fu.set_result(args)
            return

        func = self._handlers.get(func_name)
        if func is None:
            logging.error(f"no such handler named {func_name}")
            return

        try:
            ret = await func(id, *args)
        except Exception as e:
            logging.error(f"execute {func_name} error!" + str(e.with_traceback(None)))

        serial_id = data.get("serial_id")
        if serial_id:
            return json.dumps({
                "name": serial_id,
                "args": ret
            }).encode()


async def json_rpc(send_msg: Callable, name, *args, has_return=False):
    if has_return:
        serial_id = gen_serial_id()
        ret = asyncio.Future(loop=asyncio.get_running_loop())
        wait_futures[serial_id] = ret
        msg = {"name": name,
               "args": args,
               "serial_id": serial_id}
        if not await send_msg(json.dumps(msg).encode()):
            logging.error(f"call function [{name}] error: send msg error!")
            return

        try:
            return await asyncio.wait_for(ret, 5)
        except Exception as e:
            logging.error(f"call server function [{name}] error: {e.with_traceback(None)}!")
            return
    else:
        msg = {"name": name, "args": args}
        return await send_msg(json.dumps(msg).encode())
