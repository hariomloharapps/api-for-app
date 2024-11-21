from django.conf import settings

class RelationshipConfig:
    @staticmethod
    def get_relationship_types(gender):
        if gender == 'Male':
            return [
                'Girlfriend',
                'Best Friend',
                'Bestie',
                'Custom'
            ]
        else:
            return [
                'Boyfriend',
                'Best Friend',
                'Bestie',
                'Custom'
            ]

    @staticmethod
    def get_character_personality_pairs():
        return {
            'Best Friend': [
                {
                    'id': 1,
                    'type': 'Supportive & Loyal',
                    'description': 'Always there through thick and thin',
                    'details': 'A reliable friend who offers emotional support, keeps your secrets, and stands by your side no matter what.'
                },
                {
                    'id': 2,
                    'type': 'Adventurous & Fun',
                    'description': 'Loves trying new things and having adventures',
                    'details': 'Spontaneous and exciting, they\'re always up for new experiences.'
                },
                {
                    'id': 3,
                    'type': 'Wise & Mature',
                    'description': 'Thoughtful mentor and advisor',
                    'details': 'Offers wisdom beyond their years, helps you see different perspectives.'
                },
                {
                    'id': 4,
                    'type': 'Goofy & Humorous',
                    'description': 'Always knows how to make you laugh',
                    'details': 'Masters of comedy who brighten your day with their humor.'
                }
            ],
            'Bestie': [
                {
                    'id': 1,
                    'type': 'Supportive & Loyal',
                    'description': 'Always there through thick and thin',
                    'details': 'A reliable friend who offers emotional support, keeps your secrets, and stands by your side no matter what.'
                },
                {
                    'id': 2,
                    'type': 'Adventurous & Fun',
                    'description': 'Loves trying new things and having adventures',
                    'details': 'Spontaneous and exciting, they\'re always up for new experiences.'
                },
                {
                    'id': 3,
                    'type': 'Wise & Mature',
                    'description': 'Thoughtful mentor and advisor',
                    'details': 'Offers wisdom beyond their years, helps you see different perspectives.'
                },
                {
                    'id': 4,
                    'type': 'Goofy & Humorous',
                    'description': 'Always knows how to make you laugh',
                    'details': 'Masters of comedy who brighten your day with their humor.'
                }
            ],
            'Girlfriend': [
                {
                    'id': 5,
                    'type': 'Sweet & Caring',
                    'description': 'Gentle, nurturing, and always there for you',
                    'details': 'A warm and affectionate partner who shows love through small gestures.'
                },
                {
                    'id': 6,
                    'type': 'Playful & Cheerful',
                    'description': 'Brings joy and excitement to your life',
                    'details': 'Energetic and fun-loving, they make every moment special.'
                },
                {
                    'id': 7,
                    'type': 'Shy & Introverted',
                    'description': 'Sweet, thoughtful, and deeply caring',
                    'details': 'Quiet but deeply affectionate, they show love through meaningful gestures.'
                },
                {
                    'id': 8,
                    'type': 'Romantic & Passionate',
                    'description': 'Deeply affectionate and emotionally expressive',
                    'details': 'Intensely romantic and passionate about the relationship.'
                },
                {
                    'id': 9,
                    'type': 'Adult',
                    'description': 'Mature content and themes',
                    'isAdult': True,
                    'details': 'Contains mature themes and content. Age verification required.'
                }
            ],
            'Boyfriend': [
                {
                    'id': 10,
                    'type': 'Protective & Caring',
                    'description': 'Strong, reliable, and nurturing',
                    'details': 'A dependable partner who makes you feel safe and protected.'
                },
                {
                    'id': 11,
                    'type': 'Shy & Sensitive',
                    'description': 'Thoughtful, gentle, and understanding',
                    'details': 'A sensitive soul who connects on a deep emotional level.'
                },
                {
                    'id': 12,
                    'type': 'Romantic & Devoted',
                    'description': 'Affectionate and deeply committed',
                    'details': 'A romantic at heart who loves expressing their feelings.'
                },
                {
                    'id': 13,
                    'type': 'Adult',
                    'description': 'Mature content and themes',
                    'isAdult': True,
                    'details': 'Contains mature themes and content. Age verification required.'
                }
            ]
        }

    @staticmethod
    def get_personality_types(relationship_type):
        character_pairs = RelationshipConfig.get_character_personality_pairs()
        return character_pairs.get(relationship_type, [])