from rest_framework import serializers
from .models import User, UserVerification
import re

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'date_of_birth', 'email', 'gender', 'address', 'telephone', 'password', 'user_image']


class SaveUserSerializer(serializers.HyperlinkedModelSerializer):
    is_superuser = serializers.BooleanField(default=False)
    is_staff = serializers.BooleanField(default=False)
    class Meta:
        model = User
        fields = ['id', 'full_name', 'date_of_birth', 'email', 'numero_social', 'is_active','is_staff', 'is_superuser','address', 'telephone', 'password', 'remuneration','base_salary','user_image']

    def create(self, validated_data):
        return super().create(validated_data)
    """
    def validate_telephone(self, value):
        if re.fullmatch('[\+]?[0-9]{10,16}$', value) is None:
            raise serializers.ValidationError("Phone number is invalid")
        return value
    """
class UserVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVerification
        exclude = [ 'code' ]


class CreatedUserSerializer(serializers.HyperlinkedModelSerializer):
    phone_verification = UserVerificationSerializer()
    
    class Meta:
        model = User
        fields = ['id', 'full_name', 'date_of_birth', 'email', 'numero_social', 'address', 'telephone', 'phone_verification', 'remuneration','base_salary','user_image']


class DisplayUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'date_of_birth', 'email', 'numero_social', 'address', 'telephone', 'remuneration','base_salary','user_image']
    
    def create(self, validated_data):
        return super().create(validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
"""
ce serializer recois la cle primaire puis execute la requete
"""
class PhoneCodeSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    code = serializers.CharField(max_length=14)

    
