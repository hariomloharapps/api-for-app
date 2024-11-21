# views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.base import ContentFile
import base64
from datetime import datetime
from groq import Groq
import os
from django.conf import settings
# from .models import UserVerification, User

def analyze_image_content(image_path):
    """
    Analyze image using Groq Vision API to detect if the person is 18+ and human
    """
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        client = Groq(api_key=settings.GROQ_API_KEY)
        
        prompt = """Please analyze this image carefully and answer the following questions:
                   1. Is there a human person in this image?
                   2. Does the person appear to be 18 years or older?
                   3. Is the image appropriate (non-explicit/non-adult content)?
                   
                   Respond in this exact format:
                   HUMAN: YES/NO
                   AGE_18_PLUS: YES/NO
                   APPROPRIATE: YES/NO"""

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="llama-3.2-11b-vision-preview",
        )
        
        # Parse the response
        result = response.choices[0].message.content.strip()
        lines = result.split('\n')
        analysis = {}
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':')
                analysis[key.strip()] = value.strip().upper() == 'YES'
        
        return {
            'is_human': analysis.get('HUMAN', False),
            'is_adult': analysis.get('AGE_18_PLUS', False),
            'is_appropriate': analysis.get('APPROPRIATE', False)
        }
    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        return {
            'is_human': False,
            'is_adult': False,
            'is_appropriate': False
        }

@api_view(['POST'])
def verify_user_image(request):
    """
    API endpoint to verify if image contains a human who is 18+ and appropriate
    """
    try:
        # Create a test user if not exists
        user, created = User.objects.get_or_create(
            name="Test User",
            defaults={
                'gender': 'Male',
                'personality': 'INTROVERT'
            }
        )
        
        verification, created = UserVerification.objects.get_or_create(user=user)

        # Handle form-data request with file upload
        if request.FILES.get('profile_picture'):
            verification.profile_picture = request.FILES['profile_picture']
            verification.save()
        else:
            return Response(
                {'error': 'No image provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the full path of the saved image
        image_path = os.path.join(settings.MEDIA_ROOT, str(verification.profile_picture))
        
        # Analyze the image
        analysis = analyze_image_content(image_path)
        
        # Determine verification status
        is_verified = all([
            analysis['is_human'],
            analysis['is_adult'],
            analysis['is_appropriate']
        ])
        
        # Update verification status
        verification.is_verified = is_verified
        if is_verified:
            verification.verification_date = datetime.now()
        verification.save()
        
        # Prepare detailed response
        response_message = {
            'verification_status': is_verified,
            'details': {
                'human_detected': analysis['is_human'],
                'is_adult': analysis['is_adult'],
                'appropriate_content': analysis['is_appropriate']
            },
            'message': 'Image verification complete'
        }
        
        # Add specific failure reasons if not verified
        if not is_verified:
            failures = []
            if not analysis['is_human']:
                failures.append("No human detected in image")
            if not analysis['is_adult']:
                failures.append("Person appears to be under 18")
            if not analysis['is_appropriate']:
                failures.append("Inappropriate content detected")
            response_message['failure_reasons'] = failures
        
        return Response(response_message)

    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    






















from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .llm_service import LLMService
import logging
from functools import lru_cache

# Cache timestamp format to avoid repeated strftime calls
@lru_cache(maxsize=1)
def get_timestamp():
    return datetime.now().strftime("%H:%M")

# Initialize LLM service with error handling
try:
    llm = LLMService(api_key="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")
except Exception as e:
    logging.error(f"Error initializing LLM service: {e}")
    llm = None

# Pre-define common response structures
ERROR_RESPONSES = {
    'no_message': {
        'error': 'No message provided',
        'status': 'error'
    },
    'empty_message': {
        'error': 'Empty message',
        'status': 'error'
    },
    'llm_unavailable': {
        'error': 'LLM service unavailable',
        'status': 'error'
    }
}

class ChatAPIView(APIView):
    def post(self, request):
        try:
            # Quick validation of request data
            data = request.data
            user_message = data.get('message', '').strip()
            
            if 'message' not in data:
                response = ERROR_RESPONSES['no_message'].copy()
                response['timestamp'] = get_timestamp()
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            if not user_message:
                response = ERROR_RESPONSES['empty_message'].copy()
                response['timestamp'] = get_timestamp()
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            if llm is None:
                response = ERROR_RESPONSES['llm_unavailable'].copy()
                response['timestamp'] = get_timestamp()
                return Response(response, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # Get response from LLM service
            result = llm.get_response(
                user_message,
                data.get('history', []),  # No need to assign to variable if used once
            )

            timestamp = get_timestamp()
            if result.get('status') == 'error':
                return Response({
                    'error': result.get('error', 'Unknown error occurred'),
                    'timestamp': timestamp,
                    'status': 'error'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                'response': result['response'],
                'timestamp': timestamp,
                'status': 'success'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            error_msg = str(e)
            logging.error(f"Error in chat API: {error_msg}")
            return Response({
                'error': f"An unexpected error occurred: {error_msg}",
                'timestamp': get_timestamp(),
                'status': 'error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
















from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserNestedSerializer

class CreateUserWithRelationship(APIView):
    def post(self, request):
        serializer = UserNestedSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User and their AI companion created successfully!", "user_id": user.user_id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
