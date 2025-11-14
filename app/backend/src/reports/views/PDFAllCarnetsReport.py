from django.http import HttpResponse
from django.views import View
from playwright.sync_api import sync_playwright
from django.urls import reverse
from clubs.models.Categorie import Categorie
from datetime import datetime


class PDFAllCarnetsReport(View):
    def render_pdf_to_bytes(self, url):
        """Renderiza la página con Playwright y devuelve el PDF como bytes."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(ignore_https_errors=True)
            page.goto(url)

            page.wait_for_load_state("networkidle")
            
            # Esperar un poco más para asegurar que las imágenes se carguen
            page.wait_for_timeout(2000)

            pdf_bytes = page.pdf(
                format="A4",
                margin={
                    "top": "0.5cm",
                    "right": "0.5cm",
                    "bottom": "0.5cm",
                    "left": "0.5cm",
                },
                print_background=True,
                landscape=False  # Orientación vertical para múltiples carnets
            )
            browser.close()
            return pdf_bytes

    def get(self, request, categoria_id, *args, **kwargs):
        """Genera un PDF de todos los carnets de una categoría y lo devuelve como respuesta."""
        carnets_path = reverse(
            "reports:carnets_categoria",
            kwargs={"categoria_id": categoria_id},
        )
        target_url = request.build_absolute_uri(carnets_path)

        pdf_bytes = self.render_pdf_to_bytes(target_url)

        try:
            categoria = Categorie.objects.get(id=categoria_id)
            filename = (
                f"Carnets-{categoria.name}-"
                f"{datetime.now().strftime('%Y%m%d')}.pdf"
            )
        except Categorie.DoesNotExist:
            filename = f"Carnets-Categoria-{categoria_id}-{datetime.now().strftime('%Y%m%d')}.pdf"

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
