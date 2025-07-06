from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.conf import settings
from .models import Invoice
import os
from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def generate_invoice_pdf_async(invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    filename = f"invoice_{invoice.id}.pdf"
    filepath = os.path.join(settings.MEDIA_ROOT, 'invoices', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    c = canvas.Canvas(filepath, pagesize=A4)
    c.drawString(100, 800, f"Invoice for {invoice.client_name}")
    c.drawString(100, 780, f"Email: {invoice.client_email}")

    y = 740
    for item in invoice.items:
        c.drawString(100, y, f"{item['name']} - ${item['price']}")
        y -= 20

    c.drawString(100, y - 20, f"Total: ${invoice.total}")
    c.save()

    invoice.pdf_file.name = f"invoices/{filename}"
    invoice.save()


@shared_task
def send_invoice_email_async(invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    if not invoice.pdf_file:
        return
    subject = f"Invoice from {invoice.user.username}"
    message = f"Dear {invoice.client_name},\n\nPlease find attached your invoice."
    email = EmailMessage(subject, message, to=[invoice.client_email])
    email.attach_file(invoice.pdf_file.path)
    email.send()
