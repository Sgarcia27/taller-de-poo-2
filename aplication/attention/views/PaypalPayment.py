from django.core.mail import EmailMessage
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin

# Asegúrate de que WeasyPrint esté importado correctamente
from aplication.attention.models import Pago, CostosAtencion, ServiciosAdicionales
from aplication.attention.forms.Pago import PagoForm
import paypalrestsdk
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from weasyprint import HTML
from django.conf import settings
from aplication.security.instance.menu_module import MenuModule
# Configurar PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # Cambia a "live" para producción
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

class PagoListView(LoginRequiredMixin, ListView):
    template_name = "attention/pagos/list.html"
    model = Pago
    context_object_name = 'pagos'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        return context

    def get_queryset(self):
        return Pago.objects.select_related('paciente', 'costo_atencion').prefetch_related('servicios_adicionales', 'examenes_medicos')

class PagoCreateView(LoginRequiredMixin, CreateView):
    model = Pago
    template_name = 'attention/pagos/form.html'
    form_class = PagoForm
    success_url = reverse_lazy('attention:pago_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        return context
    def form_valid(self, form):
        metodo_pago = form.cleaned_data['metodo_pago']
        if metodo_pago == 'PayPal':
            return self.process_paypal_payment(form)
        else:
            return self.process_cash_payment(form)

    def process_cash_payment(self, form):
        pago = form.save(commit=False)
        pago.pagado = True
        pago.save()
        form.save_m2m()  # Guardar la relación ManyToMany

        # Actualizar el campo pagado de los exámenes médicos
        for examen in form.cleaned_data['examenes_medicos']:
            examen.pagado = True
            examen.save()

        return redirect(self.success_url)

    def process_paypal_payment(self, form):
        costo_atencion = form.cleaned_data['costo_atencion']
        servicios_adicionales = form.cleaned_data['servicios_adicionales']
        examenes_medicos = form.cleaned_data['examenes_medicos']
        total_servicios = sum(servicio.costo_servicio for servicio in servicios_adicionales)
        total_examenes = sum(examen.precio_examen for examen in examenes_medicos)
        total = costo_atencion.total + total_servicios + total_examenes

        items = [{
            "name": "Costo Atención",
            "sku": "001",
            "price": str(costo_atencion.total),
            "currency": "USD",
            "quantity": 1
        }]

        for servicio in servicios_adicionales:
            items.append({
                "name": servicio.nombre_servicio,  # Asegúrate de usar el atributo correcto
                "sku": f"servicio_{servicio.id}",
                "price": str(servicio.costo_servicio),
                "currency": "USD",
                "quantity": 1
            })

        for examen in examenes_medicos:
            items.append({
                "name": examen.nombre_examen,
                "sku": f"examen_{examen.id}",
                "price": str(examen.precio_examen),
                "currency": "USD",
                "quantity": 1
            })

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": self.request.build_absolute_uri(reverse_lazy('attention:paypal_execute')) + f"?costo_atencion_id={costo_atencion.id}",
                "cancel_url": self.request.build_absolute_uri(reverse_lazy('attention:pago_list'))
            },
            "transactions": [{
                "item_list": {
                    "items": items
                },
                "amount": {
                    "total": str(total),
                    "currency": "USD"
                },
                "description": f"Costo de atención para {costo_atencion.atencion.paciente.nombre_completo}"
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    break
        
            # Guardar los servicios adicionales y exámenes médicos en la sesión
            self.request.session['servicios_adicionales'] = [servicio.id for servicio in servicios_adicionales]
            self.request.session['examenes_medicos'] = [examen.id for examen in examenes_medicos]
        
            return redirect(approval_url)
        else:
            print(payment.error)
            return redirect(self.success_url)

def paypal_execute(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    costo_atencion_id = request.GET.get('costo_atencion_id')
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        costo_atencion = get_object_or_404(CostosAtencion, pk=costo_atencion_id)
        
        # Crear el objeto Pago
        pago = Pago.objects.create(
            paciente=costo_atencion.atencion.paciente,
            costo_atencion=costo_atencion,
            metodo_pago='PayPal',
            pagado=True
        )
        
        # Obtener los servicios adicionales y exámenes médicos desde la sesión
        servicios_adicionales_ids = request.session.get('servicios_adicionales', [])
        examenes_medicos_ids = request.session.get('examenes_medicos', [])
        
        # Asignar los servicios adicionales y exámenes médicos al pago
        pago.servicios_adicionales.set(servicios_adicionales_ids)
        pago.examenes_medicos.set(examenes_medicos_ids)
        
        # Marcar el costo de atención como pagado
        costo_atencion.pagado = True
        costo_atencion.save()
        
        return redirect('attention:pago_list')
    else:
        print(payment.error)
        return redirect('attention:pago_list')

class PagoDetailView(LoginRequiredMixin, DetailView):
    model = Pago
    template_name = 'attention/pagos/detail.html'
    context_object_name = 'pago'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        MenuModule(self.request).fill(context)
        pago = self.object
        total_servicios = sum(servicio.costo_servicio for servicio in pago.servicios_adicionales.all())
        total_examenes = sum(examen.precio_examen for examen in pago.examenes_medicos.all())
        total_pagado = pago.costo_atencion.total + total_servicios + total_examenes
        context['total_pagado'] = total_pagado
        context['examenes_medicos'] = pago.examenes_medicos.all()
        return context
    
class PagoDeleteView(LoginRequiredMixin, DeleteView):
    model = Pago
    template_name = 'attention/pago/confirm_delete.html'
    success_url = reverse_lazy('attention:pago_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)

class PagoComprobanteView(View):
    def get(self, request, *args, **kwargs):
        pago = get_object_or_404(Pago, pk=self.kwargs['pk'])
        total_servicios = sum(servicio.costo_servicio for servicio in pago.servicios_adicionales.all())
        total_examenes = sum(examen.precio_examen for examen in pago.examenes_medicos.all())
        total_pagado = pago.costo_atencion.total + total_servicios + total_examenes
        template_path = 'attention/pago/comprobante.html'
        context = {
            'pago': pago,
            'total_pagado': total_pagado,
            'servicios_adicionales': pago.servicios_adicionales.all(),
            'examenes_medicos': pago.examenes_medicos.all(),
            'nombre_completo_paciente': pago.paciente.nombre_completo
        }
        template = get_template(template_path)
        html = template.render(context)
        
        # Generar el PDF
        pdf = BytesIO()
        HTML(string=html).write_pdf(pdf)
        
        # Configurar la respuesta HTTP para descargar el PDF
        response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="comprobante_pago_{pago.pk}.pdf"'
        
        return response
    
def verificar_pago_paciente(request):
    paciente_id = request.GET.get('paciente_id')
    ha_pagado = Pago.objects.filter(paciente_id=paciente_id, pagado=True).exists()
    return JsonResponse({'ha_pagado': ha_pagado})


