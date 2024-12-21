from westeros.routes import api_routes as westeros_apis


from app_instance import app

all_routes = westeros_apis


def configure_app_routes():
    for route in all_routes:
        api_url = route[0]
        handler = route[1]
        methods = route[2]
        app.add_url_rule(api_url, "{}|{}".format(route, handler), handler, methods=methods)
