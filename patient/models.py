from django.db import models
from user.models import Account


class Patient(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="patient/images/", null=True, blank=True)
    mobile_no = models.CharField(max_length=12)
    
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    


