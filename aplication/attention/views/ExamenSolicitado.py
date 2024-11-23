from aplication.attention.models import ExamenSolicitado
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from django.utils import timezone

class ExamenSolicitadoListView(ListView):
    model = ExamenSolicitado
    template_name = 'core/ExamenSolicitado/examen_solicitado_list.html'
    context_object_name = 'solicitados1'


class ExamenSolicitadoDetailView(DetailView):
    model = ExamenSolicitado
    template_name = 'core/ExamenSolicitado/examen_solicitado_detail.html'
    context_object_name ='solicitado'

class ExamenSolicitadoCreateView(CreateView):
    model = ExamenSolicitado
    fields=['nombre_examen','paciente','resultado','comentario','estado']    
    template_name='core/ExamenSolicitado/examen_solicitado_crear.html'
    success_url = reverse_lazy('core:ExamenSolicitado_list')
    def form_valid(self, form):
        form.instance.fecha_solicitud = timezone.now()  # Asigna la fecha actual automáticamente
        return super().form_valid(form)

class ExamenSolicitadoUpdateView(UpdateView):
    model = ExamenSolicitado
    fields=['nombre_examen','paciente','resultado','comentario','estado']
    template_name='core/ExamenSolicitado/examen_solicitado_editar.html'
    success_url = reverse_lazy('core:ExamenSolicitado_list')

class ExamenSolicitadoDeleteView(DeleteView):
    model = ExamenSolicitado
    template_name='core/ExamenSolicitado/examen_solicitado_eliminar.html'
    success_url = reverse_lazy('core:ExamenSolicitado_list')
