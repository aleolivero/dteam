# Generated by Django 3.2 on 2024-01-14 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Coder', '0011_questionsrules_label_last_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Coder.players', verbose_name='Player'),
        ),
    ]
