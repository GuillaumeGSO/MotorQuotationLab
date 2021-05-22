from django.shortcuts import render
from . import models 

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, "quotations/base.html", {})


def quotation(request, id):
    quotation = models.Quotation.objects.get(pk=id)
    return render(request, "quotations/quotation.html", {"quotation":quotation})
