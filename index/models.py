from django.db import models
from datetime import datetime
import zipcodetw

class data(models.Model):
    def __str__(self):
        return f"{self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    id = models.AutoField(primary_key=True)
    receiverName = models.CharField(max_length=30)
    senderName = models.CharField(max_length=30)
    receiverAddress = models.CharField(max_length=50)
    receiverAddressID = models.CharField(max_length=5, default='None')
    senderAddress = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    kind = models.IntegerField()
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)