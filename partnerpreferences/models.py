from django.db import models
from authentication.models import DrinkingPreference, PhysicalStatus, SmokingPreference, User, MaritalStatus, AnnualIncome, Employment, Education

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class EatingHabit(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class BodyArt(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class CookingSkill(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    
class PartnerExpectation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="partner_expectation")
    age_preference = models.CharField(max_length=50,blank=True, default="Does not matter")
    height_preference = models.CharField(max_length=50,blank=True, default="Does not matter")
    marital_status = models.ManyToManyField(MaritalStatus, blank=True) 
    physical_status = models.ManyToManyField(PhysicalStatus, blank=True)
    drinking_preference = models.ManyToManyField(DrinkingPreference, blank=True)
    smoking_preference = models.ManyToManyField(SmokingPreference, blank=True)
    mother_tongue = models.CharField(max_length=100, null=True, blank=True)  
    education = models.ManyToManyField(Education, blank=True)
    profession = models.ManyToManyField(Employment, blank=True)
    annual_income = models.ManyToManyField(AnnualIncome, blank=True)
    partner_district = models.CharField(max_length=255, null=True, blank=True)
    partner_country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email}'s Partner Expectation"
    
    
class UserHobby(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hobbies')
    pets_details = models.TextField(blank=True, null=True)
    favourite_sports = models.TextField(blank=True, null=True)
    favourite_places = models.TextField(blank=True, null=True)
    favourite_books = models.TextField(blank=True, null=True)
    movies_and_music = models.TextField(blank=True, null=True)
    dress_sense = models.TextField(blank=True, null=True)
    body_art = models.ForeignKey(BodyArt, on_delete=models.SET_NULL, null=True, default=None)
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL, null=True, default=None)
    eating_habits = models.ForeignKey(EatingHabit, on_delete=models.SET_NULL, null=True, default=None)
    smoking_habits = models.ForeignKey(SmokingPreference, on_delete=models.SET_NULL, null=True, default=None)
    drinking_habits = models.ForeignKey(DrinkingPreference, on_delete=models.SET_NULL, null=True, default=None)
    cooking_skill = models.ForeignKey(CookingSkill, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return f"Hobbies of {self.user.email}"
    
