from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(null=True, blank=True, verbose_name='登録日時', auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True, verbose_name='更新日時')
    is_deleted = models.BooleanField(null=True, default=False, verbose_name='削除フラグ')

    class Meta:
        abstract = True
