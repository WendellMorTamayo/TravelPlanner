from django.urls import path, include
from . import views


urlpatterns = [
    path('trip/', views.TripPlanner.as_view(), name="trip"),
    path('', views.HomePageView.as_view(), name="index"),
    path('logout/', views.user_logout, name='logout'),
    path('delete_trip/<int:trip_id>/', views.TripDeleteView.as_view(), name='delete_trip'),
    path('update_trip/<int:trip_id>/', views.TripUpdateView.as_view(), name='update_trip'),
]
