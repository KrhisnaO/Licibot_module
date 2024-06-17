from django.utils.deprecation import MiddlewareMixin
from django.db import transaction
from .models import ErrorHistory
import traceback

class ErrorLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, (ValueError, TypeError)):
            try:
                with transaction.atomic():
                    tipo_vista = request.path
                    descripcion = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))

                    ErrorHistory.objects.create(
                        tipo_vista=tipo_vista,
                        descripcion=descripcion
                    )
            except Exception as e:
                print(f"Error al registrar el error en el historial: {str(e)}")