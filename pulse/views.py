import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.db.models import Count


from .models import PriceAlert
from .models import NotificationLog
from .models import UserProfile
from .permissions import IsAdminUser

from .serializers import RegisterSerializer
from .serializers import LoginSerializer
from .serializers import PriceAlertCreateSerializer
from .serializers import PriceAlertListSerializer
from .serializers import NotificationLogSerializer




class RegisterView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
            email=serializer.validated_data["email"]
        )

        if serializer.validated_data.get("is_admin"):
            user.profile.role = UserProfile.Role.ADMIN
            user.profile.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "username": user.username,
                "access": str(refresh.access_token),
                "role": user.profile.role
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"]
        )

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )

class CreateAlertView(generics.CreateAPIView):

    serializer_class = PriceAlertCreateSerializer

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )

class AlertListView(generics.ListAPIView):

    serializer_class = PriceAlertListSerializer

    def get_queryset(self):

        return PriceAlert.objects.filter(
            user=self.request.user
        )

class DeleteAlertView(APIView):

    def delete(self, request, pk):

        alert = get_object_or_404(
            PriceAlert,
            id=pk
        )

        if alert.user != request.user:

            return Response(
                {"error": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        alert.status = PriceAlert.Status.INACTIVE

        alert.save()

        return Response(
            {"status": "inactive"},
            status=status.HTTP_200_OK
        )

class FlightPriceView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        route = request.query_params.get("route")
        if not route:
            return Response(
                {"error": "route parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "route": route,
                "price": random.randint(1000, 10000)
            },
            status=status.HTTP_200_OK
        )

class AdminSummaryView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        total_alerts = PriceAlert.objects.count()

        active_alerts = PriceAlert.objects.filter(
            status=PriceAlert.Status.ACTIVE
        ).count()

        triggered_alerts = PriceAlert.objects.filter(
            status=PriceAlert.Status.TRIGGERED
        ).count()

        total_notifications = NotificationLog.objects.count()

        routes = (
            PriceAlert.objects
            .values("origin", "destination")
            .annotate(alert_count=Count("id"))
            .order_by("-alert_count")
        )

        top_routes = [
            {
                "route": f"{r['origin']}-{r['destination']}",
                "alert_count": r["alert_count"]
            }
            for r in routes
        ]

        return Response(
            {
                "total_alerts": total_alerts,
                "active_alerts": active_alerts,
                "triggered_alerts": triggered_alerts,
                "total_notifications": total_notifications,
                "top_routes": top_routes
            }
        )

class NotificationLogListView(
    generics.ListAPIView
):

    serializer_class = NotificationLogSerializer

    def get_queryset(self):

        return NotificationLog.objects.all()