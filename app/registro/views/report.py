from django.http import HttpResponse
from django.template.loader import render_to_string
import asyncio
from playwright.async_api import async_playwright
from registro.models import CalificacionAspirante
from django.templatetags.static import static
from datetime import date
from django.conf import settings # Importar settings
from urllib.parse import urljoin # Para unir URLs de forma segura

async def render_pdf_from_html(html_content):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            device_scale_factor=1,
            is_mobile=False,
        )
        await page.set_content(html_content, wait_until="networkidle")
        await page.emulate_media(media="screen")
        await page.wait_for_timeout(100) 
        pdf_bytes = await page.pdf(print_background=True, scale=0.8)
        await browser.close()
        return pdf_bytes

def descargar_pdf(request, pk):
    registro = CalificacionAspirante.objects.select_related('club').get(pk=pk)

    # --- INICIO CAMBIOS ---
    # Asegúrate de tener SITE_URL definido en settings.py
    # ej: SITE_URL = 'http://tu_ip_o_dominio' o usar variables de entorno
    base_url = settings.SITE_URL

    # Obtiene las URLs absolutas de las imágenes usando SITE_URL
    foto_cedula_url = urljoin(base_url, registro.foto_cedula.url) if registro.foto_cedula else None
    foto_fondo_claro_url = urljoin(base_url, registro.foto_fondo_claro.url) if registro.foto_fondo_claro else None
    logo_url = urljoin(base_url, static('img/logo.jpg'))
    logo_colmena = urljoin(base_url, static('img/colmena.jpg'))
    # --- FIN CAMBIOS ---

    # Calcular la edad del jugador
    today = date.today()
    edad = today.year - registro.fecha_nacimiento.year - ((today.month, today.day) < (registro.fecha_nacimiento.month, registro.fecha_nacimiento.day))
    player_names = registro.club.nombre + "-" + registro.nombres + "-" + registro.apellidos
    file_name = f"{player_names}.pdf"
    # Renderiza la plantilla HTML
    html_content = render_to_string(
        'registro/ver-registro.html',
        {
            'registro': registro,
            'foto_cedula_url': foto_cedula_url,
            'foto_fondo_claro_url': foto_fondo_claro_url,
            'logo_url': logo_url,
            'logo_colmena': logo_colmena,
            'edad': edad,
        },
        request=request
    )
    # Genera el PDF usando Playwright
    pdf_bytes = asyncio.run(render_pdf_from_html(html_content))
    # Devuelve el PDF como descarga
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response
