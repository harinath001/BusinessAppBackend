# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
import json


def index(request):
    return HttpResponse(json.dumps({"test": "success api"}))
