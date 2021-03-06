# Generated by Django 4.0.4 on 2022-04-22 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyDetails',
            fields=[
                ('serial_number', models.IntegerField(db_column='Serial_Number', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', max_length=100)),
                ('description', models.CharField(blank=True, db_column='Description', max_length=4000, null=True)),
            ],
            options={
                'db_table': 'company_details',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('serial_number', models.IntegerField(db_column='Serial_Number', primary_key=True, serialize=False)),
                ('company', models.CharField(db_column='Company', max_length=100)),
                ('job_position', models.CharField(db_column='Job_Position', max_length=200)),
                ('location', models.CharField(db_column='Location', max_length=200)),
            ],
            options={
                'db_table': 'jobs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JobTypes1',
            fields=[
                ('category', models.CharField(db_column='Category', max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'job_types1',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JobTypes2',
            fields=[
                ('subcategory', models.CharField(db_column='Subcategory', max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'job_types2',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='States',
            fields=[
                ('state', models.CharField(db_column='State', max_length=45, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'states',
                'managed': False,
            },
        ),
    ]
