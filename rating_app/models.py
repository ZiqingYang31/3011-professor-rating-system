from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Professor(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.id})"


class Module(models.Model):
    code = models.CharField(max_length=10, primary_key=True) 
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.code})"


class ModuleInstance(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField(choices=[(1, "Semester 1"), (2, "Semester 2")]) 
    professors = models.ManyToManyField(Professor) 
    class Meta:
        unique_together = ('module', 'year', 'semester') 

    def __str__(self):
        return f"{self.module.name} ({self.year} - S{self.semester})"


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module_instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = ('user', 'professor', 'module_instance')

    def __str__(self):
        return f"{self.user.username} rated {self.professor.name} {self.rating}/5 in {self.module_instance.module.name} ({self.module_instance.year} - S{self.module_instance.semester})"
    
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
