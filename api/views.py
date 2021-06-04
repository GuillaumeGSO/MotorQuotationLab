from api import serializers
from api.models import Coverage, Customer, Quotation
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

# Views utilized by Api


class CoverageView(generics.ListAPIView):
    """
    Return all the :model:Coverage from the database
    GET only
    """
    queryset = Coverage.objects.all()
    serializer_class = serializers.CoverageSerializer


class QuotationDetail(generics.RetrieveAPIView):
    """
    Return a :model:Quotation with details by its id
    """
    serializer_class = serializers.QuotationSerializer
    queryset = Quotation.objects.all()
    lookup_field = 'id'


class QuotationList(generics.ListCreateAPIView):
    """
    Get : list of all the :model:Quotation
    Post : create a new :model:Quotation with :model:Customer creation if not yet in the :model:User base.
    The email adress is used for Customer creation
    """
    queryset = Quotation.objects.all()
    serializer_class = serializers.QuotationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            quotation = Quotation.objects.get(pk=serializer.instance.id)
            quotation.quotationPrice = quotation.compute_quotation_price()
            quotation.save()
            return Response(self.get_serializer(quotation).data,
                            status=status.HTTP_201_CREATED)
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
            email=mail,
            phone=self.request.data['phone']
        )
        cust.set_password('Tigerlab@2021')
        cust.save()
        #login(request, cust)
        return cust



