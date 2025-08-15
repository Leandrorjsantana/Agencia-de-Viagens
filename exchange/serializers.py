# exchange/serializers.py
from rest_framework import serializers

class CurrencyRateSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    high = serializers.CharField()
    low = serializers.CharField()
    varBid = serializers.CharField()
    pctChange = serializers.CharField()
    bid = serializers.CharField()
    ask = serializers.CharField()
    timestamp = serializers.CharField()