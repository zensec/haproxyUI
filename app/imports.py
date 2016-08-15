def register_blueprints(flask_app):
    from app.views.login import Login
    Login.register(flask_app)

    from app.views.clusters import Clusters
    Clusters.register(flask_app)
    return
