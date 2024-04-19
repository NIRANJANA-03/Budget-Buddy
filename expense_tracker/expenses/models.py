from django.db import models
from django.contrib.auth.models import User
import datetime

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    emergency = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profession = models.CharField(max_length=100, blank=True, null=True)
    savings = models.DecimalField(max_digits=10, decimal_places=2, default=0)  

    class Meta:
        managed = True

    def __str__(self):
        return f"Income of {self.amount} for {self.user.username}"


class ExpenseCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    fixed_expense = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.category} for {self.user.username} with {self.fixed_expense}"
    
class ExpenseDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    category = models.CharField(max_length=100)
    cat_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    month_year = models.DateField(default=datetime.date.today().replace(day=1)) 
    
    def __str__(self):
        return f"{self.category} - {self.month_year}"
    
class ExpenseSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    month_year = models.DateField(default=datetime.date.today().replace(day=1))  
    total = models.DecimalField(max_digits=10, decimal_places=2) 
    status = models.IntegerField(default=0) 

    def __str__(self):
        return f"{self.user.username} - {self.month_year}: ${self.total}"
    

class TDetails(models.Model):
    tour_name = models.CharField(max_length=100,primary_key=True) 
    budget = models.DecimalField(max_digits=10,decimal_places=2)
    duration = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(default=0) 
    remaining = models.DecimalField(max_digits=10,decimal_places=2,default=0) 
    

    def __str__(self):
        return self.tour_name
    
class Tcat(models.Model):
    
    tour_name = models.CharField(max_length=100) 
    category = models.CharField(max_length=100)
    expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    

    def __str__(self):
        return f"{self.category} ---{self.tour_name}"
    


class DEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    event_location = models.CharField(max_length=100)
    num_persons = models.IntegerField()
    president_name = models.CharField(max_length=100)
    president_email = models.EmailField()
    program_secretary_name = models.CharField(max_length=100)
    program_secretary_email = models.EmailField()
    status = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    collected = models.DecimalField(max_digits=10, decimal_places=2, default=0)  

    def __str__(self):
        return self.event_name
    
class CatEvent(models.Model):
    event_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    expense = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)

    def __str__(self):
        return f"{self.event_name} - {self.category}"