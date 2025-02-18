from authentication.models import DrinkingPreference, SmokingPreference
from .models import BodyArt, CookingSkill, EatingHabit, Exercise, PartnerExpectation, UserHobby
from rest_framework import serializers

from rest_framework import serializers
from .models import UserHobby, BodyArt, Exercise, EatingHabit, SmokingPreference, DrinkingPreference, CookingSkill

class UserHobbySerializer(serializers.ModelSerializer):
    body_art = serializers.CharField()
    exercise = serializers.CharField()
    eating_habits = serializers.CharField()
    smoking_habits = serializers.CharField()
    drinking_habits = serializers.CharField()
    cooking_skill = serializers.CharField()

    class Meta:
        model = UserHobby
        fields = [
            'id',
            'pets_details',
            'favourite_sports',
            'favourite_places',
            'favourite_books',
            'movies_and_music',
            'dress_sense',
            'body_art',
            'exercise',
            'eating_habits',
            'smoking_habits',
            'drinking_habits',
            'cooking_skill'
        ]

    def update(self, instance, validated_data):
        # Handle body_art by name
        body_art_name = validated_data.pop('body_art', None)
        if body_art_name:
            body_art = BodyArt.objects.filter(name=body_art_name).first()
            
            if body_art:
                instance.body_art = body_art
            else:
                raise serializers.ValidationError({"body_art": f"Body art with name '{body_art_name}' not found."})

        # Handle exercise by name
        exercise_name = validated_data.pop('exercise', None)
        if exercise_name:
            exercise = Exercise.objects.filter(name=exercise_name).first()
            if exercise:
                instance.exercise = exercise
            else:
                raise serializers.ValidationError({"exercise": f"Exercise with name '{exercise_name}' not found."})

        # Handle eating_habits by name
        eating_habit_name = validated_data.pop('eating_habits', None)
        if eating_habit_name:
            eating_habit = EatingHabit.objects.filter(name=eating_habit_name).first()
            if eating_habit:
                instance.eating_habits = eating_habit
            else:
                raise serializers.ValidationError({"eating_habits": f"Eating habit with name '{eating_habit_name}' not found."})

        # Handle smoking_habits by name
        smoking_habit_name = validated_data.pop('smoking_habits', None)
        if smoking_habit_name:
            smoking_habit = SmokingPreference.objects.filter(status=smoking_habit_name).first()
            if smoking_habit:
                instance.smoking_habits = smoking_habit
            else:
                raise serializers.ValidationError({"smoking_habits": f"Smoking habit with name '{smoking_habit_name}' not found."})

        # Handle drinking_habits by name
        drinking_habit_name = validated_data.pop('drinking_habits', None)
        if drinking_habit_name:
            drinking_habit = DrinkingPreference.objects.filter(status=drinking_habit_name).first()
            if drinking_habit:
                instance.drinking_habits = drinking_habit
            else:
                raise serializers.ValidationError({"drinking_habits": f"Drinking habit with name '{drinking_habit_name}' not found."})

        # Handle cooking_skill by name
        cooking_skill_name = validated_data.pop('cooking_skill', None)
        if cooking_skill_name:
            cooking_skill = CookingSkill.objects.filter(name=cooking_skill_name).first()
            if cooking_skill:
                instance.cooking_skill = cooking_skill
            else:
                raise serializers.ValidationError({"cooking_skill": f"Cooking skill with name '{cooking_skill_name}' not found."})

        # Update other fields (those not related to ForeignKey)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

                
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
    marital_status = serializers.StringRelatedField(many=True)
    physical_status = serializers.StringRelatedField(many=True)
    drinking_preference = serializers.StringRelatedField(many=True)
    smoking_preference = serializers.StringRelatedField(many=True)
    education = serializers.StringRelatedField(many=True)
    profession = serializers.StringRelatedField(many=True)
    annual_income = serializers.StringRelatedField(many=True)

    class Meta:
        model = PartnerExpectation
        fields = "__all__"