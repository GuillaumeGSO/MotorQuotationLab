from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from . import models
from . import forms
from django.forms import modelform_factory

# Create your views here.
from django.http import HttpResponse


def index(request):
    lst = models.Quotation.objects.all()
    return render(request, "quotations/quotation_list.html", {"quotations":lst})


def quotation(request, id):
    quotation = models.Quotation.objects.get(pk=id)
    return render(request, "quotations/quotation.html", {"quotation":quotation})

def create(request):
    if request.method=="POST":
        createform = forms.QuotationForm(request.POST)
        if createform.is_valid():
            mod=createform.cleaned_data["vehiculeModel"]
            ym=createform.cleaned_data["vehiculeYearMake"]
            t = models.Quotation(vehiculeModel=mod, vehiculeYearMake=ym)
            t.save()

            return HttpResponseRedirect("/")
    else:
        createform= modelform_factory(models.Quotation, fields=("customer","vehiculeModel","vehiculeYearMake", "vehiculeNumber","vehiculePrice", "coverages"))
        print(createform)

    return render(request, "quotations/create.html", {"form":createform })