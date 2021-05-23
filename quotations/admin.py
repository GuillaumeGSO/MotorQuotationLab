from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib import messages
from django.utils.translation import ngettext

from . import models

# Models in the regular admin
admin.site.register([models.Coverage])

class QuotationAdminSite(AdminSite):
    site_header = "Quotations view by Agent"
    site_title = "Quotation Admin"

quotAdmin = QuotationAdminSite(name='quotAdmin')


class QuotationModelAdmin(admin.ModelAdmin):
    list_display = ('customer','vehiculeModel', 'vehiculePrice','quotationPrice', 'modified')
    ordering = ('created','modified')
    search_fields = ['vehiculeModel']
    actions = ['send_emails', 'refresh_quotation_price']
    
    @admin.action(description='Send email to user')
    def send_emails(self, request, queryset):
        for q in queryset:
            q.send_email()
        self.message_user(request, ngettext(
            '%d email was successfully sent.',
            '%d emails were successfully sent.',
            len(queryset),
        ) % len(queryset), messages.SUCCESS)
    
    @admin.action(description='Refresh quotation price')
    def refresh_quotation_price(self, request, queryset):
        for q in queryset:
            q.quotationPrice = q.compute_quotation_price()
            q.save()
        
        self.message_user(request, ngettext(
            '%d quotation was successfully updated.',
            '%d quotation were successfully updated.',
            len(queryset),
        ) % len(queryset), messages.SUCCESS)

quotAdmin.register(models.Quotation, QuotationModelAdmin)