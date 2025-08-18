# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile
from django.db import transaction

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_picture', 'full_name', 'cpf', 'phone_number', 'cep', 'logradouro', 'numero', 'bairro', 'cidade', 'estado')

class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'profile')
        read_only_fields = ('username',)

    @transaction.atomic
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # Passa os ficheiros (a foto) para o serializer do perfil
        profile_serializer = ProfileSerializer(instance.profile, data=profile_data, partial=True, context=self.context)
        
        if profile_serializer.is_valid(raise_exception=True):
            profile_serializer.save()

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance

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
        
        # --- LÓGICA INTELIGENTE ADICIONADA AQUI ---
        # Pega o nome completo do perfil e divide-o
        full_name = profile_data.get('full_name', '').strip()
        if full_name:
            name_parts = full_name.split(' ', 1)
            user.first_name = name_parts[0]
            if len(name_parts) > 1:
                user.last_name = name_parts[1]
            user.save()
        
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