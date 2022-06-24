from datetime import datetime

from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from .serializers import (
    UserCreateSerializer, RestaurantCreateSerializer, TokenRefreshSerializer,
    MenuCreateSerializer, EmployeeCreateSerializer, VoteCreateSerializer
)
from rest_framework.response import Response
from .permissions import IsRestaurantAdmin
from django.contrib.auth.models import User
from django.db.models import Count


class UserViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = UserCreateSerializer
    permission_classes = None

    def get_user(self, **kwargs):
        return User.objects.get(**kwargs)

    def create(self, request, *args, **kwargs):
        serializer_data = super().create(request, *args, **kwargs)
        
        access_info = TokenRefreshSerializer(
            context={'user': self.get_user(serializer_data.data)}
        ).data

        return Response(access_info, status=status.HTTP_201_CREATED)


class RestaurantViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = RestaurantCreateSerializer


class MenuCreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = MenuCreateSerializer 
    permission_classes = (IsRestaurantAdmin, )

    def get_serializer_context(self):
        return {
            'restaurant': self.request.user.restaurant
        }

    def create(self, request, *args, **kwargs):
        serializer_data = super().create(request, *args, **kwargs)
        return Response(serializer_data, status=status.HTTP_201_CREATED)


class RetrieveCurrentDayMenu(APIView):
    permission_classes = (IsRestaurantAdmin)

    def get(self, request):
        highest_vote = Vote.objects.values('menu_date').annotate(
            total_vote=Count('id')
        ).order_by('total').last()
        serializer_data = MenuetreiveSerializer(highest_vote.menu).data
        return Response(serializer_data, status=status.HTTP_200_OK)


class EmployeeViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = EmployeeCreateSerializer
    permission_classes = (IsRestaurantAdmin, )

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = User.objects.create(
            **serializer.data
        )
        
        restaurant = request.user.restaurant

        employee_create_data = {
            'user': user,
            'restraurant': restraurant,
            'name': request.data.get('name', None)
        }

        employee_serializer = EmployeeCreateSerializer(data=employee_create_data)
        employee_serializer.is_valid(raise_exception=True)
        self.perform_create(employee_serializer)

        access_info = TokenRefreshSerializer(
            context={'user': user}
        ).data

        return Response({**access_info, **employee_serializer.data}, status=HTTP_201_CREATED)

    def perform_create(serializer):
        serializer.save()


class VoteCreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = VoteCreateSerializer
    permission_classes = (IsEmployee, )

    def create(self, request, *args, **kwargs):
        # get serializer data
        serializer = VoteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # is thie menu can accept vote
        menue_total_vote = Vote.objects.fiter(menu=serializer.data.get('menu')).count()
        if menue_total_vote == 3:
            return Response({'messsage': 'vote exceed'}, status=status.HTTP_200_OK)

        employee = request.user.employee

        # check if employee already voted (old version)
        already_voted = employee.votes.filter(menu__menu_date=datetime.now().date()).exists()
        if already_voted:
            return Response({'message': 'already voted'}, status=HTTP_200_OK)
        else:
            serializer = VoteCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Done'}, status=HTTP_200_OK)

        # new version can vote for top three menu
        top_three = Vote.objects.filter(menu__menu_date=datetime.now().date()) \
        .values('menu') \
        .annotate(
            total_vote=Count('id')
        ) \
        .filter(
            total_vote__in=[1, 2, 3]
        )

        # vote to top three
        

