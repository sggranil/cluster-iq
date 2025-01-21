from django.db import models
from geographical.models import Barangay
from market.models import ProductCategory


class ConsumerProfile(models.Model):
    timestamp = models.DateTimeField()
    age_group = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    income_level = models.CharField(max_length=50)
    occupation = models.CharField(max_length=50)
    shopping_frequency = models.CharField(max_length=50)
    product_categories = models.ManyToManyField('market.ProductCategory', related_name="consumers", blank=True)
    shopping_preference = models.CharField(max_length=50)
    influences = models.ManyToManyField('market.ProductInfluences', related_name="consumers", blank=True)
    spending_category = models.CharField(max_length=50)
    product_preferences = models.ManyToManyField('market.ProductPreference', related_name="consumers", blank=True)
    return_likelihood = models.CharField(max_length=50)
    barangay = models.ForeignKey('geographical.Barangay', on_delete=models.SET_NULL, null=True, blank=True)

    def serializer(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "age_group": self.age_group,
            "gender": self.gender,
            "income_level": self.income_level,
            "occupation": self.occupation,
            "shopping_frequency": self.shopping_frequency,
            "product_categories": [category.name for category in self.product_categories.all()],
            "shopping_preference": self.shopping_preference,
            "product_preferences": [preference.name for preference in self.product_preferences.all()],
            "spending_category": self.spending_category,
            "influences": [influence.name for influence in self.influences.all()],
            "return_likelihood": self.return_likelihood,
            "barangay": self.barangay.serialize() if self.barangay else None,
        }
