from django.views import View
from django.views.generic import FormView, TemplateView, RedirectView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .models import CustomUser
from .forms import RegisterForm, LoginForm, OTPTokenForm
from .tokens import account_activation_token
from django_otp import login as otp_login


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('activation_sent')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.send_activation_email(user, form.cleaned_data.get('email'))
        return super().form_valid(form)

    def send_activation_email(self, user, to_email):
        mail_subject = 'Activa tu cuenta'
        message = render_to_string('users/activate_account.html', {
            'user': user,
            'domain': get_current_site(self.request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if self.request.is_secure() else 'http'
        })
        EmailMessage(mail_subject, message, to=[to_email]).send(fail_silently=False)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        
        if not form.cleaned_data['remember_me']:
            self.request.session.set_expiry(0)
            
        return super().form_valid(form)


class LogoutView(RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, '¡Cuenta activada correctamente!')
            return redirect('login')
        return HttpResponse('Enlace de activación inválido o expirado.')


class ActivationSentView(TemplateView):
    template_name = 'users/activation_sent.html'


@method_decorator(login_required, name='dispatch')
class Verify2FAView(FormView):
    template_name = 'users/verify_2fa.html'
    form_class = OTPTokenForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        try:
            device = self.request.user.totpdevice_set.get()
            if device.verify_token(form.cleaned_data['token']):
                otp_login(self.request, device)
                return super().form_valid(form)
            messages.error(self.request, 'Token inválido.')
        except:
            messages.error(self.request, 'Dispositivo 2FA no configurado.')
        return self.form_invalid(form)

