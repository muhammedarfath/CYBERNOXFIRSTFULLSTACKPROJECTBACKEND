from .models import BodyArt, CookingSkill, EatingHabit, Exercise, PartnerExpectation, UserHobby
from rest_framework import serializers

class UserHobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHobby
        fields = "__all__"
        
class BodyArtStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyArt
        fields = ['id', 'name']    
        
class CookingSkillStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingSkill
        fields = ['id', 'name']        
        
        
class EatingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EatingHabit
        fields = ['id', 'name']                        


class ExerciseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name']    
        
class PartnerExpectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerExpectation
        fields = "__all__"