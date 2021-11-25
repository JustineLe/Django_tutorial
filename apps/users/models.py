from django.contrib.auth.models import AbstractUser
from django.db import models

from commons.models import BaseModel


class ClientModel(BaseModel):
    client_id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=255, null=False)
    seconds_delivered_per_month = models.IntegerField(null=False)
    is_archived = models.BooleanField()

    class Meta:
        db_table = 'clients'


class UserAccountModel(AbstractUser):
    client = models.ForeignKey(ClientModel, on_delete=models.CASCADE, null=True, related_name='users')
    user_type = models.IntegerField(null=True)
    remember_token = models.CharField(max_length=255, null=True)
    last_name_kanji = models.CharField(max_length=255, null=True)
    first_name_kanji = models.CharField(max_length=255, null=True)
    last_name_kana = models.CharField(max_length=255, null=True)
    first_name_kana = models.CharField(max_length=255, null=True)
    nickname = models.CharField(max_length=255, null=True)
    sex = models.CharField(max_length=255, null=True)
    is_sex_public = models.CharField(max_length=255, null=True)
    date_of_birth = models.DateField(null=True)
    is_date_of_birth_public = models.BooleanField(max_length=255, null=True)
    phone = models.CharField(max_length=45, null=True)
    created_at = models.DateTimeField(null=True, blank=True, verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True, verbose_name='更新日時')
    is_deleted = models.BooleanField(null=True, default=False, verbose_name='削除フラグ')

    class Meta:
        db_table = 'users'
