from aplication.attention.models import HorarioAtencion
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView


class HorarioAtencionListView(ListView):
    model = HorarioAtencion
    template_name = 'core/Horariodeatencion/horario_list.html'
    context_object_name = 'horarios'


class HorarioAtencionDetailView(DetailView):
    model = HorarioAtencion
    template_name = 'core/Horariodeatencion/horario_detail.html'
    context_object_name = 'horario'


class HorarioAtencionCreateView(CreateView):
    model = HorarioAtencion
    fields = ['dia_semana', 'hora_inicio', 'hora_fin', 'Intervalo_desde', 'Intervalo_hasta', 'activo']
    template_name = 'core/Horariodeatencion/horario_form.html'
    success_url = reverse_lazy('core:horario_list')
    
    

class HorarioAtencionUpdateView(UpdateView):
    model = HorarioAtencion
    fields = ['dia_semana', 'hora_inicio', 'hora_fin', 'Intervalo_desde', 'Intervalo_hasta', 'activo']
    template_name = 'core/Horariodeatencion/horario_form.html'
    success_url = reverse_lazy('core:horario_list')
