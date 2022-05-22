# Generated by Django 3.1.7 on 2022-05-22 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='technologies',
            field=models.ManyToManyField(to='main.Technology'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.role'),
        ),
    ]