from django.db import models

class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    amount = models.FloatField()
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=50, default='Created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id
