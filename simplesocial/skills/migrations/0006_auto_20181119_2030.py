# Generated by Django 2.1.2 on 2018-11-20 01:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0005_auto_20181119_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skilllike',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likeships', to='skills.Skill'),
        ),
    ]