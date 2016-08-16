from app.models.cluster import Cluster
from app.forms.cluster import ClusterForm
from flask import render_template, flash, redirect, url_for
from .base import BaseView


class Clusters(BaseView):
    def index(self):
        clusters = Cluster.query.filter_by(audit_is_deleted=False).all()
        return render_template('clusters/index.html', page_heading='Clusters', page_title='Clusters', clusters=clusters)

    def new(self):
        form = ClusterForm()
        return render_template('clusters/new.html', page_heading='New Cluster', page_title='New Cluster', form=form)

    def post(self):
        form = ClusterForm()
        cluster = Cluster.query.filter_by(audit_is_deleted=False, name=form.name.data).first()
        if cluster:
            flash('Cluster name already in use', 'error')
            return render_template('clusters/new.html', page_heading='New Cluster', page_title='New Cluster', form=form)
        cluster = Cluster(name=form.name.data, is_active=True)
        cluster.create()

        flash('Cluster created successfully', 'success')
        return redirect(url_for('Clusters:index'))

    def delete(self, cluster_id):
        cluster = Cluster.query.filter_by(audit_is_deleted=False, id=cluster_id).first()
        if not cluster:
            flash('Cluster not found', 'error')
            return redirect(url_for('Clusters:index'))
        if cluster.domains.filter_by(audit_is_deleted=False).count() > 0:
            flash('Active domains in this cluster, Cannot delete', 'error')
            return redirect(url_for('Clusters:index'))
        for server in cluster.servers.filter_by(audit_is_deleted=False).all():
            server.delete()
        cluster.delete()
        flash('Cluster and all associated servers deleted successfully', 'success')
        return redirect(url_for('Clusters:index'))
