from django.urls import reverse_lazy
from aplication.core.forms.diagnosis import DiagnosticoForm
from aplication.core.models import Diagnostico
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from doctor.utils import save_audit
from django.http import JsonResponse
from aplication.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from aplication.security.instance.menu_module import MenuModule


class DiagnosisListView(PermissionMixin, ListViewMixin, ListView):
    template_name = "core/diagnosis/list.html"
    model = Diagnostico
    permission_required = 'view_diagnostico'
    context_object_name = 'diagnosticos'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        return context
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return self.model.objects.filter(descripcion__icontains=query).order_by('descripcion')
        return self.model.objects.all().order_by('descripcion')

class DiagnosisCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Diagnostico
    permission_required = 'add_diagnostico'
    template_name = 'core/diagnosis/form.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('core:diagnosis_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Diagnóstico'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        diagnostico = self.object
        save_audit(self.request, diagnostico, action='A')
        messages.success(self.request, f"Éxito al crear el diagnóstico {diagnostico.descripcion}.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class DiagnosisUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Diagnostico
    permission_required = 'change_diagnostico'
    template_name = 'core/diagnosis/form.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('core:diagnosis_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Diagnóstico'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        diagnostico = self.object
        save_audit(self.request, diagnostico, action='M')
        messages.success(self.request, f"Éxito al modificar el diagnóstico {diagnostico.descripcion}.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class DiagnosisDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Diagnostico
    permission_required = 'delete_diagnostico'
    success_url = reverse_lazy('core:diagnosis_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Diagnóstico'
        context['description'] = f"¿Desea eliminar el diagnóstico: {self.object.descripcion}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar el diagnóstico {self.object.descripcion}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class DiagnosisDetailView(LoginRequiredMixin, DetailView):
    model = Diagnostico

    def get(self, request, *args, **kwargs):
        diagnostico = self.get_object()
        data = {
            'id': diagnostico.id,
            'codigo': diagnostico.codigo,
            'descripcion': diagnostico.descripcion,
            'datos_adicionales': diagnostico.datos_adicionales,
            'activo': diagnostico.activo,
        }
        return JsonResponse(data)