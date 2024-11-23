from aplication.core.models import Paciente
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin

from aplication.security.instance.menu_module import MenuModule
class DashboardtListView(LoginRequiredMixin,ListViewMixin,ListView):
    template_name = "core/dashboad/index.html"
    model = Paciente
    context_object_name = 'pacientes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        return context
