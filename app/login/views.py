from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView
from app.login.forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.auth import login
import sweetify

# Clase para manejar el registro de usuarios
from django.contrib import messages

class UserRegisterView(CreateView):
    template_name = 'login.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Procesar los datos del formulario
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        email = form.cleaned_data['email']

        # Crear el nuevo usuario
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        # Loggear al nuevo usuario
        login(self.request, user)

        # Usar el sistema de mensajes de Django para mostrar un mensaje de éxito
        messages.success(self.request, 'Registro exitoso.')

        # Redireccionar al formulario de autenticación
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        # Mensajes de error para campos vacíos
        if not form.cleaned_data.get('username') and 'username' not in form.errors:
            messages.error(self.request, 'El nombre de usuario es obligatorio.')
        if not form.cleaned_data.get('email') and 'email' not in form.errors:
            messages.error(self.request, 'El correo electrónico es obligatorio.')
        if not form.cleaned_data.get('password1') and 'password1' not in form.errors:
            messages.error(self.request, 'La contraseña es obligatoria.')
        if not form.cleaned_data.get('password2') and 'password2' not in form.errors:
            messages.error(self.request, 'Debe repetir la contraseña.')

        # Verificar los errores de validación
        if 'password2' in form.errors:
            messages.error(self.request, 'Las contraseñas no coinciden.')
        if 'username' in form.errors:
            messages.error(self.request, 'El nombre de usuario ya está en uso.')
        if 'email' in form.errors:
            messages.error(self.request, 'El correo electrónico ya está en uso.')

        # Mensaje genérico si no se cumplen las reglas
        if not messages.get_messages(self.request):
            messages.error(self.request, 'Error al crear usuario. Verifique los datos ingresados.')

        # Renderizar el contexto
        context = self.get_context_data(form=form)
        context['has_error'] = True
        return self.render_to_response(context)

# Clase para manejar la autenticación de inicio de sesión
class CustomLoginView(LoginView):
    template_name = 'login.html'  # Nombre del template a usar
     
    # Sobrescribir método form_valid para agregar lógica personalizada
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if remember_me:
            self.request.session.set_expiry(1209600)  # Establecer expiración en 2 semanas
        else:
            self.request.session.set_expiry(0)  # No establecer expiración
        
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            if user.is_superuser:
                return redirect('adminn')  # Redirigir al administrador si es superusuario
            else:
                return redirect('user')  # Redirigir al usuario normal
        else:
            form.add_error(None, 'Nombre de usuario o contraseña inválido.')  # Agregar un error si los datos son incorrectos
            return self.form_invalid(form)


class User(TemplateView):
    template_name = "user.html"


# Clase para manejar la salida de sesión
class LogoutView(View):
    def get(self, request):
        logout(request)  # Desconectar al usuario
        return redirect('home')  # Redirigir a la página principal