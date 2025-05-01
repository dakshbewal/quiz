from django.contrib import admin
from django.urls import path, include
from quiz_app import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', include('quiz_app.urls')),
    path('quiz/', include('quiz_app.urls')),
]
