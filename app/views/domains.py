from .base import BaseView
from flask import render_template, redirect, flash, url_for
from app.helpers import log
from app.models.domain import Domain
from app.models.cluster import Cluster
from app.forms.domain import DomainForm


class Domains(BaseView):
    def index(self):
        domains = self._get_domains()
        form = self._generate_domain_form()

        log()
        return render_template('domains/index.html', page_tite='All Domains', page_heading='All Domains',
                               domains=domains, form=form)

    def get(self, domain_name):
        domain = self._get_domain(domain_name=domain_name)
        if not domain:
            flash('Domain not found', 'error')
            return redirect(url_for('Domains:index'))
        log()
        return render_template('domains/show.html', page_title='Domain {0}'.format(domain.name),
                               page_heading='Domain {0}'.format(domain.name), domain=domain)

    def new(self):
        return self._new_domain_return()

    def post(self):
        form = self._generate_domain_form()

        cluster = Cluster.query.filter_by(audit_is_deleted=False, id=form.cluster_id.data).first()
        if not cluster:
            flash('Cluster not found', 'error')
            return self._new_domain_return()

        domain = self._get_domain(domain_name=form.name.data)
        if domain:
            flash('Domain name already exists', 'error')
            return self._new_domain_return()

        domain = Domain(name=form.name.data, is_active=True, cluster_id=cluster.id)
        domain.create()

        log(domain.id)
        flash('Domain created successfully', 'success')
        return redirect(url_for('Domains:index'))

    def delete(self, domain_name):
        domain = self._get_domain(domain_name=domain_name)
        if not domain:
            flash('Domain not found', 'error')
            return redirect(url_for('Domains:index'))
        domain.delete()
        flash('Domain deleted successfully', 'success')
        return redirect(url_for('Domains:index'))

    def _get_domain(self, domain_id=None, domain_name=None):
        filter_args = {'audit_is_deleted': False}
        if domain_id:
            filter_args['id'] = domain_id
        if domain_name:
            filter_args['name'] = domain_name
        return Domain.query.filter_by(**filter_args).first()

    def _get_domains(self):
        return Domain.query.filter_by(audit_is_deleted=False).all()

    def _new_domain_return(self):
        form = self._generate_domain_form()
        log()
        return render_template('domains/new.html', page_heading='New Domain',
                               page_title='New Domain', form=form)

    def _generate_domain_form(self):
        form = DomainForm()
        form.generate_cluster_id_options()
        return form
