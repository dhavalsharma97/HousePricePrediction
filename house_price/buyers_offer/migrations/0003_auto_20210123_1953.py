# Generated by Django 3.1.5 on 2021-01-24 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyers_offer', '0002_auto_20210123_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='paymenttype',
            field=models.CharField(choices=[('Cash', 'Cash'), ('Loan', 'Loan')], help_text='Enter a type of payment', max_length=50),
        ),
    ]
