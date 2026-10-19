from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.Health.as_view()),
    path("profile/", views.ProfileDetail.as_view()),
    path("projects/", views.ProjectList.as_view()),
    path("services/", views.ServiceList.as_view()),
    path("skills/", views.SkillList.as_view()),
    path("contact/", views.ContactCreate.as_view()),
]
