#(©)Codexbotz
#rymme

from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("CodeXBotz")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.router.add_routes(routes)
    return web_app