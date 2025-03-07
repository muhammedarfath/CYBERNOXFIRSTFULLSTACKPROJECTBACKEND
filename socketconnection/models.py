from django.db import models

from authentication.models import User
from django.utils.timezone import now

# Create your models here.


class Message(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name='receiver_message')
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'send_message')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
            return f"{self.sender} - {self.receiver}"
        


 
 
class SubscriptionPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription")
    plan_name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan_name}"

    def is_subscription_active(self):
        return self.is_active and self.end_date >= now()    
    