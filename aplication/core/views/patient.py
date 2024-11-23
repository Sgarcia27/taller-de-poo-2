from django.urls import reverse_lazy
from aplication.core.forms.patient import PatientForm
from aplication.core.models import Paciente
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from doctor.utils import save_audit
from aplication.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from aplication.security.instance.menu_module import MenuModule


class PatientListView(PermissionMixin, ListViewMixin, ListView):
    template_name = "core/patient/list.html"
    model = Paciente
    permission_required = 'view_paciente'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pacientes'] = context['object_list']
      
        MenuModule(self.request).fill(context)
        return context

    def get_queryset(self):
        self.query = Q()  # Inicializar la consulta
        q1 = self.request.GET.get('q', '')  # Obtener el término de búsqueda
        sex = self.request.GET.get('sex', 'T')  # Obtener el sexo o "T" si no se selecciona nada

        if q1:
            self.query |= Q(nombres__icontains=q1) | Q(apellidos__icontains=q1) | Q(cedula__icontains=q1)
        if sex in ["M", "F"]:
            self.query &= Q(sexo=sex)  # Filtrar por sexo

        return self.model.objects.filter(self.query).order_by('apellidos')



class PatientCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Paciente
    template_name = 'core/patient/form.html'
    form_class = PatientForm
    success_url = reverse_lazy('core:patient_list')
    permission_required = 'add_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Paciente'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        patient = self.object
        save_audit(self.request, patient, action='A')
        messages.success(self.request, f"Éxito al crear al paciente {patient.nombre_completo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))


class PatientUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Paciente
    template_name = 'core/patient/form.html'
    form_class = PatientForm
    success_url = reverse_lazy('core:patient_list')
    permission_required = 'change_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Paciente'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        patient = self.object
        save_audit(self.request, patient, action='M')
        messages.success(self.request, f"Éxito al modificar el paciente {patient.nombre_completo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))


class PatientDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Paciente
    success_url = reverse_lazy('core:patient_list')
    permission_required = 'delete_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Paciente'
        context['description'] = f"¿Desea eliminar al paciente: {self.object.nombre_completo}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, f"Éxito al eliminar al paciente {self.object.nombre_completo}.")
        # Cambiar el estado de eliminado lógico (si es necesario)
        # self.object.deleted = True
        # self.object.save()
        return super().delete(request, *args, **kwargs)


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Paciente

    def get(self, request, *args, **kwargs):
        patient = self.get_object()
        data = {
            'id': patient.id,
            'nombres': patient.nombres,
            'apellidos': patient.apellidos,
            'foto': patient.get_image(),  # Asegúrate de que el método exista en el modelo
            'fecha_nac': patient.fecha_nacimiento,
            'edad': patient.calcular_edad(patient.fecha_nacimiento),
            'dni': patient.cedula,
            'telefono': patient.telefono,
            'direccion': patient.direccion,
            # Añade más campos según tu modelo
        }
        return JsonResponse(data)
