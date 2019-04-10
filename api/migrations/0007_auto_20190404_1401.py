# Generated by Django 2.0 on 2019-04-04 06:01

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.query_utils


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20180611_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrolledcourse',
            name='course',
            field=models.ForeignKey(limit_choices_to=django.db.models.query_utils.Q(_negated=True, course_type=2), on_delete=django.db.models.deletion.CASCADE, to='api.Course'),
        ),
        migrations.AlterField(
            model_name='enrolleddegreecourse',
            name='mentor',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 1}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_students', to='api.Account', verbose_name='导师'),
        ),
        migrations.AlterField(
            model_name='homeworkrecord',
            name='mentor',
            field=models.ForeignKey(limit_choices_to={'role': 1}, on_delete=django.db.models.deletion.CASCADE, related_name='my_stu_homework_record', to='api.Account', verbose_name='导师'),
        ),
        migrations.AlterField(
            model_name='studyrecord',
            name='course_module',
            field=models.ForeignKey(limit_choices_to={'course_type': 2}, on_delete=django.db.models.deletion.CASCADE, to='api.Course', verbose_name='学位模块'),
        ),
        migrations.AlterField(
            model_name='stufollowuprecord',
            name='mentor',
            field=models.ForeignKey(limit_choices_to={'role': 1}, on_delete=django.db.models.deletion.CASCADE, related_name='mentor', to='api.Account', verbose_name='导师'),
        ),
    ]
