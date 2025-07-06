from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    items = models.JSONField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='invoices/', null=True, blank=True)
    download_token = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"Invoice {self.id} to {self.client_name}"
