# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile
from django.db import transaction
from django.utils.translation import gettext_lazy as _

# --------------------------------------------------------------------
# NOVO: Serializer para exibir e atualizar os dados do perfil
# --------------------------------------------------------------------
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # Lista dos campos do perfil que queremos que a API manipule
        fields = ('full_name', 'cpf', 'phone_number', 'cep', 'logradouro', 'numero', 'bairro', 'cidade', 'estado')

class UserProfileSerializer(serializers.ModelSerializer):
    # Aninhamos o ProfileSerializer aqui. A API retornará os dados do User e do Profile juntos.
    profile = ProfileSerializer()

    class Meta:
        model = User
        # Lista dos campos do User que queremos expor na API de perfil
        fields = ('username', 'email', 'profile')
        read_only_fields = ('username',) # O nome de usuário não pode ser alterado

    @transaction.atomic
    def update(self, instance, validated_data):
        # Lógica para atualizar dados aninhados (o perfil dentro do usuário)
        profile_data = validated_data.pop('profile', {})
        profile_serializer = ProfileSerializer(instance.profile, data=profile_data, partial=True)
        
        if profile_serializer.is_valid(raise_exception=True):
            profile_serializer.save()

        # Atualiza os campos do User (ex: email)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance

# --------------------------------------------------------------------
# Serializers de Registro e Login (JÁ EXISTENTES E FUNCIONAIS)
# --------------------------------------------------------------------
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
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False, required=True)

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')
        user = None
        if '@' in login:
            try:
                user_obj = User.objects.get(email=login)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        else:
            user = authenticate(username=login, password=password)
        if not user:
            msg = 'Credenciais inválidas. Por favor, tente novamente.'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs