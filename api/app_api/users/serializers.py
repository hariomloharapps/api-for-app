# serializers.py
# from rest_framework import serializers
# # from .models import UserVerification

# class Base64ImageField(serializers.Field):
#     def to_internal_value(self, data):
#         if isinstance(data, str) and data.startswith('data:image'):
#             # Remove the data:image/[format];base64, prefix
#             format, base64_str = data.split(';base64,')
#             return base64.b64decode(base64_str)
#         raise serializers.ValidationError("Invalid image format")

# class UserVerificationSerializer(serializers.ModelSerializer):
#     profile_picture = serializers.ImageField(required=False)
#     base64_image = Base64ImageField(required=False, write_only=True)

#     class Meta:
#         model = UserVerification
#         fields = ['profile_picture', 'base64_image', 'is_verified']
#         read_only_fields = ['is_verified']




from rest_framework import serializers
from .models import User, UserRelationship

class UserRelationshipNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRelationship
        fields = [
            'relationship_type', 'personality_type', 
            'custom_name', 'ai_name', 'bio', 'is_active'
        ]

class UserNestedSerializer(serializers.ModelSerializer):
    relationship = UserRelationshipNestedSerializer()

    class Meta:
        model = User
        fields = [
            'name', 'gender', 'is_verified', 'is_adult', 
            'profile_picture', 'relationship'
        ]

    def create(self, validated_data):
        relationship_data = validated_data.pop('relationship')
        user = User.objects.create(**validated_data)
        UserRelationship.objects.create(user=user, **relationship_data)
        return user

    def update(self, instance, validated_data):
        relationship_data = validated_data.pop('relationship', None)

        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create the relationship
        if relationship_data:
            if hasattr(instance, 'relationship'):
                for attr, value in relationship_data.items():
                    setattr(instance.relationship, attr, value)
                instance.relationship.save()
            else:
                UserRelationship.objects.create(user=instance, **relationship_data)

        return instance

