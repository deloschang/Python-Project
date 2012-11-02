from django.conf import settings
from django.template.loader import render_to_string

def analytics(request):
    """
    1. Returns analytics code for Google Analytics
    2. Also returns flashapp id for macromeme generator
    3. Returns standard js files used 
    """
    if not settings.DEBUG:
        # production
        return { 'analytics_code': render_to_string("processors/analytics.html", { 'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY}), 'flashappid': '320238601417173','standard_js': render_to_string("processors/standard_js.html", { 'STATIC_URL': settings.STATIC_URL})}
    else:
        return { 'analytics_code': "", 'flashappid': '479174175436255', 'standard_js': render_to_string("processors/standard_js.html", { 'STATIC_URL': settings.STATIC_URL})}


