from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from clubs.models.Register import Register
from clubs.models.Season import Season
from clubs.models.Club import Club


class CheckPlayerNumberView(LoginRequiredMixin, View):
    """Vista API para verificar disponibilidad de número de jugador."""

    def get(self, request):
        """Verifica si un número está disponible para un jugador en una temporada/club."""
        try:

            number = request.GET.get("number")
            season_id = request.GET.get("season_id")
            club_id = request.GET.get("club_id")

            if not all([number, season_id, club_id]):
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Faltan parámetros requeridos (number, season_id, club_id)",
                    },
                    status=400,
                )

            try:
                number = int(number)
                season_id = int(season_id)
                club_id = int(club_id)
            except ValueError:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Los parámetros deben ser valores numéricos válidos",
                    },
                    status=400,
                )

            try:
                club = Club.objects.get(id=club_id)
                if not request.user.is_superuser and club.users != request.user:
                    return JsonResponse(
                        {
                            "success": False,
                            "error": "No tienes permisos para verificar números en este club",
                        },
                        status=403,
                    )
            except Club.DoesNotExist:
                return JsonResponse(
                    {"success": False, "error": "Club no encontrado"}, status=404
                )

            try:
                season = Season.objects.select_related("categorie").get(id=season_id)
            except Season.DoesNotExist:
                return JsonResponse(
                    {"success": False, "error": "Temporada no encontrada"}, status=404
                )

            exists = Register.objects.filter(
                season=season, club=club, number=number
            ).exists()

            if exists:

                register = Register.objects.select_related("player").get(
                    season=season, club=club, number=number
                )

                return JsonResponse(
                    {
                        "success": True,
                        "available": False,
                        "message": f"Número {number} ya asignado a {register.player.full_name}",
                        "player_info": {
                            "name": register.player.full_name,
                            "national_id": register.player.national_id,
                            "status": register.status,
                        },
                    }
                )

            category = season.categorie

            if number < 1 or number > 999:
                return JsonResponse(
                    {
                        "success": False,
                        "available": False,
                        "message": "El número debe estar entre 1 y 999",
                        "valid_range": False,
                    }
                )

            response_data = {
                "success": True,
                "available": True,
                "message": f"Número {number} disponible",
                "category_info": {
                    "name": category.name,
                    "adult_range": {
                        "min": category.min_number_player,
                        "max": category.max_number_player,
                    },
                    "youth_range": {
                        "min": category.min_number_youth_player,
                        "max": category.max_number_youth_player,
                    },
                },
            }

            in_adult_range = (
                category.min_number_player <= number <= category.max_number_player
            )
            in_youth_range = (
                category.min_number_youth_player
                <= number
                <= category.max_number_youth_player
            )

            if not in_adult_range and not in_youth_range:
                response_data["warning"] = (
                    f"Número {number} fuera de los rangos permitidos para la categoría {category.name}"
                )
                response_data["valid_range"] = False
            else:
                response_data["valid_range"] = True
                if in_youth_range and not in_adult_range:
                    response_data["range_type"] = "youth"
                    response_data["info"] = "Número en rango juvenil (menor de 18 años)"
                elif in_adult_range and not in_youth_range:
                    response_data["range_type"] = "adult"
                    response_data["info"] = "Número en rango adulto"
                else:
                    response_data["range_type"] = "both"
                    response_data["info"] = "Número válido para adultos y juveniles"

            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse(
                {"success": False, "error": f"Error al verificar número: {str(e)}"},
                status=500,
            )
