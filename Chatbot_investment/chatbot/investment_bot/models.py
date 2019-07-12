from django.db import models

# Create your models here.
class user_database(models.Model):
    employee_code=models.CharField(max_length=264,unique=True,primary_key=True)
    name=models.CharField(max_length=264)
    Father_or_Husband_name=models.CharField(max_length=264)
    Company_name=models.CharField(max_length=264)
    dob=models.DateField()
    Gender=models.CharField(max_length=264)
    location=models.CharField(max_length=264)
    PAN=models.CharField(max_length=264)
    Contact_Number=models.CharField(max_length=264)
    Date_of_Join=models.DateField()

class Section_Details(models.Model):
    section_id=models.CharField(max_length=100)
    subsection_id=models.CharField(max_length=100)
    query=models.CharField(max_length=10000)
    class Meta:
        unique_together=(("section_id","subsection_id"),)

class Amount_Restrictions(models.Model):
    section_id=models.CharField(max_length=100)
    subsection_id=models.CharField(max_length=100)
    Max_Amount=models.IntegerField()
    Additional_Amount=models.IntegerField()
    class Meta:
        unique_together=(("section_id","subsection_id"),)

class Section_Deduction(models.Model):
    year=models.CharField(max_length=10)
    employee_code=models.CharField(max_length=100)
    section_id=models.CharField(max_length=100)
    subsection_id=models.CharField(max_length=100)
    amount=models.IntegerField()
