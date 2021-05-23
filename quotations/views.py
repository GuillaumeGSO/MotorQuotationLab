from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from . import models
from . import forms

# Create your views here.
from django.http import HttpResponse


def index(request):
    lst = models.Quotation.objects.all()
    return render(request, "quotations/quotation_list.html", {"quotations": lst})


def quotation(request, id):
    quotation = models.Quotation.objects.get(pk=id)
    return render(request, "quotations/quotation.html", {"quotation": quotation})


def create(request):
    print(request.method)
    if request.method == "POST":
        print("POST Method")
        createform = forms.QuotationForm(request.POST)
        if createform.is_valid():

            t = models.Quotation(
                customer=createform.cleaned_data["customer"],
                vehiculeModel=createform.cleaned_data["vehiculeModel"],
                vehiculeYearMake=createform.cleaned_data["vehiculeYearMake"],
                vehiculeNumber=createform.cleaned_data["vehiculeNumber"],
                vehiculePrice=createform.cleaned_data["vehiculePrice"],
            )
            t.save_and_calculate(createform.cleaned_data["coverages"])
            t.send_email()
            return HttpResponseRedirect("/quotation/" + str(t.id))
    else:
        createform = forms.QuotationForm()

    return render(request, "quotations/create.html", {"form": createform})
