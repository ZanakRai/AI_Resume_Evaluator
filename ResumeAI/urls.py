from django.urls import path
from .views import JobDescriptionView,ResumeAPIView

urlpatterns = [
    path('jobs/',JobDescriptionView.as_view()),
    path('resume/',ResumeAPIView.as_view()),
]