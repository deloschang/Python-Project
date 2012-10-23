from django.conf import settings

def macromeme_key(request):
    #raise Exception
    if not settings.DEBUG:
        # production
        return { 'flashappid': "320238601417173" }
    else:
        # development
        return { 'flashappid': "479174175436255" }
