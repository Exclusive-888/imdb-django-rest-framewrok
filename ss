
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_complete_user(self, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=UserManager.normalize_email(email),
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email"""
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CiceroUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=180, null=True)
    email = models.EmailField(unique=True)
    clinic_name = models.CharField(max_length=256, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email




=======================================
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password

from .models import CiceroUser


class UserCreateSerializer(serializers.ModelSerializer):
    """CiceroUser Registration"""
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    Confirm_Password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CiceroUser
        fields = ['full_name', 'clinic_name', 'email', 'password', 'Confirm_Password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        cicerouser = CiceroUser(
            full_name=self.validated_data['full_name'],
            clinic_name=self.validated_data['clinic_name'],
            email=self.validated_data['email'],
            password=self.validated_data['password'],

        )
        password = self.validated_data['password']
        Confirm_Password = self.validated_data['Confirm_Password']
        if password != Confirm_Password:
            raise serializers.ValidationError({'Confirm Password': 'Passwords Not match.'})
        cicerouser.set_password(password)
        cicerouser.save()
        return cicerouser


class UserLoginSerializer(serializers.ModelSerializer):
    """CiceroUser Login"""
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        write_only=True,
        label="Email Address"
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta(object):
        model = CiceroUser
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if not email:
            raise serializers.ValidationError({
                'email': 'Please enter email'
            })
        user = CiceroUser.objects.filter(
            Q(email=email)
        ).exclude(
            email__isnull=True
        ).exclude(
            email__iexact=''
        ).distinct()

        """Check CiceroUser Register or Not!"""

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError({
                'email': 'This email not registered!'
            })

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError({
                    'email or password': 'Invalid credentials!'
                })

        return data


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    Confirm_Password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CiceroUser
        fields = ('old_password', 'password', 'Confirm_Password')

    def validate(self, attrs):
        if attrs['password'] != attrs['Confirm_Password']:
            raise serializers.ValidationError({"Confirm password": "Password didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance
======================================
from rest_framework import generics, status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CiceroUser
from .serializers import UserLoginSerializer, UserCreateSerializer, ChangePasswordSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)
    queryset = CiceroUser.objects.all()


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny, ]

    @staticmethod
    def post(request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"status": status.HTTP_200_OK})


class ChangePasswordView(generics.UpdateAPIView):

    queryset = CiceroUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    
    
    
    ============
    from django.urls import path
from rest_framework import routers

from .views import UserCreateAPIView, UserLoginAPIView, ChangePasswordView

router = routers.SimpleRouter()
router.register('register/', UserCreateAPIView)


urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name="user-login"),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),

]
