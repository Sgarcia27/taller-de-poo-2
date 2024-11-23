from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,DeleteView
from aplication.attention.models import CostosAtencion

class CostosAtencionListView(ListView):
    model = CostosAtencion
    template_name = 'core/costos_atencion/costos_atencion_list.html'
    context_object_name = 'costos_atencion'

class CostosAtencionCreateView(CreateView):
    model = CostosAtencion
    template_name = 'core/costos_atencion/costos_atencion_form.html'
    fields = ['atencion', 'total', 'activo']
    success_url = reverse_lazy('core:CostosAtencion_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Costo de Atención'
        return context

class CostosAtencionUpdateView(UpdateView):
    model = CostosAtencion
    template_name = 'core/costos_atencion/costos_atencion_form.html'
    fields = ['atencion', 'total', 'activo']
    success_url = reverse_lazy('core:CostosAtencion_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Costo de Atención'
        return context

class CostosAtencionDeleteView(DeleteView):
    model = CostosAtencion
    success_url = reverse_lazy('core:CostosAtencion_list')