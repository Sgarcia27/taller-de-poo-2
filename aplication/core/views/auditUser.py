from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from aplication.security.models import AuditUser
from django.http import JsonResponse
from aplication.security.mixins.mixins import  ListViewMixin, PermissionMixin
from aplication.security.instance.menu_module import MenuModule

class AuditUserListView(PermissionMixin, ListViewMixin, ListView):
    template_name = "security/admin/audituser/list.html"
    model = AuditUser
    context_object_name = 'audit_users'
    permission_required = 'view_audituser'
    paginate_by = 8
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pacientes'] = context['object_list']
        MenuModule(self.request).fill(context)
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return self.model.objects.filter(usuario__username__icontains=query).order_by('-fecha', 'hora')
        return self.model.objects.all().order_by('-fecha', 'hora')

class AuditUserDetailView(LoginRequiredMixin, DetailView):
    model = AuditUser

    def get(self, request, *args, **kwargs):
        audit_user = self.get_object()
        data = {
            'id': audit_user.id,
            'usuario': audit_user.usuario.username,
            'tabla': audit_user.tabla,
            'registroid': audit_user.registroid,
            'accion': audit_user.accion,
            'fecha': audit_user.fecha,
            'hora': audit_user.hora,
            'estacion': audit_user.estacion,
        }
        return JsonResponse(data)