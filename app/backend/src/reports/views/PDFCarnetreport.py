from django.http import HttpResponse
from django.views import View
from playwright.sync_api import sync_playwright
from django.urls import reverse
from clubs.models.Register import Register
from datetime import datetime


class PDFCarnetreport(View):
    def render_pdf_to_bytes(self, url):
        """Renderiza la página con Playwright y devuelve el PDF como bytes."""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(ignore_https_errors=True)
            page.goto(url)

            page.wait_for_load_state("networkidle")

            pdf_bytes = page.pdf(
                format="A4",
                margin={
                    "top": "0.5cm",
                    "right": "0.5cm",
                    "bottom": "0.5cm",
                    "left": "0.5cm",
                },
                print_background=True,
                landscape=False,  # Orientación horizontal para los carnets
            )
            browser.close()
            return pdf_bytes

    def get(self, request, registro_id, *args, **kwargs):
        """Genera un PDF del carnet y lo devuelve como respuesta."""
        carnet_path = reverse(
            "reports:carnet",
            kwargs={"pk": registro_id},
        )
        target_url = request.build_absolute_uri(carnet_path)

        pdf_bytes = self.render_pdf_to_bytes(target_url)

        try:
            registro = Register.objects.get(id=registro_id)
            filename = (
                f"Carnet-{registro.player.last_name}-{registro.player.first_name}-"
                f"{registro.number}-{datetime.now().strftime('%Y%m%d')}.pdf"
            )
        except Register.DoesNotExist:
            filename = f"Carnet-{registro_id}-{datetime.now().strftime('%Y%m%d')}.pdf"

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response