import requests
import cluster_iq.utils

from django.conf import settings
from collections import defaultdict, Counter

from sklearn.cluster import DBSCAN
import numpy as np


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
            top_categories = category_counts.most_common(count)

            top_categories_list = []
            for category, count in top_categories:
                percentage = (count / total_respondents) * 100
                top_categories_list.append({
                    "product_category": category,
                    "percentage": round(percentage, 2),
                })

            top_demand_per_barangay.append({
                "name": barangay,
                "product_category": top_categories_list[0]['product_category'],
                "percentage": top_categories_list[0]['percentage'],
                "top_3_categories": top_categories_list,
            })

    top_demand_per_barangay.sort(key=lambda x: x["percentage"], reverse=True)

    return top_demand_per_barangay[:count]


def calculate_demand_intensity(datasets):
    """
    Calculates demand intensity for all product categories per barangay.
    """
    demand_data = defaultdict(lambda: defaultdict(int))

    for record in datasets:
        if record.product_preferences and record.barangay:
            for category in record.product_preferences.values_list('name', flat=True):
                demand_data[category][record.barangay.name] += 1

    flattened_data = []
    for category, barangay_data in demand_data.items():
        for barangay, intensity in barangay_data.items():
            flattened_data.append({
                "category": category,
                "barangay": barangay,
                "intensity": intensity
            })

    return flattened_data


def apply_dbscan_for_high_demand(barangays, demand_data):
    """
    Apply DBSCAN clustering on barangays with their demand intensity.
    """
    merged_data = []
    for barangay in barangays:
        matching_demand = next((d["intensity"] for d in demand_data if d["barangay"] == barangay.name), 0)
        merged_data.append({
            "name": barangay.name,
            "latitude": barangay.latitude,
            "longitude": barangay.longitude,
            "intensity": matching_demand
        })

    coordinates = np.array([(d["latitude"], d["longitude"]) for d in merged_data if d["intensity"] > 0])
    intensities = np.array([d["intensity"] for d in merged_data if d["intensity"] > 0])

    if coordinates.size == 0:
        for data in merged_data:
            data["cluster"] = -1  # Indicate no cluster
        return merged_data

    dbscan = DBSCAN(eps=0.01, min_samples=2, metric='euclidean')
    clusters = dbscan.fit_predict(coordinates)

    for idx, cluster in enumerate(clusters):
        merged_data[idx]["cluster"] = cluster

    return merged_data

