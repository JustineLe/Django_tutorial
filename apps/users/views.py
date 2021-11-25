from django.db.models import Prefetch
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from apps.users.models import UserAccountModel, ClientModel
from apps.users.serializers.user_serializers import UserSerializer, ClientSerializer
from commons.pagination import PaginationAPIView
from commons.permission import CustomPermission


class UserListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [CustomPermission]
    # def get(self, request, format=None):
    #     keyword = ''
    #     param = request.GET
    #     if 'keyword' in param:
    #         keyword = param['keyword']
    #     print('param', param)
    #     users = UserAccountModel.objects.filter(client_id__name__icontains=keyword)
    #     serializer = UserSerializer(users, many=True)
    #     return Response(serializer.data)
    #
    # def post(self, request, format=None):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    queryset = UserAccountModel.objects.select_related('client').filter(is_deleted=False)
    serializer_class = UserSerializer


class UserDetailUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserAccountModel.objects.filter(is_deleted=False)
    serializer_class = UserSerializer


class ClientListCreateAPIView(APIView):
    # queryset = ClientModel.objects.prefetch_related(Prefetch('users',
    #                                                          queryset=UserAccountModel.objects.filter(
    #                                                              email='vdong@gmail.com'))).filter(
    #     is_deleted=False)
    # serializer_class = ClientSerializer

    def post(self, request, format=None):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyView(PaginationAPIView):
    queryset = UserAccountModel.objects.select_related('client').filter(is_deleted=False)
    serializer_class = UserSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS  # cool trick right? :)

    # We need to override get method to achieve pagination
    def get(self, request):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Now add the pagination handlers taken from
        #  django-rest-framework/rest_framework/generics.py
