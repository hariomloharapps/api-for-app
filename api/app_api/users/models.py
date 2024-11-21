# apps/relationships/models.py
from django.db import models
import uuid
from django.core.exceptions import ValidationError
from datetime import date
from .config import RelationshipConfig

class User(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    
    user_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    # date_of_birth = models.DateField()
    is_verified = models.BooleanField(default=False)
    is_adult = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def __str__(self):
        return f"{self.name} ({self.user_id})"

class UserRelationship(models.Model):
    RELATIONSHIP_TYPES = (
        ('Girlfriend', 'Girlfriend'),
        ('Boyfriend', 'Boyfriend'),
        ('Bestie', 'Bestie'),
        ('Best Friend', 'Best Friend'),
        ('Custom', 'Custom'),
    )
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='relationships'
    )
    relationship_type = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_TYPES
    )
    personality_type = models.IntegerField()
    custom_name = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    ai_name = models.CharField(
        max_length=50,
        help_text="Name of the AI companion"
    )
    bio = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        help_text="Short biography or description of the AI companion"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Relationship'
        verbose_name_plural = 'User Relationships'
        unique_together = ('user', 'relationship_type', 'personality_type')

    def clean(self):
        personalities = RelationshipConfig.get_personality_types(self.relationship_type)
        selected_personality = next(
            (p for p in personalities if p['id'] == self.personality_type),
            None
        )
        
        if selected_personality and selected_personality.get('isAdult', False) and not self.user.is_adult:
            raise ValidationError({
                'personality_type': "Adult verification required for this personality type."
            })
        
        if not self.ai_name:
            raise ValidationError({
                'ai_name': "AI companion name is required."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_personality_display(self):
        personalities = RelationshipConfig.get_personality_types(self.relationship_type)
        personality = next(
            (p['type'] for p in personalities if p['id'] == self.personality_type),
            'Unknown'
        )
        return personality

    def __str__(self):
        return f"{self.user.name}'s {self.ai_name} ({self.get_relationship_type_display()} - {self.get_personality_display()})"