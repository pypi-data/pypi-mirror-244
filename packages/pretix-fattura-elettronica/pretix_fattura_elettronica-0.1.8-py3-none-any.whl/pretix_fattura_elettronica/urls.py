# django urls
from __future__ import annotations

from django.urls import re_path

from pretix.api.urls import router

from . import views
from .views import ElectronicInvoiceViewSet

router.register("orders", ElectronicInvoiceViewSet, basename="orders")


urlpatterns = [
    re_path(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/orders/(?P<code>[0-9A-Z]+)/send_fattura/$",
        views.send_fattura_elettronica,
        name="send_fattura",
    ),
]
