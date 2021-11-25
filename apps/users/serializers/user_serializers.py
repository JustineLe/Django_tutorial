from rest_framework import serializers

from apps.users.models import UserAccountModel, ClientModel


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccountModel
        fields = ['email', 'last_name_kanji', 'first_name_kanji']


class ClientSerializer(serializers.ModelSerializer):
    users = UserListSerializer(many=True, read_only=True)

    class Meta:
        model = ClientModel
        fields = ['client_id', 'name', 'users', 'seconds_delivered_per_month', 'is_archived']

        extra_kwargs = {
            'client_id': {'required': False}
        }

    def save(self, **kwargs):
        client = ClientModel()
        client.client_id = self.initial_data['client_id']
        client.name = self.initial_data['name']
        client.seconds_delivered_per_month = 0
        client.is_archived = self.initial_data['is_archived']
        client.save()
        return client


class UserSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False)

    class Meta:
        model = UserAccountModel
        fields = ['email', 'last_name_kanji', 'first_name_kanji', 'client']

    # def save(self, **kwargs):
