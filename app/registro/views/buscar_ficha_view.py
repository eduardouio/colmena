from django.http import JsonResponse
from ..models import CalificacionAspirante

def buscar_ficha(request):
    cedula = request.GET.get('cedula', '')
    
    if not cedula:
        return JsonResponse({'error': 'El número de cédula es requerido'}, status=400)
    
    try:
        # Buscar el registro por cédula
        registro = CalificacionAspirante.objects.filter(cedula=cedula).first()
        
        if registro:
            return JsonResponse({'id': registro.pk})
        else:
            return JsonResponse({'error': 'No se encontró ningún registro con esa cédula'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': f'Error al buscar ficha: {str(e)}'}, status=500)
