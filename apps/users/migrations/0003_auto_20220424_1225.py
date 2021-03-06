# Generated by Django 2.2.5 on 2022-04-24 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_author_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hobby',
            field=models.CharField(max_length=20, null=True, verbose_name='爱好'),
        ),
        migrations.AddField(
            model_name='user',
            name='signature',
            field=models.CharField(max_length=100, null=True, verbose_name='个人签名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='author_img',
            field=models.ImageField(default='group1/M00/00/02/wKixgGJlF96AHdruAAFmeY1_DW0295.jpg', null=True, upload_to='img/'),
        ),
    ]
