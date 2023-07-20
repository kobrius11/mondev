# Generated by Django 4.2.2 on 2023-07-05 08:51

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0003_coursegroup_course_code_course_price_topicmaterial_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='code',
            field=models.SlugField(blank=True, max_length=7, null=True, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='coursegroup',
            name='code',
            field=models.SlugField(blank=True, max_length=7, null=True, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='coursegroup',
            name='name',
            field=models.CharField(db_index=True, max_length=127, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='topicmaterial',
            name='name',
            field=models.CharField(db_index=True, max_length=127, verbose_name='name'),
        ),
    ]