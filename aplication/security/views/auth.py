from django.views.generic import FormView, CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout, authenticate
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from aplication.security.forms.user import CustomUserCreationForm
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from aplication.security.instance.menu_module import MenuModule

User = get_user_model()

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "security/auth/register.html"
    success_url = reverse_lazy("core:dashboard")  # Cambia 'dashboard' por una ruta válida

    permission_required = 'add_user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar User'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        try:
            patient_group = Group.objects.get(name="PACIENTE")
            user.groups.add(patient_group)
        except Group.DoesNotExist:
            messages.error(self.request, "El grupo 'Paciente' no existe. Por favor, créalo.")
            return redirect(self.success_url)
        
        backend = 'django.contrib.auth.backends.ModelBackend'  
        user.backend = backend
        auth_login(self.request, user)
        messages.success(self.request, f"Cuenta creada exitosamente para {user.email}. Ahora has iniciado sesión.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        email = form.data.get('email') 
        if User.objects.filter(email=email).exists():
            messages.error(self.request, "El email ya se encuentra en uso")
        return super().form_invalid(form)

class SigninView(FormView):
    form_class = AuthenticationForm
    template_name = "security/auth/login.html"
    success_url = reverse_lazy("core:home")  # Cambia 'dashboard' por la ruta válida

    def form_valid(self, form):
        username = form.cleaned_data.get('username')  # Esto será el username del formulario
        password = form.cleaned_data.get('password')

        # Autenticar al usuario con username directamente
        user = authenticate(self.request, username=username, password=password)

        if user is not None and user.is_active:
            backend = 'django.contrib.auth.backends.ModelBackend'
            user.backend = backend
            auth_login(self.request, user)
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, "Credenciales incorrectas o cuenta inactiva.")
            return self.form_invalid(form)



def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('security:custom_login')


class PerfilView(DetailView):
    template_name = "security/auth/profile.html"
    model = User

    def get_object(self):
        # Devuelve solo el usuario actual
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Perfil del Usuario"
        MenuModule(self.request).fill(context)  # Solo si este módulo está implementado
        return context
