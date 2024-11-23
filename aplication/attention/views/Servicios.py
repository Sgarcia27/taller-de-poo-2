from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,DeleteView
from aplication.attention.models import ServiciosAdicionales

class ServiciosAdicionalesListView(ListView):
    model = ServiciosAdicionales
    template_name = 'core/servicios_adicionales/servicios_adicionales_list.html'
    context_object_name = 'servicios_adicionales'

class ServiciosAdicionalesCreateView(CreateView):
    model = ServiciosAdicionales
    template_name = 'core/servicios_adicionales/servicios_adicionales_form.html'
    fields = ['nombre_servicio', 'costo_servicio', 'descripcion', 'activo']
    success_url = reverse_lazy('core:servicios_list')

class ServiciosAdicionalesUpdateView(UpdateView):
    model = ServiciosAdicionales
    template_name = 'core/servicios_adicionales/servicios_adicionales_form.html'
    fields = ['nombre_servicio', 'costo_servicio', 'descripcion', 'activo']
    success_url = reverse_lazy('core:servicios_list')

class ServiciosAdicionalesDeleteView(DeleteView):
    model = ServiciosAdicionales
    success_url = reverse_lazy('core:servicios_list')
