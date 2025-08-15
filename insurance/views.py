# insurance/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import InsuranceBenefit, InsurancePlan, InsuranceFAQ, TrustSeal
from .serializers import InsurancePageDataSerializer

class InsurancePageDataView(APIView):
    """
    Entrega todos os dados necessários para a página de Seguro Viagem de uma só vez.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        # Busca todos os dados dos diferentes modelos
        benefits = InsuranceBenefit.objects.all()
        plans = InsurancePlan.objects.all()
        faqs = InsuranceFAQ.objects.all()
        seals = TrustSeal.objects.all()

        # Monta o "pacote" de dados
        data = {
            'benefits': benefits,
            'plans': plans,
            'faqs': faqs,
            'seals': seals,
        }

        # Usa o serializer para formatar os dados
        serializer = InsurancePageDataSerializer(data, context={'request': request})
        return Response(serializer.data)