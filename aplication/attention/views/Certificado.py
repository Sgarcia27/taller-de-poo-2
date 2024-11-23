from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from aplication.attention.models import Certificado
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.shortcuts import get_object_or_404
class CertificadoPDFView(View):
    def get(self, request, pk):
        certificado = get_object_or_404(Certificado, pk=pk)
        # Renderizar la plantilla como HTML
        html_content = render_to_string('core/certificados/certificado_pdf.html', {'certificado': certificado})
        # Convertir el HTML en PDF
        pdf = HTML(string=html_content).write_pdf()
        # Devolver el PDF como respuesta
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="certificado_{certificado.id}.pdf"'
        return response

class CertificadoListView(ListView):
    model = Certificado
    template_name = 'core/certificados/lista.html'
    context_object_name = 'certificados'

class CertificadoCreateView(CreateView):
    model = Certificado
    fields = ['paciente', 'doctor', 'motivo', 'detalles', 'firmado', 'archivo_pdf']
    template_name = 'core/certificados/formulario.html'
    success_url = reverse_lazy('core:listacertificado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = 'create'
        return context


class CertificadoUpdateView(UpdateView):
    model = Certificado
    fields = ['paciente', 'doctor', 'motivo', 'detalles', 'firmado', 'archivo_pdf']
    template_name = 'core/certificados/formulario.html'
    success_url = reverse_lazy('core:listacertificado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = 'update'
        return context
class CertificadoDeleteView(DeleteView):
    model = Certificado
    template_name = 'core/certificados/confirmar_eliminacion.html'
    success_url = reverse_lazy('core:listacertificado')
