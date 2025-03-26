from django.urls import path
from .views import Verify2FAView, ActivateView, RegisterView, LoginView, LogoutView, ActivationSentView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('activation_sent/', ActivationSentView.as_view(), name='activation_sent'),
    path('verify-2fa/', Verify2FAView.as_view(), name='verify_2fa'),

]