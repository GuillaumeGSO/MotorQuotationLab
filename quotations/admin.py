from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.template.defaultfilters import register

from . import models

# Models in the regular admin
admin.site.register([models.Customer, models.Coverage])


class QuotationAdminSite(AdminSite):
    site_header = "Quotations view by Agent"
    site_title = "Quotation Admin"

quotAdmin = QuotationAdminSite(name='quotAdmin')


#custom view for quotation admin

class QuotationModelAdmin(admin.ModelAdmin):
    list_display = ('customer','vehiculeModel','quotationPrice', 'modified')
    ordering = ('created','modified')
    search_fields = ['vehiculeModel']

quotAdmin.register(models.Quotation, QuotationModelAdmin)