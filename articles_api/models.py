from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pages = models.IntegerField(default=10)
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.title} by {self.author}'


class Car(models.Model):
    manufacturer = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    num_seats = models.IntegerField()
    drive_range = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.owner}'s {self.name} by {self.manufacturer}"


class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    dob = models.DateTimeField()

    def __str__(self):
        return self.name


