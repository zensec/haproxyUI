from flask import render_template, g
from .base import BaseView
from app.models.server import Server
from app.models.domain import Domain
from app.models.cluster import Cluster
from app.helpers import log


class Dashboard(BaseView):
    def index(self):
        stats = {
            'online_servers': Server.query.filter_by(audit_is_deleted=False, is_active=True).count(),
            'active_domains': Domain.query.filter_by(audit_is_deleted=False, is_active=True).count(),
            'active_clusters': Cluster.query.filter_by(audit_is_deleted=False, is_active=True).count()
        }
        log()
        return render_template('dashboard/index.html',
                               page_title='Dashboard',
                               page_heading='Dashboard',
                               stats=stats)
