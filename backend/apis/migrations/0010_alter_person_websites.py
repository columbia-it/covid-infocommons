# Generated by Django 4.0.2 on 2022-12-02 02:55

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0009_person_comments_person_desired_collaboration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='websites',
            field=django_mysql.models.ListCharField(models.CharField(blank=True, max_length=1000, null=True), blank=True, max_length=1000, null=True, size=None),
        ),
    ]
