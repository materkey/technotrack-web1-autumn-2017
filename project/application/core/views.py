# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.

def price(request, variable):

    return HttpResponse("Product  #" + variable + " costs: " + str(int(variable)/3) + " rubles")


def content(request, post_id = None):

    return render(request, 'post.html', {'post_id' : post_id})


def main(request):

    return HttpResponse("Main page of edu-purpose web-app")
