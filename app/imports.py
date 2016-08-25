def register_blueprints(flask_app):
    from app.views.auth import Auth
    Auth.register(flask_app)

    from app.views.clusters import Clusters
    Clusters.register(flask_app)

    from app.views.servers import Servers
    Servers.register(flask_app)

    from app.views.dashboard import Dashboard
    Dashboard.register(flask_app)

    from app.views.domains import Domains
    Domains.register(flask_app)

    from app.models.server import Server
    from app.models.domain import Domain
    from app.models.log import Log

    return
