from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from  aplication.attention.models import CostoAtencionDetalle

class CostoAtencionDetalleListView(ListView):
    model = CostoAtencionDetalle
    template_name = "core/costos_detalle/costos_atencion_detalle_list.html"
    context_object_name = "costos_detalle"

class CostoAtencionDetalleCreateView(CreateView):
    model = CostoAtencionDetalle
    fields = ['costo_atencion', 'servicios_adicionales', 'costo_servicio']
    template_name = "core/costos_detalle/costos_atencion_detalle_form.html"
    success_url = reverse_lazy('core:costos_atencion_detalle_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Detalle de Atencion'
        return context

class CostoAtencionDetalleUpdateView(UpdateView):
    model = CostoAtencionDetalle
    fields = ['costo_atencion', 'servicios_adicionales', 'costo_servicio']
    template_name = "core/costos_detalle/costos_atencion_detalle_form.html"
    success_url = reverse_lazy('core:costos_atencion_detalle_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Detalle de Atencion'
        return context

class CostoAtencionDetalleDeleteView(DeleteView):
    model = CostoAtencionDetalle
    template_name = "core/costos_detalle/costos_atencion_detalle_confirm_delete.html"
    success_url = reverse_lazy('core:costos_atencion_detalle_list')
