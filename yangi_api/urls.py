from django.urls import path


from . import views



urlpatterns = [
    path("news/", views.NewsApiView.as_view()),
    path("news/<int:pk>/", views.SingleNewsApiView.as_view()),
    path("login/", views.CustomAuthToken.as_view()),
]