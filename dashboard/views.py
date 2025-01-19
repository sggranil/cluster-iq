import django.template.response


def index(request):
    template_path = 'pages/dashboard.page.html'

    return django.template.response.TemplateResponse(request, template_path)
