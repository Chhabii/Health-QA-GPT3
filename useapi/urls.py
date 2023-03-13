from django.urls import path 
from .views import create_question
urlpatterns = [
    path("",create_question,name='create-question')
]