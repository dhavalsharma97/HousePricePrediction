# Generated by Django 3.1.5 on 2021-01-24 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyers_offer', '0003_auto_20210123_1953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buyer',
            name='payment',
        ),
        migrations.AddField(
            model_name='buyer',
            name='payment',
            field=models.ManyToManyField(help_text='Enter the payment', to='buyers_offer.Payment'),
        ),
    ]
