from django.contrib import admin

from .models import Customer, Quotation, Coverage

# Models in the regular admin
admin.site.register([Customer, Coverage])

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('quotationPrice', 'vehiculeModel')
    ordering = ('created','modified')
    search_fields = ['vehiculeModel']