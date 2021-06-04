from django.urls import path
from . import views

app_name = 'Quotations'

urlpatterns = [
    path('coverages/', views.CoverageView.as_view(), name='coverages'),
    path('', views.QuotationList.as_view(), name='quotations'),
    path('<int:id>', views.QuotationDetail.as_view(), name='quotation_detail'),
    path('create/', views.QuotationList.as_view(), name='create'),
]
