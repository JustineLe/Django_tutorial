from django.conf import settings
from django.conf.urls import url
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from apps.users.views import UserListCreateAPIView, UserDetailUpdateAPIView, ClientListCreateAPIView, MyView

urlpatterns = [
    url(r'^/login', obtain_jwt_token),
    url(r'^/refresh-token', refresh_jwt_token),
    url(r'^/users$', MyView.as_view(), name='user_list'),
    path('/user/<int:pk>', UserDetailUpdateAPIView.as_view(), name='user_detail_update'),
    url(r'^/clients$', ClientListCreateAPIView.as_view(), name='client_list'),
]
