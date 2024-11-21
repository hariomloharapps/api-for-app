# urls.py
from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('verify-image/', views.verify_user_image, name='verify-image'),
    path('chat/', ChatAPIView.as_view(), name='chat'),
path('api/create-user-with-relationships/', CreateUserWithRelationship.as_view(), name='create-user-with-relationships'),


]
