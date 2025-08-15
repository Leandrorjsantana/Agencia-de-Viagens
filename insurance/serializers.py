# insurance/serializers.py
from rest_framework import serializers
from .models import InsuranceBenefit, InsurancePlan, InsuranceFAQ, TrustSeal

class InsuranceBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceBenefit
        # Adicionando o novo campo 'long_description'
        fields = ('title', 'description', 'long_description', 'icon_class')

class InsurancePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsurancePlan
        fields = ('name', 'price_info', 'features', 'is_popular')

class InsuranceFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceFAQ
        fields = ('question', 'answer')

class TrustSealSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrustSeal
        fields = ('name', 'logo')

# Este é o "pacote" de dados completo para a página
class InsurancePageDataSerializer(serializers.Serializer):
    benefits = InsuranceBenefitSerializer(many=True)
    plans = InsurancePlanSerializer(many=True)
    faqs = InsuranceFAQSerializer(many=True)
    seals = TrustSealSerializer(many=True)