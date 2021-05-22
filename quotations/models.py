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
    quotationPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    coverages = models.ManyToManyField(Coverage, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.short_creation_date(), self.customer.name, self.vehiculeModel)

    def short_creation_date(self):
        return date(self.created, "j/n/Y")
    
    def save_and_calculate(self, coverage_list):
        result = 0.00
        super(Quotation, self).save()
        if self.vehiculePrice:
            result = self.vehiculePrice * 2 / 100
        for c in coverage_list:
            self.coverages.add(c)
            result += c.price
        self.quotationPrice = result
        super(Quotation, self).save()

