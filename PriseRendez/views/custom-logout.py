from django.shortcuts import redirect
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)  # Django's built-in logout function
    return redirect('login')  # Redirect to the login page after logout