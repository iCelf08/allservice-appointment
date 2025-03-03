def base_template_processor(request):
    """
    Adds BASE_TEMPLATE to the context of all templates.
    """
    return {
        'BASE_TEMPLATE': 'base_admin.html',
    }