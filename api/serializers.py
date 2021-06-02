from rest_framework.fields import SerializerMethodField
from rest_framework import serializers
from api.models import Coverage, Quotation, Customer

class CoverageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Coverage
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ('name', 'email', 'phone')

class QuotationSerializer(serializers.ModelSerializer):

    customer = serializers.PrimaryKeyRelatedField(read_only=True)
    #quotationPrice = SerializerMethodField
    
    def get_quotationPrice():
        pass

    class Meta:
        model = Quotation
        #'name', 'email', 'phone'
        fields = ['customer','id','vehiculeYearMake', 'vehiculeModel',
                  'vehiculeNumber', 'vehiculePrice','quotationPrice',
                  'covWind', 'covPass', 'covFlood']
        #read_only_fields = ['quotationPrice']
    
