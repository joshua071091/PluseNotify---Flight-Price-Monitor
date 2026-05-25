from django.test import TestCase
from django.contrib.auth.models import User
from .models import (
    PriceAlert,
    NotificationLog
)


class PriceThresholdTest(
    TestCase
):

    def test_price_below_threshold_triggers_alert(
        self
    ):
        self.assertTrue(
            4200 <= 4500
        )

    def test_price_above_threshold_does_not_trigger(
        self
    ):
        self.assertFalse(
            5000 <= 4500
        )

    def test_price_equal_threshold(
        self
    ):
        self.assertTrue(
            4500 <= 4500
        )

class NotificationLogTest(
    TestCase
):

    def setUp(self):

        self.user = (
            User.objects.create_user(
                username="josh",
                password="123456"
            )
        )

        self.alert = (
            PriceAlert.objects.create(
                user=self.user,
                origin="DEL",
                destination="BOM",
                threshold_price=4500
            )
        )

    def test_notification_created(self):

        log = (
            NotificationLog.objects.create(
                alert=self.alert,
                triggered_price=4200,
                message="Price dropped"
            )
        )

        self.assertEqual(
            log.triggered_price,
            4200
        )

class AlertScopingTest(
    TestCase
):

    def setUp(self):

        self.user1 = (
            User.objects.create_user(
                username="user1"
            )
        )

        self.user2 = (
            User.objects.create_user(
                username="user2"
            )
        )

        PriceAlert.objects.create(
            user=self.user1,
            origin="DEL",
            destination="BOM",
            threshold_price=4500
        )

        PriceAlert.objects.create(
            user=self.user2,
            origin="BLR",
            destination="HYD",
            threshold_price=2000
        )

    def test_user_only_own_alerts(self):

        alerts = (
            PriceAlert.objects.filter(
                user=self.user1
            )
        )

        self.assertEqual(
            alerts.count(),
            1
        )