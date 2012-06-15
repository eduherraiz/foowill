def debug_mode(request):
    from django.conf import settings
    return {'DEBUG': settings.DEBUG} 
