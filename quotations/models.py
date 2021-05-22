from django.db import models
from django.core.validators import MinValueValidator
from django.template.defaultfilters import date


class Customer(models.Model):
    name = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, null=False)

    def __str__(self):
        return self.name + ' (' + self.email +')'

class Coverage(models.Model):
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.description + ' - actual price : RM ' + str(self.price)

class Quotation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_quotations')
    vehiculeYearMake = models.PositiveSmallIntegerField(default=2021)
    vehiculeModel = models.CharField(max_length=80)
    vehiculeNumber = models.CharField(max_length=30, blank=True, null=True)
    vehiculePrice = models.DecimalField(max_digits=10, decimal_places=2, default=100000, validators=[MinValueValidator(30000)])
    quotationPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coverages = models.ManyToManyField(Coverage, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.short_date(self.created), self.customer.name, self.vehiculeModel)

    def short_date(self, adate):
        return date(adate, "Y/n/j")


