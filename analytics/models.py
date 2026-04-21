from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class ClientInsight(models.Model):
    # This links the data securely to whoever is logged in
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The cleaned data fields (The Gold Layer)
    upload_date = models.DateTimeField(auto_now_add=True)
    total_revenue = models.FloatField()
    top_performing_product = models.CharField(max_length=100)
    total_rows_processed = models.IntegerField()

    def __str__(self):
        return f"{self.client.username} - Insight {self.id}"