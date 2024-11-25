from django.urls import path

from petrol_spy import views

urlpatterns = [
    path('leaderboard', views.GetLeaderboardView.as_view()),
]
