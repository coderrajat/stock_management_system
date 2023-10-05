from rest_framework import serializers

from . import models


class new_order_serializer(serializers.ModelSerializer):
    class Meta():
        model=models.Order_placed
        fields=('__all__')