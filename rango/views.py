from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    html = "<html><body><a href = \"/rango/about/\">ABOUT</a></body></html>"
    return HttpResponse("Rango says: Here's a link to the about page: %s" % html)

def about(request):
    html = "<html><body><a href = \"/rango/\">INDEX</a></body></html>"
    return HttpResponse(html)
