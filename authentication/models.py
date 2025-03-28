from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string
from django.utils.timezone import now
from django.utils import timezone

# Create your models here.
  
class Religion(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name  
    
class Religiousness(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name     
    
class ReligiousServices(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name 
    
    
class Polygamy(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name     
    
class Political(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name 
    
    
    
class Skin(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name      
    
class Blood(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name     
    
class Hair(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name           
    
    
class HairType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name            
        
           
    
class Caste(models.Model):
    name = models.CharField(max_length=100)
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE, related_name="castes")

    def __str__(self):
        return f"{self.name} ({self.religion.name})"    
    
    
class Gender(models.Model):
    name = models.CharField(max_length=10) 

    def __str__(self):
        return self.name
    
class CreateFor(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Created For")

    def __str__(self):
        return self.name

    
class MaritalStatus(models.Model):
    status = models.CharField(max_length=10) 

    def __str__(self):
        return self.status
    
    
    
class Education(models.Model):
    highest_education = models.CharField(max_length=100)

    def __str__(self):
        return self.highest_education

class Employment(models.Model):
    employed_in = models.CharField(max_length=100)

    def __str__(self):
        return self.employed_in

class AnnualIncome(models.Model):
    annual_income = models.CharField(max_length=100)

    def __str__(self):
        return self.annual_income   
    
    
class FamilyType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class FamilyStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class HomeType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name    


class CurrentLiving(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name    


class Occupation(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name  
    
        
    
class BodyType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name   
    
    
class PhysicalStatus(models.Model):
    status = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.status

class DrinkingPreference(models.Model):
    status = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.status

class SmokingPreference(models.Model):
    status = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.status

class EthnicGroup(models.Model):
    status = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.status    
          
           
class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ]

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='',
        verbose_name="User Type"
    )
    username = models.CharField(max_length=150, blank=True, null=True,unique=True) 
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email")
    mobileno = models.CharField(max_length=15, unique=True, verbose_name="Mobile Number",null=True,)
    createfor = models.ForeignKey(CreateFor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Created For")
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)
    password = models.CharField(max_length=128, verbose_name="Password")
    termsandcondition = models.BooleanField(default=False, verbose_name="Terms and Conditions Accepted")
    unique_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name="Profile Picture",default='profile_pictures/default.jpg')
    is_online = models.BooleanField(default=False)
    blocked_users = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='blocked_by')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    
    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_id():
        prefix = "WT"
        while True:
            random_digits = ''.join(random.choices(string.digits, k=7))
            unique_id = f"{prefix}{random_digits}"
            if not User.objects.filter(unique_id=unique_id).exists():
                return unique_id

    def __str__(self):
        return self.email
    
    def block_user(self, user_to_block):
        """
        Block a user.
        :param user_to_block: The user to block (User instance).
        """
        if user_to_block not in self.blocked_users.all():
            self.blocked_users.add(user_to_block)
            self.save()

    def unblock_user(self, user_to_unblock):
        """
        Unblock a user.
        :param user_to_unblock: The user to unblock (User instance).
        """
        if user_to_unblock in self.blocked_users.all():
            self.blocked_users.remove(user_to_unblock)
            self.save()

    def is_user_blocked(self, user_to_check):
        """
        Check if a user is blocked by the current user.
        :param user_to_check: The user to check (User instance).
        :return: True if the user is blocked, False otherwise.
        """
        return self.blocked_users.filter(id=user_to_check.id).exists()    
    
class InterestSent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interest", blank=True, null=True)
    interest = models.ManyToManyField(User, related_name="liked_posts", blank=True)  
    timestamp = models.DateTimeField(default=now) 
    def like_count(self):
        return self.interest.count()


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('message', 'Message Notification'),
        ('interest', 'Interest Notification'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='message')

    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="posts/", blank=True, null=True, verbose_name="Post Image")


    def __str__(self):
        return self.content
    
    


    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.SET_NULL, null=True, blank=True)    
    religion = models.ForeignKey(Religion, on_delete=models.SET_NULL, null=True, blank=True)
    religiousness = models.ForeignKey(Religiousness, on_delete=models.SET_NULL, null=True, blank=True)
    religious_services = models.ForeignKey(ReligiousServices, on_delete=models.SET_NULL, null=True, blank=True)
    polygamy = models.ForeignKey(Polygamy, on_delete=models.SET_NULL, null=True, blank=True)
    political_View = models.ForeignKey(Political, on_delete=models.SET_NULL, null=True, blank=True)
    skin_color = models.ForeignKey(Skin, on_delete=models.SET_NULL, null=True, blank=True)
    blood_group = models.ForeignKey(Blood, on_delete=models.SET_NULL, null=True, blank=True)
    hair_color = models.ForeignKey(Hair, on_delete=models.SET_NULL, null=True, blank=True)
    hair_type = models.ForeignKey(HairType, on_delete=models.SET_NULL, null=True, blank=True)
    appearance = models.TextField(blank=True, null=True)
    caste = models.ForeignKey(Caste, on_delete=models.SET_NULL, null=True, blank=True)
    mother_tongue = models.CharField(max_length=100, null=True, blank=True)  
    height = models.FloatField()
    weight = models.FloatField()
    body_type = models.ForeignKey(BodyType, on_delete=models.SET_NULL, null=True, blank=True)
    physical_challenges = models.BooleanField(default=False)
    languages_spoken = models.CharField(max_length=500, null=True, blank=True)
    physical_status = models.ForeignKey(PhysicalStatus, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.name
    
    
class GroomBrideInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    country = models.CharField(max_length=100)
    present_country = models.CharField(max_length=100,blank=True, null=True)
    state = models.CharField(max_length=100)
    present_state = models.CharField(blank=True, null=True, max_length=100)
    city = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100,blank=True, null=True)
    experience = models.CharField(max_length=100,blank=True, null=True)
    secondary_mobileno = models.CharField(max_length=15, blank=True, null=True, unique=True, verbose_name="Secondary Mobile Number")
    time_to_call = models.CharField(max_length=100,blank=True, null=True)
    present_city = models.CharField(max_length=100,blank=True, null=True)
    family_live = models.BooleanField(default=False) 
    occupation = models.ForeignKey(
        Occupation, on_delete=models.SET_NULL, null=True
    )
    addres = models.TextField(blank=True, null=True)
    other_occupation = models.CharField(max_length=100, blank=True, null=True)
    education = models.ForeignKey(Education, on_delete=models.SET_NULL, null=True, blank=True)
    employment = models.ForeignKey(Employment, on_delete=models.SET_NULL, null=True, blank=True)
    income = models.ForeignKey(AnnualIncome, on_delete=models.SET_NULL, null=True, blank=True)
    college_name = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"{self.user.email}'s Family"
    
    
class FamilyInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True) 
    family_type = models.ForeignKey(FamilyType, on_delete=models.SET_NULL, null=True,blank=True)
    family_status = models.ForeignKey(FamilyStatus, on_delete=models.SET_NULL, null=True,blank=True)
    home_type = models.ForeignKey(HomeType, on_delete=models.SET_NULL, null=True,blank=True)
    current_living = models.ForeignKey(CurrentLiving, on_delete=models.SET_NULL, null=True,blank=True)
    
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    father_occupation = models.ForeignKey(
        Occupation, on_delete=models.SET_NULL, null=True, related_name="father_occupations"
    )
    mother_occupation = models.ForeignKey(
        Occupation, on_delete=models.SET_NULL, null=True, related_name="mother_occupations"
    )
    number_of_brothers = models.PositiveIntegerField(default=0)
    number_of_sisters = models.PositiveIntegerField(default=0)
    married_brothers = models.PositiveIntegerField(default=0)
    married_sisters = models.PositiveIntegerField(default=0)
    family_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.father_name}'s Family"
        

class UserVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aadhar_number = models.CharField(max_length=12, blank=True, null=True)
    otp_sent = models.BooleanField(default=False)
    otp_verified = models.BooleanField(default=False)
    proof_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification for {self.user.email}"

class IdentityProof(models.Model):
    user_verification = models.ForeignKey(UserVerification, on_delete=models.CASCADE, related_name='identity_proofs')
    image = models.ImageField(upload_to='identity_proofs/')

    def __str__(self):
        return f"Identity Proof for {self.user_verification.user.email}"
 
 
class SavedProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_profiles")
    saved_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_by_users")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'saved_user')  

    def __str__(self):
        return f"{self.user.email} saved {self.saved_user.email}"    
  
    
    
    
