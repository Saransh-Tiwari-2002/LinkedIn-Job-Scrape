from django.db import models

# Create your models here.
class JobTypes1(models.Model):
    category = models.CharField(db_column='Category', primary_key=True, max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'job_types1'
    


class JobTypes2(models.Model):
    subcategory = models.CharField(db_column='Subcategory', primary_key=True, max_length=100)  # Field name made lowercase.
    category = models.ForeignKey(JobTypes1, models.DO_NOTHING, db_column='Category')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'job_types2'


class States(models.Model):
    state = models.CharField(db_column='State', primary_key=True, max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'states'

class CompanyDetails(models.Model):
    serial_number = models.IntegerField(db_column='Serial_Number', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    state = models.ForeignKey('States', models.DO_NOTHING, db_column='State')  # Field name made lowercase.
    subcategory = models.ForeignKey('JobTypes2', models.DO_NOTHING, db_column='Subcategory')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'company_details'

class Jobs(models.Model):
    serial_number = models.IntegerField(db_column='Serial_Number', primary_key=True)  # Field name made lowercase.
    company = models.CharField(db_column='Company', max_length=100)  # Field name made lowercase.
    job_position = models.CharField(db_column='Job_Position', max_length=200)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=200)  # Field name made lowercase.
    subcategory = models.ForeignKey(JobTypes2, models.DO_NOTHING, db_column='Subcategory')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'jobs'

