from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from django.shortcuts import HttpResponseRedirect


class HomePage(Page):
    def serve(self, request):
        return HttpResponseRedirect('/admin')

