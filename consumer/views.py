import django.http
import django.template.response
import django.http.response
import cluster_iq.utils
import consumer.utils

from consumer.forms import CSVUploadForm


def index(request):
    template_path = 'pages/consumer.page.html'
    shopping_preferences = cluster_iq.utils.chart_count_formatter(
        ['In-store', 'Online'],
        [60, 40]
    )
    product_preferences = cluster_iq.utils.chart_count_formatter(
        ['Food and Beverages', 'Personal Care', 'Clothing', 'Electronics'],
        [45, 30, 15, 10]
    )
    spending_patterns = cluster_iq.utils.chart_count_formatter(
        ['18-24', '25-34', '35-44', '45+'],
        [1500, 2500, 3500, 4000]
    )

    context = {
        "shopping_preferences": shopping_preferences,
        "product_preferences": product_preferences,
        "spending_patterns": spending_patterns
    }

    return django.template.response.TemplateResponse(request, template_path, context=context)


def upload_datasets(request):
    template_path = 'pages/consumer.page.html'
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']

            serialized_data = consumer.utils.serialize_datasets(csv_file)

            return django.http.JsonResponse({'status': 'success', 'data': serialized_data})
        else:
            return django.template.response.TemplateResponse(request, template_path, {'form': form})

    form = CSVUploadForm()
    return django.template.response.TemplateResponse(request, template_path, {'form': form})
