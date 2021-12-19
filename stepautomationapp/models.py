from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from PIL import Image


class UserData(models.Model):
    userrelation = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=225, null=True, blank=True)
    city = models.CharField(max_length=225, null=True, blank=True)
    profilepic = models.ImageField(upload_to='media', default='media/profilepic.png')
    address = models.TextField(null=True, blank=True)
    zipcode = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return self.userrelation


class UserFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projectName = models.CharField(max_length=225)
    customerName = models.CharField(max_length=225)
    description = models.TextField()
    userFile = models.FileField(upload_to='userfiles')


class Country(models.Model):
    country = models.CharField(max_length=225)

    def __str__(self):
        return self.country


class City(models.Model):
    countryrel = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=225)

    def __str__(self):
        return self.city


class ProjectTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=225)
    lead = models.CharField(max_length=12)
    added_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.description

    def get_step_count(self):
        return Steps.objects.filter(project_template=self).count()


class Steps(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.FloatField()
    description = models.CharField(max_length=224)
    instruction = models.TextField()
    visibility = models.BooleanField(default=False)
    download = models.BooleanField(default=False)
    step_file = models.FileField(upload_to='stepfiles')
    upload = models.BooleanField(default=False)
    project_template = models.ForeignKey(ProjectTemplate, on_delete=models.CASCADE, related_name='project_template')


class Documents(models.Model):
    user = models.CharField(max_length=225)
    description = models.CharField(max_length=225)
    step_file = models.FileField(upload_to='documents')
    file_add_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description + "-" + self.user


class Customers(models.Model):
    user = models.CharField(max_length=225)
    customer_name = models.CharField(max_length=225)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    email = models.EmailField(max_length=225)
    location = models.CharField(max_length=225)
    customer_added_date = models.DateTimeField(auto_now=True)



class CustomerWorkflow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.CharField(max_length=225)
    description = models.CharField(max_length=225)
    status = models.CharField(max_length=15)
    lead = models.CharField(max_length=12)
    added_date = models.DateField(auto_now_add=True)    


    def __str__(self):
        return self.description

    def get_step_count(self):
        return CustomerSteps.objects.filter(customerworkflow=self).count()

class CustomerSteps(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.FloatField()
    description = models.CharField(max_length=224)
    instruction = models.TextField()
    visibility = models.BooleanField(default=False)
    download = models.BooleanField(default=False)
    step_file = models.FileField(upload_to='customer_stepfiles')
    upload = models.BooleanField(default=False)
    customerworkflow = models.ForeignKey(CustomerWorkflow, on_delete=models.CASCADE, related_name='customerworkflow')