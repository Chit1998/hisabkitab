from django.contrib import admin
from django.urls import path
from apis import views

urlpatterns = [
    path('offers', views.OfferUpload.as_view(), name="offers"),
    path('OffersData', views.OffersData),
]