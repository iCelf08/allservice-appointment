from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.shortcuts import redirect
from django.contrib.auth import logout


@login_required
def user_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')  
    else:
        return render(request, 'user_dashboard.html')  

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')  
    else:
        return render(request, 'admin_dashboard.html')  



@login_required
def user_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard') 
    else:
        return redirect('user_dashboard')  




# class CustomLoginView(LoginView):
#     template_name = 'registration/login.html'

#     def get_success_url(self):
#         if self.request.user.is_staff:
#             print("self.request.user.is_staff")
#             return '/admin-dashboard/'
#         return '/user-dashboard/'


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

# views.py - Function-based approach with debugging
def custom_login(request):
    print("custom_login view called!")

    if request.method == 'POST':
        # Add debugging output
        print("Login form submitted with data:", request.POST)
        
        # Create the form with POST data
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            print("Form is valid, logging in user")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Redirect based on user type
                redirect_url = '/admin-dashboard/' if user.is_staff else '/user-dashboard/'
                print(f"User authenticated, redirecting to {redirect_url}")
                return redirect(redirect_url)
            else:
                print("Authentication failed despite valid form")
        else:
            # Print form errors for debugging
            print("Form validation errors:", form.errors)
    else:
        form = AuthenticationForm()
    
    # If we get here, something went wrong or it's a GET request
    return render(request, 'registration/login.html', {'form': form})


def custom_logout(request):
    logout(request)  
    return redirect('account_login') 