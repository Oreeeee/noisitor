from litestar import Litestar, get


@get("/")
async def index() -> str:
    return "Hello World"


app = Litestar([index])
