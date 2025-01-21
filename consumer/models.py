from django.db import models


class ConsumerProfile(models.Model):
    age_group = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    income_level = models.CharField(max_length=50)
    occupation = models.CharField(max_length=50)
    shopping_frequency = models.CharField(max_length=50)
    shopping_preference = models.CharField(max_length=50)
    spending_category = models.CharField(max_length=50)
    return_likelihood = models.CharField(max_length=50)
