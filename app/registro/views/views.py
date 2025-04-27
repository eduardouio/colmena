from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML

from registro.models import CalificacionAspirante


def descargar_registro_pdf(request, pk):
    registro = CalificacionAspirante.objects.select_related('club').get(pk=pk)
    html_string = render_to_string('registro/ver-registro.html', {'registro': registro}, request=request)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ficha_{registro.cedula}.pdf"'
    return response


def preview_registro(request, pk):
    registro = CalificacionAspirante.objects.select_related('club').get(pk=pk)
    html_string = render_to_string('registro/ver-registro.html', {'registro': registro}, request=request)
    return HttpResponse(html_string, content_type='text/html')