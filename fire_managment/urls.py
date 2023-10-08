from django.urls import path
from fire_managment import views

urlpatterns = [
    path("select_points/<str:x_1>/<str:x_2>/<str:y_1>/<str:y_2>/", views.select_points, name= "select points"),
    path("add_point/", views.add_points, name="add_point"),
    path("monitor_area", views.monitor_area, name="monitor_area"),
    path('register_user/', views.register_user, name="register_user"),
]