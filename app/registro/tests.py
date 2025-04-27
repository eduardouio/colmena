from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import date, timedelta
from .models import Club, CalificacionAspirante

class ClubModelTest(TestCase):
    """Tests para el modelo Club"""
    
    def setUp(self):
        self.club = Club.objects.create(nombre="Club de Prueba")
    
    def test_club_creation(self):
        """Verifica que un club se crea correctamente"""
        self.assertEqual(self.club.nombre, "Club de Prueba")
        self.assertEqual(str(self.club), "Club de Prueba")

class CalificacionAspiranteModelTest(TestCase):
    """Tests para el modelo CalificacionAspirante"""
    
    def setUp(self):
        self.club = Club.objects.create(nombre="Club de Prueba")
        # Definir fechas para diferentes edades
        self.fecha_edad_10 = date.today() - timedelta(days=365 * 10 + 1)
        self.fecha_edad_11 = date.today() - timedelta(days=365 * 11 + 1)
        self.fecha_edad_9 = date.today() - timedelta(days=365 * 9 + 1)
        self.fecha_edad_17 = date.today() - timedelta(days=365 * 17 + 1)
        self.fecha_edad_18 = date.today() - timedelta(days=365 * 18 + 1)
        self.fecha_edad_39 = date.today() - timedelta(days=365 * 39 + 1)
        self.fecha_edad_40 = date.today() - timedelta(days=365 * 40 + 1)
        
        # Crear archivos de prueba
        self.foto_test = SimpleUploadedFile(
            "foto.jpg", 
            b"archivo_de_prueba", 
            content_type="image/jpeg"
        )
        
    def test_crear_aspirante_valido(self):
        """Verifica la creación de un aspirante válido"""
        aspirante = CalificacionAspirante(
            email="test@example.com",
            temporada="2025",
            club=self.club,
            categoria="senior",
            nombres="Juan",
            apellidos="Pérez",
            cedula="1722919725",
            fecha_nacimiento=self.fecha_edad_18,
            numero_jugador=10,  # <= 30 para adultos
            tiene_pases=False,
            foto_fondo_claro=self.foto_test,
            foto_cedula=self.foto_test,
            recalificacion=False
        )
        aspirante.full_clean()  # Debería pasar sin errores
        aspirante.save()
        self.assertEqual(CalificacionAspirante.objects.count(), 1)
        self.assertEqual(str(aspirante), "Juan Pérez (1722919725)")
        
    def test_categorias_niños(self):
        """Verifica validaciones de la categoría 'niños'"""
        # Caso 1: Niño de 10 años con número <= 30 (válido)
        aspirante = CalificacionAspirante(
            email="test@example.com",
            temporada="2025",
            club=self.club,
            categoria="niños",
            nombres="Niño",
            apellidos="Prueba",
            cedula="1722919725",
            fecha_nacimiento=self.fecha_edad_10,
            numero_jugador=25,  # <= 30, válido
            tiene_pases=False,
            foto_fondo_claro=self.foto_test,
            foto_cedula=self.foto_test,
            recalificacion=False
        )
        aspirante.full_clean()  # No debería dar error
        
        # Caso 2: Niño de 10 años con número > 30 (inválido)
        aspirante.numero_jugador = 35  # > 30, inválido
        with self.assertRaises(ValidationError):
            aspirante.full_clean()
            
        # Caso 3: Niño de 9 años (menor de 10) con número > 30 (válido)
        aspirante.fecha_nacimiento = self.fecha_edad_9
        aspirante.full_clean()  # No debería dar error
        
        # Caso 4: Niño de 9 años con número <= 30 (inválido)
        aspirante.numero_jugador = 25  # <= 30, inválido para menores de 10
        with self.assertRaises(ValidationError):
            aspirante.full_clean()
    
    def test_categorias_senior_femenino(self):
        """Verifica validaciones de categorías 'senior' y 'femenino'"""
        # Caso 1: Adulto (18+) con número <= 30 (válido)
        aspirante = CalificacionAspirante(
            email="test@example.com",
            temporada="2025",
            club=self.club,
            categoria="senior",
            nombres="Adulto",
            apellidos="Prueba",
            cedula="1722919725",
            fecha_nacimiento=self.fecha_edad_18,
            numero_jugador=25,  # <= 30, válido para 18+
            tiene_pases=False,
            foto_fondo_claro=self.foto_test,
            foto_cedula=self.foto_test,
            recalificacion=False
        )
        aspirante.full_clean()  # No debería dar error
        
        # Caso 2: Adulto (18+) con número > 30 (inválido)
        aspirante.numero_jugador = 35  # > 30, inválido para 18+
        with self.assertRaises(ValidationError):
            aspirante.full_clean()
            
        # Caso 3: Menor (17) con número > 30 (válido)
        aspirante.fecha_nacimiento = self.fecha_edad_17
        aspirante.full_clean()  # No debería dar error
        
        # Caso 4: Menor (17) con número <= 30 (inválido)
        aspirante.numero_jugador = 25  # <= 30, inválido para menores
        with self.assertRaises(ValidationError):
            aspirante.full_clean()
            
        # Lo mismo para categoría 'femenino'
        aspirante.categoria = "femenino"
        aspirante.fecha_nacimiento = self.fecha_edad_18
        aspirante.numero_jugador = 25  # <= 30, válido para 18+
        aspirante.full_clean()  # No debería dar error
        
    def test_categoria_master(self):
        """Verifica validaciones de la categoría 'master'"""
        # Caso 1: Adulto 40+ con número <= 30 (válido)
        aspirante = CalificacionAspirante(
            email="test@example.com",
            temporada="2025",
            club=self.club,
            categoria="master",
            nombres="Master",
            apellidos="Prueba",
            cedula="1722919725",
            fecha_nacimiento=self.fecha_edad_40,
            numero_jugador=25,  # <= 30, válido para 40+
            tiene_pases=False,
            foto_fondo_claro=self.foto_test,
            foto_cedula=self.foto_test,
            recalificacion=False
        )
        aspirante.full_clean()  # No debería dar error
        
        # Caso 2: Adulto 40+ con número > 30 (inválido)
        aspirante.numero_jugador = 35  # > 30, inválido para 40+
        with self.assertRaises(ValidationError):
            aspirante.full_clean()
            
        # Caso 3: Menor de 40 con número > 30 (válido)
        aspirante.fecha_nacimiento = self.fecha_edad_39
        aspirante.full_clean()  # No debería dar error
        
        # Caso 4: Menor de 40 con número <= 30 (inválido)
        aspirante.numero_jugador = 25  # <= 30, inválido para menores de 40
        with self.assertRaises(ValidationError):
            aspirante.full_clean()
            
class RegistroAspiranteViewTest(TestCase):
    """Tests para la vista de registro de aspirantes"""
    
    def setUp(self):
        self.client = Client()
        self.club = Club.objects.create(nombre="Club de Prueba")
        self.registro_url = reverse('registro:formulario')
        self.success_url = reverse('registro:success')
        
        # Fechas y edades
        self.fecha_adulto = date.today() - timedelta(days=365 * 20)  # 20 años
        self.fecha_menor = date.today() - timedelta(days=365 * 15)   # 15 años
        
        # Archivos de prueba
        self.foto_test = SimpleUploadedFile(
            "foto.jpg", 
            b"archivo_de_prueba", 
            content_type="image/jpeg"
        )
        self.doc_test = SimpleUploadedFile(
            "autorizacion.pdf", 
            b"archivo_de_prueba", 
            content_type="application/pdf"
        )
        
    def test_acceso_a_formulario(self):
        """Verifica que se puede acceder al formulario"""
        response = self.client.get(self.registro_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro/form-registro.html')
        
    def test_registro_exitoso_adulto(self):
        """Verifica que un adulto puede registrarse correctamente"""
        form_data = {
            'email': 'adulto@example.com',
            'temporada': '2025',
            'club': self.club.id,
            'categoria': 'senior',
            'nombres': 'Juan',
            'apellidos': 'Pérez',
            'cedula': '1722919725',
            'fecha_nacimiento': self.fecha_adulto.strftime('%Y-%m-%d'),
            'numero_jugador': 10,
            'tiene_pases': 'False',
            'foto_fondo_claro': self.foto_test,
            'foto_cedula': self.foto_test,
            'recalificacion': 'False',
        }
        
        response = self.client.post(self.registro_url, form_data, format='multipart')
        self.assertEqual(CalificacionAspirante.objects.count(), 1)
        self.assertRedirects(response, self.success_url)
        
    def test_registro_incorrecto_adulto_numero_invalido(self):
        """Verifica que se validan los números de camiseta para adultos"""
        form_data = {
            'email': 'adulto@example.com',
            'temporada': '2025',
            'club': self.club.id,
            'categoria': 'senior',
            'nombres': 'Juan',
            'apellidos': 'Pérez',
            'cedula': '1722919725',
            'fecha_nacimiento': self.fecha_adulto.strftime('%Y-%m-%d'),
            'numero_jugador': 35,  # > 30, inválido para adultos
            'tiene_pases': 'False',
            'foto_fondo_claro': self.foto_test,
            'foto_cedula': self.foto_test,
            'recalificacion': 'False',
        }
        
        response = self.client.post(self.registro_url, form_data, format='multipart')
        self.assertEqual(response.status_code, 200)  # Se queda en el formulario
        self.assertEqual(CalificacionAspirante.objects.count(), 0)  # No se crea el registro
        
    def test_registro_menor_sin_autorizacion(self):
        """Verifica que se requiere autorización para menores"""
        form_data = {
            'email': 'menor@example.com',
            'temporada': '2025',
            'club': self.club.id,
            'categoria': 'senior',
            'nombres': 'Joven',
            'apellidos': 'Pérez',
            'cedula': '1722919725',
            'fecha_nacimiento': self.fecha_menor.strftime('%Y-%m-%d'),
            'numero_jugador': 35,  # > 30, válido para menores
            'tiene_pases': 'False',
            'foto_fondo_claro': self.foto_test,
            'foto_cedula': self.foto_test,
            'recalificacion': 'False',
            # No incluimos autorización
        }
        
        response = self.client.post(self.registro_url, form_data, format='multipart')
        self.assertEqual(response.status_code, 200)  # Se queda en el formulario
        self.assertEqual(CalificacionAspirante.objects.count(), 0)  # No se crea el registro
        self.assertFormError(response, 'form', 'autorizacion_menor', 'La autorización es obligatoria para menores de edad.')
        
    def test_registro_exitoso_menor_con_autorizacion(self):
        """Verifica que un menor puede registrarse con autorización"""
        form_data = {
            'email': 'menor@example.com',
            'temporada': '2025',
            'club': self.club.id,
            'categoria': 'senior',
            'nombres': 'Joven',
            'apellidos': 'Pérez',
            'cedula': '1722919725',
            'fecha_nacimiento': self.fecha_menor.strftime('%Y-%m-%d'),
            'numero_jugador': 35,  # > 30, válido para menores
            'tiene_pases': 'False',
            'autorizacion_menor': self.doc_test,  # Incluimos autorización
            'foto_fondo_claro': self.foto_test,
            'foto_cedula': self.foto_test,
            'recalificacion': 'False',
        }
        
        response = self.client.post(self.registro_url, form_data, format='multipart')
        self.assertEqual(CalificacionAspirante.objects.count(), 1)
        self.assertRedirects(response, self.success_url)
        
    def test_success_view(self):
        """Verifica que la vista de éxito funciona correctamente"""
        response = self.client.get(reverse('registro:success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro/success.html')
        
    def test_error_view(self):
        """Verifica que la vista de error funciona correctamente"""
        response = self.client.get(reverse('registro:error'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registro/error.html')
