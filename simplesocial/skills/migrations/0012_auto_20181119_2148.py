# Generated by Django 2.1.2 on 2018-11-20 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0011_auto_20181119_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skilllike',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likeships', to='skills.Skill'),
        ),
    ]