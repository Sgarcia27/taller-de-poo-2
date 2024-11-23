from django.urls import reverse_lazy
from aplication.core.forms.employee import EmployeeForm
from aplication.core.models import Empleado
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from aplication.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from aplication.security.instance.menu_module import MenuModule
from doctor.utils import save_audit

class EmployeeListView( PermissionMixin, ListViewMixin, ListView):
    permission_required = 'view_empleado'
    template_name = "core/employee/list.html"
    model = Empleado
    context_object_name = 'empleados'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        return context
    def get_queryset(self):
        query = Q()
        q1 = self.request.GET.get('q')
        if q1 is not None:
            query.add(Q(nombres__icontains=q1), Q.OR)
            query.add(Q(apellidos__icontains=q1), Q.OR)
            query.add(Q(cedula__icontains=q1), Q.OR)
        return self.model.objects.filter(query).order_by('apellidos')

class EmployeeCreateView(PermissionMixin, CreateViewMixin, CreateView):
    permission_required = 'add_empleado'
    model = Empleado
    template_name = 'core/employee/form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('core:employee_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Empleado'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        employee = self.object
        save_audit(self.request, employee, action='A')
        messages.success(self.request, f"Éxito al crear al empleado {employee.nombres} {employee.apellidos}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class EmployeeUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    permission_required = 'change_empleado'
    model = Empleado
    template_name = 'core/employee/form.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('core:employee_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Empleado'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        employee = self.object
        save_audit(self.request, employee, action='M')
        messages.success(self.request, f"Éxito al modificar al empleado {employee.nombres} {employee.apellidos}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class EmployeeDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    permission_required = 'delete_empleado'
    model = Empleado
    success_url = reverse_lazy('core:employee_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Empleado'
        context['description'] = f"¿Desea eliminar al empleado: {self.object.nombres} {self.object.apellidos}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente al empleado {self.object.nombres} {self.object.apellidos}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class EmployeeDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    
    model = Empleado

    def get(self, request, *args, **kwargs):
        employee = self.get_object()
        data = {
            'id': employee.id,
            'nombres': employee.nombres,
            'apellidos': employee.apellidos,
            'cedula': employee.cedula,
            'fecha_nacimiento': employee.fecha_nacimiento,
            'cargo': employee.cargo.nombre,
            'sueldo': employee.sueldo,
            'direccion': employee.direccion,
            'latitud': employee.latitud,
            'longitud': employee.longitud,
            'foto': employee.foto.url if employee.foto else None,
            'activo': employee.activo,
        }
        return JsonResponse(data)
