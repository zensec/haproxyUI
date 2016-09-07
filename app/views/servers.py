from app.models.server import Server
from app.models.cluster import Cluster
from app.forms.server import ServerForm
from app.helpers import log
from flask import render_template, flash, redirect, url_for
from .base import BaseView


class Servers(BaseView):
    route_base = '/clusters/<cluster_id>/servers'

    def index(self, cluster_id):
        cluster = Cluster.query.filter_by(audit_is_deleted=False, id=cluster_id).first()
        if not cluster:
            flash('Cluster not found', 'error')
            return redirect(url_for('Clusters:index'))
        servers = cluster.servers.filter_by(audit_is_deleted=False).all()

        log()
        return render_template('servers/index.html', page_heading='Servers',
                               page_title='Servers', servers=servers, cluster=cluster)

    def new(self, cluster_id):
        cluster = Cluster.query.filter_by(audit_is_deleted=False, id=cluster_id).first()
        if not cluster:
            flash('Cluster not found', 'error')
            return redirect(url_for('Clusters:index'))
        return self._new_server_return(cluster)

    def post(self, cluster_id):
        form = ServerForm()
        cluster = Cluster.query.filter_by(audit_is_deleted=False, id=cluster_id).first()
        if not cluster:
            flash('Cluster not found', 'error')
            return redirect(url_for('Clusters:index'))
        server = Server.query.filter_by(audit_is_deleted=False, name=form.name.data).first()
        if server:
            flash('Server name already in use', 'error')
            return self._new_server_return()
        server = Server(name=form.name.data, is_active=True, cluster_id=cluster_id)
        server.create()

        log(server.id)
        flash('Server created successfully', 'success')
        return redirect(url_for('Clusters:index'))

    def delete(self, cluster_id, server_id):
        cluster = Cluster.query.filter_by(audit_is_deleted=False, id=cluster_id).first()
        if not cluster:
            flash('Cluster not found', 'error')
            return redirect(url_for('Clusters:index'))

        server = Server.query.filter_by(audit_is_deleted=False, id=server_id).first()
        if not server:
            flash('Server not found', 'error')
            return redirect(url_for('Servers:index'))
        if server.cluster.domains.filter_by(audit_is_deleted=False).count() > 0:
            flash('Active domains in this server, Cannot delete', 'error')
            return redirect(url_for('Servers:index', cluster_id=cluster.id))
        for server in server.servers.filter_by(audit_is_deleted=False).all():
            server.delete()
        server.delete()

        log(server.id)
        flash('Server deleted successfully', 'success')
        return redirect(url_for('Servers:index', cluster_id=cluster.id))

    def _new_server_return(self, cluster):
        form = ServerForm()
        log()
        return render_template('servers/new.html', page_heading='New Server',
                               page_title='New Server', form=form, cluster=cluster)
