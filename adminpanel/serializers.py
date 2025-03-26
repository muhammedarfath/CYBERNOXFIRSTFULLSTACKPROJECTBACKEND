from authentication.serializers import UserSerializer
from rest_framework import serializers
from authentication.models import IdentityProof, UserVerification

class IdentityProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentityProof
        fields = ['image'] 

class UserVerificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    identity_proofs = IdentityProofSerializer(many=True, read_only=True) 
    
    class Meta:
        model = UserVerification
        fields = ['user', 'proof_verified', 'identity_proofs']