from django.db import models
from django.contrib.auth.models import User


class FoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack')
    ])
    food_item = models.CharField(max_length=100)
    calories = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date', 'meal_type']

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.meal_type}: {self.food_item}"