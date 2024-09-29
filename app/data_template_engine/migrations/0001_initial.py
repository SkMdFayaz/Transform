# Generated by Django 4.2.16 on 2024-09-26 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attribute_library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DataTemplateMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mappings', to='data_template_engine.datatemplate')),
                ('destination_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_mappings', to='attribute_library.field')),
                ('source_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_mappings', to='attribute_library.field')),
            ],
        ),
    ]
