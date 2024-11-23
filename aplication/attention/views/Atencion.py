from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from aplication.attention.models import Atencion
from aplication.security.instance.menu_module import MenuModule
class AtencionListView(ListView):
    model = Atencion
    template_name = 'core/Atencion/atencion_list.html'
    context_object_name = 'atenciones'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        return context

class AtencionDetailView(DetailView):
    model = Atencion
    template_name = 'core/Atencion/atencion_detail.html'
    context_object_name = 'atencion'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        return context

class AtencionCreateView(CreateView):
    model = Atencion
    fields = ['paciente', 'diagnostico', 'motivo_consulta', 'tratamiento', 'comentario']
    template_name = 'core/Atencion/atencion_form.html'
    success_url = reverse_lazy('core:atencion_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        return context

class AtencionUpdateView(UpdateView):
    model = Atencion
    fields = ['paciente', 'diagnostico', 'motivo_consulta', 'tratamiento', 'comentario']
    template_name = 'core/Atencion/atencion_form.html'
    success_url = reverse_lazy('core:atencion_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        return context

class AtencionDeleteView(DeleteView):
    model = Atencion
    template_name = 'core/Atencion/atencion_confirm_delete.html'
    success_url = reverse_lazy('core:atencion_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        return context