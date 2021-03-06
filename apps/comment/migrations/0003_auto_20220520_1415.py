# Generated by Django 2.2.5 on 2022-05-20 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20220520_0246'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='like_num',
            field=models.IntegerField(default=0, verbose_name='喜欢数量'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='aid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albums.Albums', verbose_name='画册的ID'),
        ),
    ]
