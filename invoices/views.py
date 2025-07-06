from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.http import FileResponse, Http404
from django.core.mail import send_mail
from .models import Invoice
from .serializers import InvoiceSerializer
from .utils import generate_invoice_pdf_async, send_invoice_email_async


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        invoice = serializer.save(user=self.request.user)
        generate_invoice_pdf_async.delay(invoice.id)
        send_invoice_email_async.delay(invoice.id)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def download(self, request, pk=None):
        token = request.query_params.get('token')
        invoice = Invoice.objects.filter(pk=pk).first()
        if invoice and str(invoice.download_token) == token:
            return FileResponse(invoice.pdf_file.open('rb'), as_attachment=True, filename=f"invoice_{invoice.id}.pdf")
        raise Http404("Not found or invalid token")
