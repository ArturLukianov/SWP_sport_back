# Generated by Django 3.1.8 on 2021-06-16 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0053_student_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_status',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='sport.studentstatus'),
        ),
    ]