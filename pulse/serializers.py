from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (
    UserProfile,
    PriceAlert,
    NotificationLog
)

class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(
        write_only=True,
        min_length=6
    )
    email = serializers.EmailField()
    is_admin = serializers.BooleanField(
        write_only=True,
        default=False
    )

    def validate_username(self, value):

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists."
            )

        return value

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True
    )

class RegisterResponseSerializer(serializers.Serializer):

    username = serializers.CharField()
    access = serializers.CharField()
    role = serializers.CharField()

class PriceAlertCreateSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = PriceAlert

        fields = (
            'id',
            'origin',
            'destination',
            'threshold_price'
        )

        read_only_fields = ('id',)

class PriceAlertListSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = PriceAlert

        fields = (
            'id',
            'origin',
            'destination',
            'threshold_price',
            'status',
            'created_at'
        )

class NotificationLogSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = NotificationLog

        fields = '__all__'

class FlightPriceSerializer(
    serializers.Serializer
):

    route = serializers.CharField()
    price = serializers.IntegerField()

class AdminSummarySerializer(
    serializers.Serializer
):

    total_alerts = serializers.IntegerField()

    active_alerts = serializers.IntegerField()

    triggered_alerts = serializers.IntegerField()

    total_notifications = serializers.IntegerField()

    top_routes = serializers.ListField()