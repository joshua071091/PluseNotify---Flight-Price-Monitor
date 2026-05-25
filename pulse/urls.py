from pulse.views import NotificationLogListView
from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    CreateAlertView,
    AlertListView,
    DeleteAlertView,
    FlightPriceView,
    AdminSummaryView,
)

urlpatterns = [

    path(
        "auth/register/",
        RegisterView.as_view()
    ),

    path(
        "auth/login/",
        LoginView.as_view()
    ),

    path(
        "alerts/",
        CreateAlertView.as_view()
    ),

    path(
        "alerts/list/",
        AlertListView.as_view()
    ),

    path(
        "alerts/<int:pk>/",
        DeleteAlertView.as_view()
    ),

    path(
        "flights/price/",
        FlightPriceView.as_view()
    ),

    path(
        "admin/summary/",
        AdminSummaryView.as_view()
    ),

    path(
        "notifications/",
        NotificationLogListView.as_view()
    ),
]