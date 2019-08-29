import aiohttp


class WebApp:
    DEFAULT_PORT = 8180
    DEFAULT_ADDR = '127.0.0.1'

    def __init__(self, addr, port):
        self.addr = self.DEFAULT_ADDR if addr is None else addr
        self.port = self.DEFAULT_PORT if port is None else port

        self.app = aiohttp.web.Application()
    

    @routes.get('/')
    async def root(req):
        return 
