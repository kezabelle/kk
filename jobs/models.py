from __future__ import unicode_literals

import swapper
from django.db import models
from django.utils.encoding import force_str


class BaseJob(models.Model):
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_short_description(self):
        msg = ("Concrete (non-abstract) classes should implement this to "
               "return a suitable short description or summary of this job")
        raise NotImplementedError(msg)

    def __str__(self):
        return self.title

    def __repr__(self):
        return force_str('<%s.%s: title="%s">' % (
            self._meta.app_label, self.__class__.__name__, self.title
        ))

    class Meta:
        abstract = True


class Job(BaseJob):
    summary = models.TextField()

    def get_short_description(self):
        return self.summary

    class Meta:
        swappable = swapper.swappable_setting('jobs', 'Job')
