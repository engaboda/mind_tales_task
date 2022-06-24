from django.db import models
from django.contrib.auth.models import User
import timezone


class Restaurant(models.Model):
    """
        # o Authentication
        # o Creating restaurant
    """
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'Restaurant Name: {self.name} with id: {self.id}'


class Employee(models.Model):
    # o Creating employee 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='employees', help_text="Employee")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'Employee: {self.name} working with: {self.restaurant.name} with id: {self.id}'


class Menu(models.Model):
    # uploading menus using the system every day over API
    # Employees will vote for menu before leaving for lunch on mobile app
    # for whom backend has to be implemented
    # There are users which did not update app to the latest version and
    # backend has to support both versions.
    # Mobile app always sends build version in headers.
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='menus', help_text="Menu")
    name = models.CharField(max_length=100)
    menu_date = models.DateField(default=timezone.now)


    def __str__(self):
        return f'Menu from Restaurant: {self.restaurant.name} with id: {self.id}'


class Vote(models.Model):
    # o Voting for restaurant menu (Old version api accepted one menu, New one accepts top three menus with respective points (1 to 3)
    # o Getting results for current day
    # o Getting current day menu
    menu = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='votes', help_text="Vote")
    
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='votes', help_text="Vote")

    def __str__(self):
        return f'Vote from : {self.employee.name} for: {self.menu.id}'
