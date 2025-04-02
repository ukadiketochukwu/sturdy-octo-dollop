import os
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserForm, DoctorForm, PatientForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

# Registration view for Doctor
def register_doctor(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Add user to the 'Doctors' group
            doctor_group = Group.objects.get(name='Doctors')
            user.groups.add(doctor_group)

            # Create Doctor profile and save it
            doctor_profile = doctor_form.save(commit=False)
            doctor_profile.user = user
            doctor_profile.save()

            messages.success(request, "Doctor account created successfully.")
            login(request, user)  # Log the user in immediately
            return redirect('profile')
            
    else:
        user_form = UserForm()
        doctor_form = DoctorForm()

    return render(request, 'register_doctor.html', {'user_form': user_form, 'doctor_form': doctor_form})


API_KEY = os.getenv('AZURE_TRANSLATOR_API_KEY')
ENDPOINT = os.getenv('TRANSLATOR_ENDPOINT')
REGION = os.getenv('AZURE_REGION')
def translate_text(request):
    text = request.GET.get('text')
    target_language = request.GET.get('targetLanguage')
    
    if not text or not target_language:
        return JsonResponse({'error': 'Text and target language are required.'}, status=400)
    
    url = f"{ENDPOINT}/translate?api-version=3.0&to={target_language}"

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': API_KEY,
        'Ocp-Apim-Subscription-Region': REGION
    }

    body = [{'Text': text}]

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        translation = response.json()
        print(translation)
        #response_data = {"translatedText": translation}
        return JsonResponse(translation, safe=False)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

# Registration view for Patient
def register_patient(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        patient_form = PatientForm(request.POST)

        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Add user to the 'Patients' group
            patient_group = Group.objects.get(name='Patients')
            user.groups.add(patient_group)

            # Create Patient profile and save it
            patient_profile = patient_form.save(commit=False)
            patient_profile.user = user
            patient_profile.save()

            messages.success(request, "Patient account created successfully.")
            login(request, user)  # Log the user in immediately
            return redirect('profile')

    else:
        user_form = UserForm()
        patient_form = PatientForm()

    return render(request, 'register_patient.html', {'user_form': user_form, 'patient_form': patient_form})

# Profile view that fetches the user's name and role
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    user = request.user

    # Check if the user is a doctor or a patient
    if hasattr(user, 'doctor'):
        role = 'Doctor'
    elif hasattr(user, 'patient'):
        role = 'Patient'
    else:
        role = 'Unknown'
        return redirect('login')  # Redirect to profile after login

    return render(request, 'profile.html', {
        'user': user,
        'role': role
    })

# Custom Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Successfully logged in.")
            return redirect('profile')  # Redirect to profile after login
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})
