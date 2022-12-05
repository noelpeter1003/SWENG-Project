from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path("", views.homePage, name="githubPage"),
    path("home", views.index, name='home'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
