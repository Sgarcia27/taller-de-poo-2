from django.urls import path
from aplication.security.views.auth import SignupView, SigninView, logout_view, PerfilView

app_name = 'security'

urlpatterns = [
    path('custom-register/', SignupView.as_view(), name='custom_register'),  # Ruta para registro
    path('custom-login/', SigninView.as_view(), name='custom_login'),        # Ruta para inicio de sesión
    path('logout/', logout_view, name='logout'),                             # Ruta para cierre de sesión
    path('profile/', PerfilView.as_view(), name='profile'),                  # Ruta para perfil de usuario
]
