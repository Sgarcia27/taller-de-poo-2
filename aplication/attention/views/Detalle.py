from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from aplication.attention.models import DetalleAtencion

class DetalleAtencionListView(ListView):
    model = DetalleAtencion
    template_name = 'core/Detalle/detalle_atencion_list.html'
    context_object_name = 'detalles_atencion'

class DetalleAtencionDetailView(DetailView):
    model = DetalleAtencion
    template_name = 'core/Detalle/detalle_atencion_detail.html'
    context_object_name = 'detalle_atencion'

class DetalleAtencionCreateView(CreateView):
    model = DetalleAtencion
    fields = ['atencion', 'medicamento', 'cantidad', 'prescripcion', 'duracion_tratamiento']
    template_name = 'core/Detalle/detalle_atencion_form.html'
    success_url = reverse_lazy('core:detalle_atencion_list')

class DetalleAtencionUpdateView(UpdateView):
    model = DetalleAtencion
    fields = ['atencion', 'medicamento', 'cantidad', 'prescripcion', 'duracion_tratamiento']
    template_name = 'core/Detalle/detalle_atencion_form.html'
    success_url = reverse_lazy('core:detalle_atencion_list')

class DetalleAtencionDeleteView(DeleteView):
    model = DetalleAtencion
    template_name = 'core/Detalle/detalle_atencion_confirm_delete.html'
    success_url = reverse_lazy('core:detalle_atencion_list')
