from django.db import models
from django.core.validators import MinValueValidator
from django.template.defaultfilters import date
from io import BytesIO
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage


class Customer(models.Model):
    name = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, null=False)

    def __str__(self):
        return self.name + ' (' + self.email + ')'


class Coverage(models.Model):
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.description + ' - actual price : RM ' + str(self.price)


class Quotation(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)
    vehiculeYearMake = models.PositiveSmallIntegerField(default=2021)
    vehiculeModel = models.CharField(max_length=80)
    vehiculeNumber = models.CharField(max_length=30, blank=True, null=True)
    vehiculePrice = models.DecimalField(
        max_digits=10, decimal_places=2, default=100000, validators=[MinValueValidator(30000)])
    quotationPrice = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, editable=False)
    coverages = models.ManyToManyField(Coverage, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.short_creation_date(), self.customer.name, self.vehiculeModel, self.quotationPrice)

    def short_creation_date(self):
        return date(self.created, "j/n/Y")

    def save_and_calculate(self, coverage_list):
        if not self.id:
            # this first save creates the id before the m2m save
            self.save()
        self.coverages.clear()
        for c in coverage_list:
            self.coverages.add(c)
        # Calculate the quotation price
        self.quotationPrice = self.compute_quotation_price()
        self.save()

    def compute_quotation_price(self):
        result = 0
        if self.vehiculePrice:
            result = self.vehiculePrice * 2 / 100
        for c in self.coverages.all():
            result += c.price
        return result

    def generate_pdf(self):
        x = 100
        y = 100
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize="letter")
        p.drawString(x, y, "TO DO")
        p.showPage()
        p.save()

        # FIXME : i'd like to write temporairly the pdf file so i can visualize it
        pdf = buffer.getvalue()
        f = open("tmp.pdf", "wb")
        f.write(pdf)
        f.close()
        # end FIXME

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
