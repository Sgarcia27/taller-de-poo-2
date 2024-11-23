from django.views.generic import TemplateView
from aplication.core.models import Paciente
from aplication.attention.models import CitaMedica
from datetime import date
from aplication.security.instance.menu_module import MenuModule
class HomeTemplateView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Rellenar el contexto con los menús usando MenuModule
        MenuModule(self.request).fill(context)
        
        # Agregar datos personalizados al contexto existente
        context.update({
            "title": "SaludSync",
            "title1": "Sistema Medico", 
            "title2": "Sistema Medico",
            "can_paci": Paciente.cantidad_pacientes(),
            "ultimo_paciente": Paciente.objects.order_by('-id').first(),
            "proximas_citas": CitaMedica.objects.filter(
                fecha=date.today(),
                estado='P'  # Citas pendientes
            ).order_by('hora_cita'),
            "ultima_cita_completada": CitaMedica.objects.filter(
                estado='R'  # Citas realizadas
            ).order_by('-fecha', '-hora_cita').first(),
            "ultima_cita": CitaMedica.objects.order_by(
                '-fecha', '-hora_cita'
            ).first(),
        })
        
        return context
