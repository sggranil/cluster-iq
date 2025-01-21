import django.http
import django.template.response
import django.http.response
import django.views.decorators.http

import cluster_iq.utils
import consumer.utils
import consumer.models
import geographical.models
import market.models

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

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
        "spending_patterns": spending_patterns,
    }

    return django.template.response.TemplateResponse(request, template_path, context=context)


@django.views.decorators.http.require_POST
def upload_datasets(request):
    try:
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            serialized_data = consumer.utils.serialize_datasets(csv_file)

            field_mapping = [
                "timestamp",
                "age_group",
                "gender",
                "income_level",
                "occupation",
                "shopping_frequency",
                "product_categories",
                "shopping_preference",
                "product_preferences",
                "spending_category",
                "influences",
                "return_likelihood",
                "barangay",
            ]

            success_count = 0
            duplicate_count = 0
            error_occurred = False

            for data in serialized_data:
                values = list(data.values())

                if len(values) != len(field_mapping):
                    raise ValueError("The number of fields in the data does not match the field mapping.")

                defaults = {field: value for field, value in zip(field_mapping, values)}

                timestamp_str = defaults.get('timestamp')
                if timestamp_str:
                    try:
                        timestamp = consumer.utils.parse_timestamp(timestamp_str)
                        defaults['timestamp'] = timestamp
                    except ValueError as e:
                        if not error_occurred:
                            messages.error(request, str(e))
                            error_occurred = True
                        continue
                else:
                    if not error_occurred:
                        messages.error(request, "Missing timestamp value.")
                        error_occurred = True
                    continue

                if consumer.models.ConsumerProfile.objects.filter(timestamp=defaults['timestamp']).exists():
                    duplicate_count += 1
                    continue

                barangay_name = defaults.get('barangay')
                if barangay_name:
                    try:
                        barangay_instance = geographical.models.Barangay.objects.get(name=barangay_name)
                        defaults['barangay'] = barangay_instance
                    except  geographical.models.Barangay.DoesNotExist:
                        if not error_occurred:
                            messages.error(request, f"Barangay '{barangay_name}' not found.")
                            error_occurred = True
                        continue

                product_category_names = defaults.get('product_categories', '').split(';')
                product_preferences_names = defaults.get('product_preferences', '').split(';')
                influences_names = defaults.get('influences', '').split(';')

                product_categories = []
                for name in product_category_names:
                    category, created = market.models.ProductCategory.objects.get_or_create(name=name)
                    if created:
                        product_categories.append(category)
                    else:
                        duplicate_count += 1

                product_preferences = []
                for name in product_preferences_names:
                    preference, created = market.models.ProductPreference.objects.get_or_create(name=name)
                    if created:
                        product_preferences.append(preference)
                    else:
                        duplicate_count += 1

                influences = []
                for name in influences_names:
                    influence, created = market.models.ProductInfluences.objects.get_or_create(name=name)
                    if created:
                        influences.append(influence)
                    else:
                        duplicate_count += 1

                consumer_profile = consumer.models.ConsumerProfile.objects.create(
                    timestamp=defaults['timestamp'],
                    age_group=defaults['age_group'],
                    gender=defaults['gender'],
                    income_level=defaults['income_level'],
                    occupation=defaults['occupation'],
                    shopping_frequency=defaults['shopping_frequency'],
                    shopping_preference=defaults['shopping_preference'],
                    spending_category=defaults['spending_category'],
                    return_likelihood=defaults['return_likelihood'],
                    barangay=defaults['barangay'],
                )

                consumer_profile.product_categories.set(product_categories)
                consumer_profile.product_preferences.set(product_preferences)
                consumer_profile.influences.set(influences)

                success_count += 1

            if success_count > 0:
                messages.success(request, f"{success_count} new record(s) uploaded successfully.")
            if duplicate_count > 0:
                messages.info(request, f"{duplicate_count} existing record(s) were skipped because they already exist.")
            if success_count == 0 and duplicate_count == 0:
                messages.warning(request, "No records were uploaded or skipped. Please check the data.")

        else:
            if not error_occurred:
                messages.error(request, "Invalid form data. Please upload a valid CSV file.")
    except Exception as e:
        if not error_occurred:
            messages.error(request, f"An error occurred: {str(e)}")

    return redirect(reverse('consumer:index'))
