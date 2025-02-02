# Generated by Django 4.2.3 on 2025-01-21 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('market', '0001_initial'),
        ('geographical', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('age_group', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=10)),
                ('income_level', models.CharField(max_length=50)),
                ('occupation', models.CharField(max_length=50)),
                ('shopping_frequency', models.CharField(max_length=50)),
                ('shopping_preference', models.CharField(max_length=50)),
                ('spending_category', models.CharField(max_length=50)),
                ('return_likelihood', models.CharField(max_length=50)),
                ('barangay', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='geographical.barangay')),
                ('influences', models.ManyToManyField(blank=True, related_name='consumers', to='market.productinfluences')),
                ('product_categories', models.ManyToManyField(blank=True, related_name='consumers', to='market.productcategory')),
                ('product_preferences', models.ManyToManyField(blank=True, related_name='consumers', to='market.productpreference')),
            ],
        ),
    ]
