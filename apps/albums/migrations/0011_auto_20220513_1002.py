# Generated by Django 2.2.5 on 2022-05-13 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0010_auto_20220513_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albums',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建者的ID'),
        ),
        migrations.AlterField(
            model_name='useralbum',
            name='albums_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albums.Albums', verbose_name='画册ID'),
        ),
    ]
