from .models import *
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from usersapp.models import *
from django.utils.text import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(max_length=155,min_length=3,required=True)
    name = serializers.CharField(max_length=55,min_length=3,required=True)

    class Meta:
        model = UserProfile
        fields = ("id","name", "email", "password","gender")
        # fields="__all__"


    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = UserProfile
        fields = ['token']


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    '''field for entering the refresh token'''
    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }
    '''if token is expired or invalid it will raise this exception message'''

    def validate(self, attrs):
        self.token = attrs['refresh']
        '''validateing the given token and returning'''
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
            '''getting the token and put in the blacklist'''
        except TokenError:
            self.fail('bad_token')



class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50,min_length=6,write_only=True)
    name = serializers.CharField(max_length=255,min_length=3,read_only=True)
    tokens = serializers.CharField(max_length=135,min_length=6,read_only=True)
    email = serializers.EmailField(max_length=155,min_length=6,write_only=True)

    class Meta:
        model = UserProfile
        fields = ['id','password','name','tokens','email']


    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email,password=password)
        # import pdb
        # pdb.set_trace()
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled , contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('user is not verified')

        return {
            'id':user.id,
            'mobile': user.email,
            'name': user.name,
            'tokens': user.tokens,

        }


