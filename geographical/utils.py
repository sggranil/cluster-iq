import requests
import cluster_iq.utils

from django.conf import settings
from collections import defaultdict, Counter


def geocode_address(address):
    url = settings.GOOGLE_MAP_API_URL
    params = {
        'address': f'{address}, {settings.CITY}',
        'key': settings.GOOGLE_MAP_API_KEY
    }

    response = requests.get(url, params=params)
    result = response.json()

    if response.status_code == 200 and result['status'] == 'OK':
        location = result['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        return lat, lng
    else:
        return None, None


def get_average_income_by_barangay(datasets, count=3, barangay=None):
    barangay_spending = defaultdict(list)

    for record in datasets:
        if record.income_level and record.barangay:
            income = cluster_iq.utils.extract_spending_value(record.income_level)
            barangay_spending[record.barangay.name].append(income)

    barangay_data = [
        {
            "name": barangay,
            "average": sum(values) / len(values) if values else 0,
        }
        for barangay, values in barangay_spending.items()
    ]

    barangay_data = sorted(barangay_data, key=lambda x: x["average"], reverse=True)

    return barangay_data[:count]


def get_average_spent_by_barangay(datasets, count=3, barangay=None):
    barangay_spending = defaultdict(list)

    for record in datasets:
        if record.spending_category and record.barangay:
            spending_value = cluster_iq.utils.extract_spending_value(record.spending_category)
            barangay_spending[record.barangay.name].append(spending_value)

    barangay_data = [
        {
            "name": barangay,
            "average": sum(values) / len(values) if values else 0,
        }
        for barangay, values in barangay_spending.items()
    ]

    barangay_data = sorted(barangay_data, key=lambda x: x["average"], reverse=True)

    return barangay_data[:count]


def get_most_demand_product_category(datasets, count=3):
    category_counter = Counter()

    for record in datasets:
        if record.product_categories:
            category_counter.update([pref.name for pref in record.product_categories.all()])

    most_demanded_categories = [{"name": category} for category, _ in category_counter.most_common()]

    return most_demanded_categories[:count]


def get_top_demanded_product_categories(datasets, count=3):
    barangay_category_counts = defaultdict(Counter)
    total_respondents_per_barangay = defaultdict(int)

    for record in datasets:
        if record.influences and record.barangay:
            total_respondents_per_barangay[record.barangay.name] += 1
            for pref in record.influences.all():
                barangay_category_counts[record.barangay.name][pref.name] += 1

    top_demand_per_barangay = []
    for barangay, category_counts in barangay_category_counts.items():
        total_respondents = total_respondents_per_barangay[barangay]
        if total_respondents > 0:
            top_category, count = category_counts.most_common(1)[0]
            percentage = (count / total_respondents) * 100
            top_demand_per_barangay.append({
                "name": barangay,
                "product_category": top_category,
                "percentage": round(percentage, 2),
            })

    top_demand_per_barangay.sort(key=lambda x: x["percentage"], reverse=True)

    return top_demand_per_barangay[:count]

