# Generated by Django 5.1.2 on 2024-11-01 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_userprofile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_images/default.jpg', upload_to='profile_images/'),
        ),
    ]