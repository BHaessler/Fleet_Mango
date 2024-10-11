# context_processors.py

from .models import FooterContent

def footer_content(request):
    try:
        footer_content = FooterContent.objects.first()  # Get the first (and only) footer content
    except FooterContent.DoesNotExist:
        footer_content = None  # Handle the case where no FooterContent exists
    return {
        'footer_content': footer_content
    }