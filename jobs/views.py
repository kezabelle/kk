# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import swapper
from django.views.generic import DetailView
from django.views.generic import ListView


class JobDetail(DetailView):
    @property
    def model(self):
        return swapper.load_model("jobs", "Job")

    def get_slug_field(self):
        return self.model.url_field()
    @property
    def slug_url_kwarg(self):
        return self.model.url_field()

    def get_template_names(self):
        template_names = super(JobDetail, self).get_template_names()
        template_names.insert(0, "%s/%s/%s%s.html" % (
                    self.object._meta.app_label,
                    self.object._meta.model_name,
                    getattr(self.object, self.object.__class__.url_field()),
                    self.template_name_suffix
                ))
        template_names.insert(0, "%s/%s/%s%s.html" % (
                    self.object._meta.app_label,
                    self.object._meta.model_name,
                    self.object.pk,
                    self.template_name_suffix
                ))
        return template_names


class JobList(ListView):
    @property
    def model(self):
        return swapper.load_model("jobs", "Job")

job_detail = JobDetail.as_view()
job_list = JobList.as_view()
