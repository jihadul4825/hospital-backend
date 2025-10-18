from django.db import models
from user.models import Account
from patient.models import Patient
from django.utils.text import slugify


class Specialization(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Designation(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class AvailableTime(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="doctor/images", null=True, blank=True)
    designation = models.ManyToManyField(Designation)
    specialization = models.ManyToManyField(Specialization)
    available_time = models.ManyToManyField(AvailableTime)
    mobile_no = models.CharField(max_length=12, null=True, blank=True)
    fee = models.IntegerField()
    meet_link = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    

START_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]
class Review(models.Model):
    reviewer = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(choices=START_CHOICES, max_length=10)

    def __str__(self):
        return f"Patient : {self.reviewer.user.first_name} {self.reviewer.user.last_name} | Doctor : {self.doctor.user.first_name} {self.doctor.user.last_name}"

