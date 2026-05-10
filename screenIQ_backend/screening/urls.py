from django.urls import path

from .views import (
    ScreenCandidateView,
    ApplicationListView,
    ApplicationDetailView
)

urlpatterns = [
    path('screen/', ScreenCandidateView.as_view()),

    path('applications/', ApplicationListView.as_view()),

    path('applications/<int:pk>/', ApplicationDetailView.as_view()),
]