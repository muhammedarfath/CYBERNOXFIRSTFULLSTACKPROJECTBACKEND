from partnerpreferences.serializers import PartnerExpectationSerializer, UserHobbySerializer
from rest_framework import serializers
from .models import Blood, CurrentLiving, DrinkingPreference, Hair, HairType, HomeType, PhysicalStatus, Political, Polygamy, Post, ReligiousServices, Religiousness, Skin, SmokingPreference, User,BodyType
from django.contrib.auth.hashers import make_password
from .models import Profile, User, MaritalStatus, Religion, Caste,GroomBrideInfo, Education, Employment, AnnualIncome,FamilyInformation, FamilyType, FamilyStatus, Occupation,Gender,CreateFor

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'name']

class CreateForSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateFor
        fields = ['id', 'name']
        
class UserSerializer(serializers.ModelSerializer):
    gender = serializers.PrimaryKeyRelatedField(queryset=Gender.objects.all(), required=False) 
    unique_id = serializers.ReadOnlyField() 
    
    class Meta:
        model = User
        fields = '__all__' 
        extra_kwargs = {
            'password': {'write_only': True}, 
        }

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    marital_status = serializers.PrimaryKeyRelatedField(queryset=MaritalStatus.objects.all())
    religion = serializers.PrimaryKeyRelatedField(queryset=Religion.objects.all())
    caste = serializers.PrimaryKeyRelatedField(queryset=Caste.objects.all())

    class Meta:
        model = Profile
        fields = ['id', 'user', 'name', 'date_of_birth', 'marital_status', 'religion', 'caste', 'mother_tongue','languages_spoken', 'height', 'weight', 'body_type', 'physical_challenges', 'physical_status']    
        
        
class GroomBrideInfoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    education = serializers.PrimaryKeyRelatedField(queryset=Education.objects.all())
    employment = serializers.PrimaryKeyRelatedField(queryset=Employment.objects.all())
    income = serializers.PrimaryKeyRelatedField(queryset=AnnualIncome.objects.all())
    occupation = serializers.PrimaryKeyRelatedField(queryset=Occupation.objects.all())

    class Meta:
        model = GroomBrideInfo
        fields = ['id','user','addres','secondary_mobileno', 'country', 'state', 'city','present_country','present_state','present_city', 'family_live', 'occupation', 'other_occupation', 'education', 'employment', 'income', 'college_name']        
        
        
class FamilyInformationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    family_type = serializers.PrimaryKeyRelatedField(queryset=FamilyType.objects.all())
    family_status = serializers.PrimaryKeyRelatedField(queryset=FamilyStatus.objects.all())
    father_occupation = serializers.PrimaryKeyRelatedField(queryset=Occupation.objects.all())
    mother_occupation = serializers.PrimaryKeyRelatedField(queryset=Occupation.objects.all())

    class Meta:
        model = FamilyInformation
        fields = [
            'id',
            'user',
            'family_type',
            'family_status',
            'father_name',
            'father_occupation',
            'mother_occupation',
            'number_of_brothers',
            'number_of_sisters',
            'married_brothers',
            'married_sisters',
            'family_description',
        ]        
        
        
class CasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caste
        fields = ['id', 'name']

class ReligionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Religion
        fields = ['id', 'name']  
        
class MaritalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaritalStatus
        fields = ['id', 'status']   


        
class BodySerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyType
        fields = ['id', 'name']
        
        
class EmployementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employment
        fields = ['id', 'employed_in']
        
        
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'highest_education']                
        
        
        
class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = ['id', 'name']    
        
class AnnualIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnualIncome
        fields = ['id', 'annual_income']    
        
                
class FamilyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyType
        fields = ['id', 'name']    
        
class FamilyStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyStatus
        fields = ['id', 'name']  
         
class FetchProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    marital_status = serializers.StringRelatedField()  
    religion = serializers.StringRelatedField()
    caste = serializers.StringRelatedField()
    mother_tongue = serializers.StringRelatedField()
    body_type = serializers.StringRelatedField()
    religiousness = serializers.StringRelatedField()
    religious_services = serializers.StringRelatedField()
    polygamy = serializers.StringRelatedField()
    political_View = serializers.StringRelatedField()
    skin_color = serializers.StringRelatedField()
    blood_group = serializers.StringRelatedField()
    hair_color = serializers.StringRelatedField()
    hair_type = serializers.StringRelatedField()
    appearance = serializers.StringRelatedField()
    
    class Meta:
        model = Profile
        fields = ['user','name', 'date_of_birth','languages_spoken','hair_color','hair_type','appearance', 'marital_status', 'religion', 'caste', 'mother_tongue', 'height', 
                  'weight', 'body_type', 'skin_color','blood_group','physical_challenges','religiousness','religious_services','polygamy','political_View','physical_status']          
                        
class FetchFamilyInformationSerializer(serializers.ModelSerializer):
    family_type = serializers.StringRelatedField()  
    family_status = serializers.StringRelatedField()  
    father_occupation = serializers.StringRelatedField()  
    mother_occupation = serializers.StringRelatedField()  
    home_type = serializers.StringRelatedField() 
    current_living = serializers.StringRelatedField() 
    
    class Meta:
        model = FamilyInformation
        fields = [
            'id',
            'family_type',
            'family_status',
            'father_name',
            'father_occupation',
            'mother_occupation',
            'number_of_brothers',
            'number_of_sisters',
            'married_brothers',
            'married_sisters',
            'family_description',
            'mother_name',
            'home_type',
            'current_living'
        ]          
                                     
class FetchGroomBrideInfoSerializer(serializers.ModelSerializer):
    education = serializers.StringRelatedField() 
    employment = serializers.StringRelatedField() 
    income = serializers.StringRelatedField() 
    occupation = serializers.StringRelatedField() 

    class Meta:
        model = GroomBrideInfo
        fields = ['id','country','present_country',
                  'present_state','present_city','time_to_call',
                  'secondary_mobileno', 'state', 'city', 'family_live',
                  'occupation', 'other_occupation','company_name','experience', 'education','addres','employment',
                  'income', 'college_name'] 
               
class FullProfileSerializer(serializers.Serializer):
    user_profile = FetchProfileSerializer()
    groom_bride_info = FetchGroomBrideInfoSerializer()  
    family_info = FetchFamilyInformationSerializer()
    user_hobby = UserHobbySerializer()
    partner_preferences = PartnerExpectationSerializer()

    class Meta:
        fields = ['user_profile', 'groom_bride_info', 'family_info','partner_preferences']   
        
class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'created_at', 'updated_at', 'image']
        read_only_fields = ['id', 'created_at', 'updated_at']
        
        
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_picture'] 
        
        
class PhysicalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalStatus
        fields = ['id', 'status'] 
        

class DrinkingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrinkingPreference
        fields = ['id', 'status']   

class SmokingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmokingPreference
        fields = ['id', 'status']       
        
        
class MaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaritalStatus
        fields = ['id', 'status']
        
class ReligiousnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Religiousness
        fields = ["id", "name"]                                
                      
class ReligiousnesServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReligiousServices
        fields = ["id", "name"]     

        
class PolygamySerializer(serializers.ModelSerializer):
    class Meta:
        model = Polygamy
        fields = ["id", "name"]     
                                            
                                            
class PoliticalViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Political
        fields = ["id", "name"]  
        
        
class SkinColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skin
        fields = ["id", "name"]  
        
        
        
class BloodGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blood
        fields = ["id", "name"]      
        
        
class HairColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hair
        fields = ["id", "name"] 
        
                                                                             
                
class HairTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairType
        fields = ["id", "name"]         
        
        
class HomeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeType
        fields = ["id", "name"]  

class LivingSituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentLiving
        fields = ['id', 'name']      
        
        

