import ssl
from ssl import SSLContext

from websockets import connect

from app.config import config
from app.multiplayer.auth import authenticate

def setup_context() -> ssl.SSLContext:
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.load_verify_locations(cafile=config.local_key)
    return ssl_context


class Client:
    def __init__(self):
        self.ssl_context: SSLContext | bool = setup_context() if config.env == "dev" else True
        self.uri: str = config.server_url
        self.headers: dict[str, str] = {}

    async def authenticate(self) -> None:
        auth_token = await authenticate()
        self.headers["Authorization"] = f"Bearer {auth_token}"

    async def connect(self) -> None:
        await self.authenticate()
        async with connect(self.uri, ssl=self.ssl_context, extra_headers=self.headers) as ws:
            msg = "Hello world"
            await ws.send(msg)
            print(f">>> {msg}")
            resp = await ws.recv()
            print(f"<<< {resp}")
