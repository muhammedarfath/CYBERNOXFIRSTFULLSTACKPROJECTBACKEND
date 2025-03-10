from django.core.mail import send_mail
from django.conf import settings
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

def send_interest_email(user_email, userEmail):
    subject = "You Have a New Interest!"
    message = f"Hi there! {userEmail} has shown interest in your profile. Log in to your account to check it out."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
    
    
@sync_to_async
def send_message_email(sender_id, recipient_id, message_text):
    User = get_user_model()

    try:
        sender = User.objects.get(id=sender_id)
        recipient = User.objects.get(id=recipient_id)

        subject = "You Have a New Message!"
        message = f"Hi {recipient.email},\n\n{sender.email} has sent you a new message:\n\n{message_text}\n\nLog in to your account to reply."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [recipient.email]

        send_mail(subject, message, from_email, recipient_list)
    except User.DoesNotExist:
        print("User not found. Email not sent.")