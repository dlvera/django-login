from django.shortcuts import redirect
from django.urls import include, path
from .views import UserRegisterView, CustomLoginView, LogoutView, User

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', lambda request: redirect('login')),  # Redireccionar a login por defecto

    # path('accounts/', include('allauth.urls')),  # Agrega las URLs de Allauth

    path('user/', User.as_view(), name='user'),
]
