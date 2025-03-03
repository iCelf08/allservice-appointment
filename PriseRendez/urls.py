from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from django.conf import settings
from PriseRendez.views.redirection import user_dashboard, admin_dashboard , custom_logout , custom_login 



urlpatterns = [
    path('accounts/login/', custom_login, name='account_login'),
    path('accounts/custom-logout/', custom_logout, name='custom_logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('user-dashboard/', user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),
    path('appointment/', include('appointment.urls')), 
    


]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)