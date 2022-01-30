from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<int:month>", views.month_by_num),
    path("<month>", views.monthly_challenges, name="month-challenge")
]
