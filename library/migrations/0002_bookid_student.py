# Generated by Django 4.2.5 on 2023-10-07 06:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_delete_attendance"),
        ("library", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookid",
            name="student",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.studentprofile",
            ),
        ),
    ]
