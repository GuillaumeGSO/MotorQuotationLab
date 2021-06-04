from api import serializers
from api.models import Customer, Quotation
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins

# Views utilized by Api


class QuotationList(generics.ListCreateAPIView):
    queryset = Quotation.objects.all()
    serializer_class = serializers.QuotationSerializer


class QuotationDetail(APIView):
    def get_object(self, pk):
        try:
            return Quotation.objects.get(pk=pk)
        except Quotation.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        quotation = self.get_object(id)
        serializer = serializers.QuotationSerializer(quotation)
        return Response(serializer.data)


class QuotationCreate(generics.CreateAPIView):
    serializer_class = serializers.QuotationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            quotation = Quotation.objects.get(pk=serializer.instance.id)
            quotation.quotationPrice = quotation.compute_quotation_price()
            quotation.save()
            return Response(self.get_serializer(quotation).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        cust = self.get_by_email_or_create()
        serializer.save(customer=cust)

    def get_by_email_or_create(self):
        """
        Retrieve the `:model:`Customer with the email inputed or create a new one
        """
        mail = self.request.data['email']
        cust = Customer.objects.filter(username__icontains=mail)
        if cust:
            #login(request, cust.first())
            return cust.first()

        # No user ? create one
        cust = Customer.objects.create(
            username=mail,
            last_name=self.request.data['name'],
            phone=self.request.data['phone']
        )
        cust.set_password('Tigerlab@2021')
        cust.save()
        #login(request, cust)
        return cust
