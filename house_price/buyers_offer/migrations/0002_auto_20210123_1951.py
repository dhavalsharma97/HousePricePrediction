# Generated by Django 3.1.5 on 2021-01-24 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyers_offer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='buyer',
            options={'ordering': ['firstname', 'lastname']},
        ),
        migrations.RenameField(
            model_name='buyer',
            old_name='secondname',
            new_name='lastname',
        ),
    ]