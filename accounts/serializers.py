# accounts/serializers.py

from rest_framework import serializers
# --- CORREÇÃO AQUI: Importando 'authenticate' que faltava ---
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile
from django.db import transaction
from django.utils.translation import gettext_lazy as _

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('full_name', 'cpf', 'phone_number', 'cep', 'logradouro', 'numero', 'bairro', 'cidade', 'estado')

class RegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Profile.objects.create(user=user, **profile_data)
        return user

class CustomLoginSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        required=True
    )

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')
        user = None

        if '@' in login:
            try:
                user_obj = User.objects.get(email=login)
                # Agora o 'authenticate' vai funcionar
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        else:
            # E aqui também
            user = authenticate(username=login, password=password)

        if not user:
            msg = 'Credenciais inválidas. Por favor, tente novamente.'
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs