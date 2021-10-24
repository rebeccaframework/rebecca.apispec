from pyramid.config import Configurator


def includeme(config):
    config.add_apispec("example API", "0.1")
    config.add_route("api.index", "/")
    config.add_route("api.upload", "/upload")
    config.scan(".views")


def main(global_conf, **settings):
    with Configurator(settings=settings) as config:
        config.include("rebecca.apispec")
        config.include(".")
        return config.make_wsgi_app()
