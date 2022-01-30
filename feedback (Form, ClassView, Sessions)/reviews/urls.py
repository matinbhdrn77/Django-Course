from django.urls import path

from . import views

urlpatterns = [
    path('', views.ReviewView.as_view()),
    path('thank-you', views.Thank_youView.as_view()),
    path('reviews', views.ReviewListView.as_view()),
    path('review/favourite', views.AddFavouriteView.as_view(), name="review-favourite"),
    path('review/<int:pk>', views.ReviewDetailView.as_view(), name="review-detail")
]