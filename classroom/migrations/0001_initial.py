# Generated by Django 4.2.5 on 2023-10-07 05:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0002_delete_attendance"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=25, unique=True)),
                ("name", models.CharField(max_length=250)),
                ("grade", models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name="Class",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "unique_field",
                    models.CharField(
                        blank=True, max_length=250, null=True, unique=True
                    ),
                ),
                (
                    "batch",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.batch",
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.department",
                    ),
                ),
                (
                    "regulation",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.regulation",
                    ),
                ),
                (
                    "section",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.section",
                    ),
                ),
                (
                    "semester",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.semester",
                    ),
                ),
                ("subjects", models.ManyToManyField(to="classroom.subject")),
                (
                    "year",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.year",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateField(
                        default=datetime.datetime(2023, 10, 7, 10, 53, 32, 114826)
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("working", "Working Day"),
                            ("nonworking", "Non Working Day"),
                        ],
                        default="working",
                        max_length=25,
                    ),
                ),
                ("students", models.ManyToManyField(to="users.studentprofile")),
            ],
        ),
    ]