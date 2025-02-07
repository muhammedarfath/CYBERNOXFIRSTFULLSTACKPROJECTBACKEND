from django.db import models

from authentication.models import User

# Create your models here.


class Message(models.Model):
    author = models.ForeignKey(User,related_name='author_messages',on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.author.email
    
    
    def last_10_messages():
        return Message.objects.order_by('timestamp').all()[:100]    