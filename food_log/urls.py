from django.urls import path, include
from . import views
from django.urls import path
from .views import signup
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('verify_code/', views.verify_code, name='verify_code'),
    path('request-reset/', views.request_reset, name='request_reset'),
    path('verify-reset-code/', views.verify_reset_code, name='verify_reset_code'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('add-food-entry/', views.add_food_entry, name='add_food_entry'),
    path('api/food-entries/', views.get_food_entries, name='get_food_entries'),
    path('food-log/new-entry/', views.new_food_entry, name='new_entry'),
    path('food-log/view-entries/', views.view_entries, name='view_entries'),
    path('food-log/delete-entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),

]