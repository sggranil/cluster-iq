import json

from django.conf import settings
from django.template.response import TemplateResponse
from consumer.models import ConsumerProfile
import geographical.models
from geographical.utils import (
    get_average_income_by_barangay,
    get_average_spent_by_barangay,
    get_most_demand_product_category,
    get_top_demanded_product_categories,
    calculate_demand_intensity,
    apply_dbscan_for_high_demand,
)
from consumer.utils import url_with_query_params


def index(request):
    template_path = 'pages/geographical.page.html'

    query = request.GET
    date = query.get('month', '').split('-')

    if len(date) != 2:
        return url_with_query_params(request, 'consumer:index', **{'month': '01-2025'})

    datasets = ConsumerProfile.objects.filter(
        timestamp__month=int(date[0]), timestamp__year=int(date[1])
    )

    barangays = geographical.models.Barangay.objects.all()

    average_income_per_barangay = get_average_income_by_barangay(datasets, count=5)
    average_spent_per_barangay = get_average_spent_by_barangay(datasets, count=5)
    most_demand_product = get_most_demand_product_category(datasets, count=5)
    top_demanded_product_per_barangay = get_top_demanded_product_categories(datasets, count=5)

    demand_data = calculate_demand_intensity(datasets)

    clustering_results = []
    for category in set(item["category"] for item in demand_data):
        category_data = [item for item in demand_data if item["category"] == category]
        clusters = apply_dbscan_for_high_demand(barangays, category_data)

        for cluster in clusters:
            top_products = get_top_demanded_product_categories(datasets.filter(barangay__name=cluster['name']), count=3)

            cluster['top_3_products'] = [
                {
                    "product_category": product['product_category'],
                    "percentage": product['percentage']
                }
                for product in top_products
            ]

            cluster['intensity'] = int(cluster.get('intensity', 0))
            cluster['cluster'] = int(cluster.get('cluster', -1))

        clustering_results.append({
            "category": category,
            "clusters": clusters
        })

    context = {
        'average_income_barangay': average_income_per_barangay,
        'average_spent_barangay': average_spent_per_barangay,
        'most_demand_product': most_demand_product,
        'demand_per_barangay': top_demanded_product_per_barangay,
        'clustered_data': json.dumps(clustering_results),
        'google_map_api_key': settings.GOOGLE_MAP_API_KEY
    }

    return TemplateResponse(request, template_path, context=context)
