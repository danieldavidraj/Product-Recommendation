from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_products),
    path('popularity', views.popularity_based),
    path('collaborative', views.model_based),
    path('hybrid', views.hybrid_based),
    path('knn', views.knn_based)
]