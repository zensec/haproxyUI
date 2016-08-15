from app.models.cluster import Cluster
from flask import render_template
from .base import BaseView


class Clusters(BaseView):
    def index(self):
        clusters = Cluster.query.filter_by(audit_is_deleted=False).all()
        return render_template('clusters/index.html', cluster=clusters)
