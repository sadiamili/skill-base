# Generated by Django 2.1.2 on 2018-11-19 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0002_auto_20181119_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skilllike',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likeships', to='skills.Skill'),
        ),
    ]
