from django.db import models

from authentication.models import User

# Create your models here.


class Message(models.Model):
    author = models.ForeignKey(User,related_name='author_messages',on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender_name")
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.author.email
    
    