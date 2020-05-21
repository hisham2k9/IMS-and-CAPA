from django.db import models

# Create your models here.
class Departments(models.Model):
    dept_id=models.IntegerField(primary_key=False, default=0)
    dept_name=models.CharField(max_length=140, unique=True, null=True, blank=True,default='Unknown')
    
    def __str__(self):
        return self.dept_name

class Locations(models.Model):
    loc_id=models.IntegerField(primary_key=False, default=0)
    loc_name=models.CharField(max_length=140, unique=True, null=True, blank=True, default='Unknown')
    
    def __str__(self):
        return self.loc_name
    
class Doctors(models.Model):
    doc_id=models.IntegerField(primary_key=False, default=0)
    emp_code=models.CharField(max_length=80)
    doc_name=models.CharField( max_length=150, unique=True, null = True, blank=True,default='Unknown')
    doc_sex=models.CharField(max_length=10)
    doc_designation=models.CharField(max_length=150)
    dept_name=models.ForeignKey('Departments', to_field='dept_name', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.doc_name
    
    