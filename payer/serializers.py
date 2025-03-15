from rest_framework import serializers
from .models import PayerGroups, Payers, PayerDetails

class PayerGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayerGroups
        fields = '__all__'

class PayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payers
        fields = '__all__'

class PayerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayerDetails
        fields = '__all__'