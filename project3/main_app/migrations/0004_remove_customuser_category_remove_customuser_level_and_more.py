# Generated by Django 4.1.7 on 2023-03-16 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_customuser_category_alter_customuser_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='category',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='level',
        ),
        migrations.CreateModel(
            name='UserCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.customuser')),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='level',
            field=models.ManyToManyField(through='main_app.UserCategory', to='main_app.category'),
        ),
    ]
