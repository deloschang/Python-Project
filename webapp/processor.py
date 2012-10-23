from django.conf import settings
from django.template.loader import render_to_string

def analytics(request):
    """
    Returns analytics code for Google Analytics
    """
    if not settings.DEBUG:
        # production
        return { 'analytics_code': render_to_string("analytics/analytics.html", { 'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY}) }
    else:
        return { 'analytics_code': "" }

def hello(request):
    return { 'hello': 'hello'}

