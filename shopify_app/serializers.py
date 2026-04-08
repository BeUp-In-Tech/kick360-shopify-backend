from rest_framework import serializers
from .models import AccessCode


class AccessCodeSerializer(serializers.ModelSerializer):

    class Meta:

        model = AccessCode

        fields = "__all__"