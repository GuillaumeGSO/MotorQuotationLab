from django.urls import path
from . import views

app_name = 'Quotations'

urlpatterns = [
    path('list/', views.QuotationList.as_view(), name='quotations'),
    path('<int:id>', views.QuotationDetail.as_view(), name='quotation_detail'),
    path('create/', views.QuotationCreate.as_view(), name='create'),
]
