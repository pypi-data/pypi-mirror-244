from __future__ import annotations

import json

from pretix_fattura_elettronica.acubeapi import send_invoice_via_api

from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from pretix.base.models import Invoice, Order
from pretix.control.permissions import organizer_permission_required
from rest_framework import status, viewsets
from rest_framework.decorators import action  # type: ignore
from rest_framework.response import Response

from .forms import ElectronicInvoiceForm


class ElectronicInvoiceViewSet(viewsets.ViewSet):
    permission = "can_edit_orders"

    lookup_field = "order_code"

    @action(methods=["POST"], detail=True)
    def update_invoice_information(
        self, request: HttpRequest, order_code: str
    ) -> Response:
        order = get_object_or_404(Order, code=order_code)

        body = request.body.decode("utf-8")
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # we use a form here instead of a serializer because we are reusing
        # the forms fields in the pretix contact form
        form = ElectronicInvoiceForm(data=body)

        if form.is_valid():
            meta_info = order.meta_info_data or {}  # type: ignore

            meta_info["pec"] = form.cleaned_data["pec"]
            meta_info["sdi"] = form.cleaned_data["sdi"]
            meta_info["codice_fiscale"] = form.cleaned_data["codice_fiscale"]

            order.meta_info = json.dumps(meta_info)  # type: ignore
            order.save(update_fields=["meta_info"])  # type: ignore

            return Response(
                {"code": order_code},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"errors": dict(form.errors), "other_errors": form.non_field_errors()},
                status=status.HTTP_400_BAD_REQUEST,
            )


@require_http_methods(["POST"])
@organizer_permission_required("can_change_settings")
def send_fattura_elettronica(request, organizer, event, code):
    invoice_id = request.POST.get("invoice_id")

    redirect = HttpResponseRedirect(
        redirect_to=reverse(
            "control:event.order",
            kwargs={"organizer": organizer, "event": event, "code": code},
        )
    )

    if not invoice_id:
        messages.error(request, "Missing invoice_id")

        return redirect

    invoice = Invoice.objects.filter(
        order__code=code, event__slug=event, id=invoice_id
    ).first()

    if not invoice:
        messages.error(request, "Missing invoice")

        return redirect

    try:
        send_invoice_via_api(invoice)
        messages.success(
            request,
            "Fattura elettronica inviata con successo",
        )
    except ValueError as e:
        messages.error(request, str(e))

    return redirect
