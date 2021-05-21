from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from . import models

class QuotationAdminSite(AdminSite):
    site_header = "Quotations view by Agent"

quotAdmin = QuotationAdminSite(name='quotAdmin')


# Models in the regular admin
admin.site.register([models.Customer, models.Coverage])


#custom view for quotation admin
class QuotationModelAdmin(admin.ModelAdmin):
    list_display = ('quotationPrice', 'vehiculeModel')
    ordering = ('created','modified')
    search_fields = ['vehiculeModel']
    quotAdmin.register(models.Quotation)