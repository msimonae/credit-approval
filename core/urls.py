from django.urls import path
from . import views

urlpatterns = [
    path('loan/', views.loan_list),
    path('loan/<str:uuid>/', views.proposal_detail),
    
]