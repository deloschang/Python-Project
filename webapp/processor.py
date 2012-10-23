from django.conf import settings
from django.template.loader import render_to_string

def analytics(request):
    """
    Returns analytics code for Google Analytics
    """
    if not settings.DEBUG:
        # production
        return { 'analytics_code': render_to_string("analytics/analytics.html", { 'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY}), 'flashappid': '320238601417173' }
    else:
        return { 'analytics_code': "", 'flashappid': '479174175436255'}


