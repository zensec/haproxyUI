from app.models.upstream import Upstream
from app.models.domain import Domain
from app.helpers import log
from flask import render_template, flash, redirect, url_for
from .base import BaseView
from app.forms.upstream import UpstreamForm


class Upstreams(BaseView):
    route_base = '/domains/<domain_name>/upstreams'

    def new(self, domain_name):
        domain = self._get_domain(domain_name=domain_name)
        if not domain:
            flash('Domain not found', 'error')
            return redirect(url_for('Domains:index'))
        return self._new_upstream_return(domain)

    def post(self, domain_name):
        form = UpstreamForm()
        domain = self._get_domain(domain_name=domain_name)
        if not domain:
            flash('Domain not found', 'error')
            return redirect(url_for('Domains:index'))
        upstream = Upstream(domain_id=domain.id, ip_address=form.ip_address.data, port=form.port.data)
        upstream.create()

        log(upstream.id)
        flash('Upstream created successfully', 'success')
        return redirect(url_for('Domains:get', domain_name=domain.name))

    def delete(self, domain_name, upstream_id):
        domain = self._get_domain(domain_name=domain_name)
        if not domain:
            flash('Domain not found', 'error')
            return redirect(url_for('Domains:index'))
        upstream = Upstream.query.filter_by(audit_is_deleted=False, id=upstream_id, domain_id=domain.id).first()
        if not upstream:
            flash('Upstream not found', 'error')
        upstream.delete()
        log(upstream.id)
        flash('Upstream deleted successfully', 'success')
        return redirect(url_for('Servers:index'))

    def _get_domain(self, domain_id=None, domain_name=None):
        filter_args = {'audit_is_deleted': False}
        if domain_id:
            filter_args['id'] = domain_id
        if domain_name:
            filter_args['name'] = domain_name
        return Domain.query.filter_by(**filter_args).first()

    def _new_upstream_return(self, domain):
        form = UpstreamForm()
        log()
        return render_template('upstreams/new.html', page_heading='New upstream for domain {0}'.format(domain.name),
                               page_title='New upstream for domain {0}'.format(domain.name), form=form, domain=domain)
