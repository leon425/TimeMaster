from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Quarterly_goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)

    def __str__ (self):
        return self.name

class Monthly_goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)

    def __str__ (self):
        return self.name

class Weekly_goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    weekNum = models.CharField(max_length=200, default=0)

    def __str__ (self):
        return self.name

class Timebox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    weekNum = models.CharField(max_length=200, default=0)

    def __str__ (self):
        return self.name

class ItemSchedule(models.Model):
    timebox = models.ForeignKey(Timebox, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=300, null=True)
    complete = models.BooleanField(null=True)

    def __str__(self):
        return self.text

class ItemGoal(models.Model):
    timebox = models.ForeignKey(Timebox, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=300, null=True)
    complete = models.BooleanField(null=True)

    def __str__(self):
        return self.text
    
class ItemPriority(models.Model):
    timebox = models.ForeignKey(Timebox, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=300, null=True)
    complete = models.BooleanField(null=True)

    def __str__(self):
        return self.text
    
class ListOfWeekNum_2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    weekId = models.IntegerField()

    def __str__(self):
        return self.weekId