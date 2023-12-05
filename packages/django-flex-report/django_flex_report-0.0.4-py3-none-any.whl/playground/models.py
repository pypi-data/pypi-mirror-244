from django.db import models
from django.utils.translation import gettext_lazy as _

from report import report_model


@report_model.register
class Test(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"))

    @classmethod
    def report_search_fields(cls):
        return ["title"]
