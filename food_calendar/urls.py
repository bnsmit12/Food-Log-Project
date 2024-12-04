from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.contrib.auth import views as auth_views

from food_log import views


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
urlpatterns = [
    path('', views.redirect_to_calendar, name='redirect_to_calendar'),
    path('admin/', admin.site.urls),
    path('', include('food_log.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logout/', CustomLogoutView.as_view(template_name='registration/logout.html'), name='logout'),]