# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context
import json

# Create your views here.

def index(request):
    f = open("frontend/templates/home.html", "r")
    content = f.read()
    f.close()
    t = Template(content)
    c = Context({})
    return HttpResponse(t.render(context=c))