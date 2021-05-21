from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib import messages
from django.utils.translation import ngettext

from . import models
import traceback


# Models in the regular admin
admin.site.register([models.Customer, models.Coverage])


class QuotationAdminSite(AdminSite):
    site_header = "Quotations view by Agent"
    site_title = "Quotation Admin"

quotAdmin = QuotationAdminSite(name='quotAdmin')




def send_emails_service(qs):
    for q in qs:
        print(q.customer.email)
    traceback.print_exc()
    return len(qs)


class QuotationModelAdmin(admin.ModelAdmin):
    list_display = ('customer','vehiculeModel','quotationPrice', 'modified')
    ordering = ('created','modified')
    search_fields = ['vehiculeModel']
    actions = ['send_emails', ]
    
    @admin.action(description='Send email to user')
    def send_emails(self, request, queryset):
        sent = send_emails_service(queryset)
        self.message_user(request, ngettext(
            '%d email was successfully sent.',
            '%d emails were successfully sent.',
            sent,
        ) % sent, messages.SUCCESS)

quotAdmin.register(models.Quotation, QuotationModelAdmin)