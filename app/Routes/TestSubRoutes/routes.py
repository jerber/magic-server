from ..TestSubRoutes import sub_router


@sub_router.get("/sub_route")
def sub_route(name: str = "subber"):
    print(name)
    return name
