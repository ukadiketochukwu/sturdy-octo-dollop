from django.urls import path
from .views import register_doctor, register_patient, login_view, profile_view, translate_text

urlpatterns = [
    path('register/doctor/', register_doctor, name='register_doctor'),
    path('register/patient/', register_patient, name='register_patient'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
     path('translate/', translate_text, name='translate_text'),
]
