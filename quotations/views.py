from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models
from . import forms

@login_required
def index(request):
    lst = models.Quotation.objects.filter(customer = request.user)
    return render(request, "quotations/quotation_list.html", {"quotations": lst})

@login_required
def quotation(request, id):
    quotation = models.Quotation.objects.get(pk=id)
    print(quotation)
    return render(request, "quotations/quotation.html", {"quotation": quotation})

@login_required
def create(request):
    if request.method == "POST":
        print("POST Method")
        cust = models.Customer.objects.filter(id = request.user.id)
        createform = forms.QuotationForm(request.POST)
        if createform.is_valid():
            t = models.Quotation(
                #Need to find the customer object that is the user connected
                customer=cust.first(),
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
