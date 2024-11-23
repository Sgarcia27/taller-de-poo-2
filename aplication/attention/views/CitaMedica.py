from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from aplication.attention.models import CitaMedica
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from doctor.utils import save_audit
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)  # Colocar el logger fuera de las clases

def enviar_correo_confirmacion_html(usuario, fecha_cita, hora_cita):
    try:
        asunto = "Confirmación de tu cita"
        html_mensaje = render_to_string(
            "correo_confirmacion.html",
            {"usuario": usuario, "fecha_cita": fecha_cita, "hora_cita": hora_cita},
        )
        correo = EmailMessage(
            asunto, html_mensaje, "bm8385307@gmail.com", [usuario.email]
        )
        correo.content_subtype = "html"
        correo.send()
        logger.info(f"Correo enviado exitosamente a {usuario.email}")
    except Exception as e:
        logger.error(f"Error al enviar correo: {e}")

class CitaMedicaListView(ListView):
    model = CitaMedica
    template_name = 'core/CitaMedica/cita_list.html'
    context_object_name = 'citas'

class CitaMedicaDetailView(DetailView):
    model = CitaMedica
    template_name = 'core/CitaMedica/cita_detail.html'
    context_object_name = 'cita'

class CitaMedicaCreateView(CreateView):
    model = CitaMedica
    fields = ['paciente', 'fecha', 'hora_cita', 'estado']
    template_name = 'core/CitaMedica/cita_form.html'
    success_url = reverse_lazy('core:cita_list')

    def form_valid(self, form):
        """Personaliza la validación del formulario."""
        try:
            response = super().form_valid(form)
            patient = self.object  
            save_audit(self.request, patient, action="A")  
            enviar_correo_confirmacion_html(
                patient.paciente, patient.fecha, patient.hora_cita
            ) 
            messages.success(
                self.request,
                f"Éxito al crear la cita médica para el {patient.fecha} a las {patient.hora_cita}.",
            )
            return response
        except Exception as e:
            logger.error(f"Error en form_valid: {e}")
            messages.error(self.request, "Error al procesar la solicitud.")
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        """Gestiona el caso en que el formulario sea inválido."""
        messages.error(
            self.request, "Error al enviar el formulario. Corrige los errores."
        )
        logger.error(f"Errores en el formulario: {form.errors}")
        return self.render_to_response(self.get_context_data(form=form))

class CitaMedicaUpdateView(UpdateView):
    model = CitaMedica
    fields = ['paciente', 'fecha', 'hora_cita', 'estado']
    template_name = 'core/CitaMedica/cita_form.html'
    success_url = reverse_lazy('core:cita_list')

class CitaMedicaDeleteView(DeleteView):
    model = CitaMedica
    template_name = 'core/CitaMedica/cita_confirm_delete.html'
    success_url = reverse_lazy('core:cita_list')
