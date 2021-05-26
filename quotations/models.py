from django.db import models
from django.contrib.auth import login, models as authModel
from django.core.validators import MinValueValidator
from django.db.models.expressions import Exists
from django.template.defaultfilters import date
from io import BytesIO
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


class Customer (authModel.User):
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.last_name + ' (' + self.email + ')'


class Coverage(models.Model):
    name = models.CharField(max_length=8, primary_key=True)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.name} : {self.description}  - actual price : RM  {str(self.price)}'


def get_coverage_price_by_name(covname):
    print("search for : ", covname)
    print(Coverage.objects.all())
    try:
        obj = Coverage.objects.get(name=covname)
    except ObjectDoesNotExist:
        return 0
    print(obj)
    return obj.price


class Quotation(models.Model):
    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="quotations")
    vehiculeYearMake = models.PositiveSmallIntegerField(default=2021)
    vehiculeModel = models.CharField(max_length=80)
    vehiculeNumber = models.CharField(max_length=30)
    vehiculePrice = models.DecimalField(
        max_digits=10, decimal_places=2, default=100_000,
        validators=[MinValueValidator(30_000)])
    quotationPrice = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, editable=False)
    covWind = models.BooleanField(choices=BOOL_CHOICES,
                                  default=False, verbose_name="Windscreen coverage")
    covPass = models.BooleanField(choices=BOOL_CHOICES,
                                  default=False,
                                  verbose_name="Passenger liability coverage")
    covFlood = models.BooleanField(choices=BOOL_CHOICES,
                                   default=False,
                                   verbose_name="Flood, Windstorm,Landslide or Subsidence coverage")
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('quotation', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.short_creation_date()} - {self.customer.email} - {self.vehiculeModel} - {self.quotationPrice}'

    def short_creation_date(self):
        return date(self.created, "j/n/Y")

    def calculate_and_save(self):
        # Calculate the quotation price
        self.quotationPrice = self.compute_quotation_price()
        self.save()

    def compute_quotation_price(self):
        result = 0.0
        if self.vehiculePrice:
            result = self.vehiculePrice * 2 / 100
        if self.covWind:
            result += get_coverage_price_by_name("WIND")
        if self.covPass:
            result += get_coverage_price_by_name("PASS")
        if self.covFlood:
            result += get_coverage_price_by_name("FLOOD")
        return result

    def generate_pdf(self):
        x = 100
        y = 100
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize="A4")
        p.drawString(x, y, "TO DO")
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    def send_email(self):
        EmailMsg = EmailMessage("Your quotation", "Please fin attached the quotation you requested", 'no-reply@email.com', [
            self.customer.email], headers={'Reply-To': 'no-reply@email.com'})
        pdf = self.generate_pdf()
        EmailMsg.attach('yourChoosenFileName.pdf', pdf, 'application/pdf')
        # Use True when able to handle exception
        # see in settings.py for EMAIL_BACKEND configuration
        EmailMsg.send(fail_silently=False)
