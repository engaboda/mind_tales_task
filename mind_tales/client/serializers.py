import logging
from rest_framework import serializer
from django.contrib.auth.models import User
from .models import Restaurant, Menu, Employee, Vote
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .exception import NotFoundSerializerContext
from .restaurant_hidden_field import CurrentRestaurantDefault

logger = logging.getLogger(__name__)


class UserCreateSerializer(serializer.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')


class RestaurantCreateSerializer(serializer.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Restaurant
        fields = '__all__'


class TokenRefreshSerializer(serializer.Serializer):
    access = serializer.SerializerMethodField(max_length=255)
    refresh = serializer.SerializerMethodField(max_length=255)

    def get_access(self, object):
        try:
            return str(
                AccessToken()\
                .for_user(self.context.get('user'))
            )
        except NotFoundSerializerContext as context_error:
            logger.error(f'Access Token Context Not Found: {context_error}')
        except Exception as error:
            logger.error(f'Access Token Error: {error}')

    def get_refresh(self, object):
        try:
            return str(
                RefreshToken()\
                .for_user(self.context.get('user'))
            )
        except NotFoundSerializerContext as context_error:
            logger.error(f'Refresh Token Context Not Found: {context_error}')
        except Exception as error:
            logger.error(f'Refresh Token Error: {error}')


class MenuCreateSerializer(serializer.ModelSerializer):
    restaurant = serializers.HiddenField(default=serializers.CurrentRestaurantDefault())

    class Meta:
        model = Menu
        fields = '__all__'


class EmployeeCreateSerializer(serializer.ModelSerializer):
    restaurant = serializers.HiddenField(default=serializers.CurrentRestaurantDefault())

    class Meta:
        model = Employee
        fields = '__all__'


class MenuetreiveSerializer(serializer.ModelSerializer):

    class Meta:
        model = Menu
        fields = ('name', )


class VoteCreateSerializer(serializer.ModelSerializer):
    employee = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vote
        fields = ('menu', )


class VoteCheckOldVersionSerializer(serializer.ModelSerializer):
    employee = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vote
        fields = ('menu', )