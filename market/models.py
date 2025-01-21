from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductPreference(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductInfluences(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name